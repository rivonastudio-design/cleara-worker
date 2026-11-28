"""Auto-Fix: deterministic whole-document repairs for a small set of safe finding types.

Each fix_type resolves one or more analyzer finding codes and knows how to repair the file.
Two kinds of fix:
  - "gs": a single Ghostscript invocation (whole-document, no design judgment needed).
  - "python": a PyMuPDF-based content-stream edit, for repairs Ghostscript has no flag for.

v1 (27 Nov 2026): rgb_to_cmyk, transparency_flatten.
v2 (28 Nov 2026, owner asked "fix kardo 4"): force_single_colour, pure_black,
remove_blank_pages, add_crop_marks.

Each of these was picked because it's a reliable, deterministic transform that does not
depend on having the original design assets (fonts, higher-res photos) or guessing design
intent (repositioning text/logos, extending bleed, resizing artwork). See
claude/future_features.md for the fuller safe / risky / never list, and for why font-embed,
repositioning and resizing are NOT in this list.
"""
import os
import re
import subprocess

import fitz  # PyMuPDF

PT_MM = 72 / 25.4
def mm(pt): return pt * (25.4 / 72)
def pts(m): return m * PT_MM


# ---------------------------------------------------------------- python-kind fix bodies

def _mixblack(c, m, y, k):
    """Same definition analyzer.py uses to FLAG a mixed black (analyzer._mixblack) -- reused
    here so the fix resolves exactly what the finding warned about, nothing more/less."""
    return (k >= 0.6 and c + m + y >= 0.3) or min(c, m, y) >= 0.6

# matches "<c> <m> <y> <k> k" or "... K" (CMYK fill/stroke colour operators) in a raw,
# decompressed PDF content stream. Deliberately does NOT touch sc/scn (named/pattern/spot
# colours) -- only direct device-CMYK operators, which is what analyzer._mixblack checks.
_K_OP_RE = re.compile(
    rb'([+-]?[\d.]+)\s+([+-]?[\d.]+)\s+([+-]?[\d.]+)\s+([+-]?[\d.]+)\s+([kK])(?![a-zA-Z])'
)

def _fix_mixblack_bytes(data):
    def repl(m):
        try:
            c, y_, yy, k = (float(m.group(i)) for i in (1, 2, 3, 4))
        except ValueError:
            return m.group(0)
        if _mixblack(c, y_, yy, k):
            return b"0 0 0 1 " + m.group(5)
        return m.group(0)
    return _K_OP_RE.sub(repl, data)

def _fix_pure_black(in_path, out_path, context):
    """Rewrites every direct-CMYK fill/stroke colour operator that matches analyzer's
    'mixed black' definition to pure 100K. Only touches page content streams (not nested
    Form XObjects/patterns) -- a known v1 limitation, acceptable since the common case
    (body text, thin rule lines set in a near-black CMYK mix) lives directly on the page."""
    doc = fitz.open(in_path)
    for page in doc:
        data = page.read_contents()
        new_data = _fix_mixblack_bytes(data)
        if new_data != data:
            xref = doc.get_new_xref()
            doc.update_object(xref, "<<>>")
            doc.update_stream(xref, new_data)
            page.set_contents(xref)
    doc.save(out_path, garbage=4, deflate=True)

def _fix_remove_blank_pages(in_path, out_path, context):
    """Deletes the specific pages the client confirmed are blank (context['pages'], 1-based).
    Page count changes -- the caller (worker.py) is responsible for renumbering every other
    finding's page field to match, and for rendering a full fresh preview rather than
    per-page ones, since old page numbers no longer line up."""
    pages = sorted(set(context.get("pages") or []), reverse=True)
    if not pages:
        raise ValueError("remove_blank_pages: no pages given")
    doc = fitz.open(in_path)
    for p in pages:
        if 1 <= p <= doc.page_count:
            doc.delete_page(p - 1)
    if doc.page_count < 1:
        raise RuntimeError("remove_blank_pages: would delete every page, refusing")
    doc.save(out_path, garbage=4, deflate=True)

def _infer_trim(full, ex):
    """Same logic as analyzer._infer_trim: is the page = job size + equal extra margin on
    all sides? Re-implemented here (not imported) to keep fixes.py independent of analyzer's
    internals -- this is the exact condition crop_marks already fired on."""
    W, H = mm(full.width), mm(full.height)
    for ew, eh in ((ex[0], ex[1]), (ex[1], ex[0])):
        dx, dy = W - ew, H - eh
        if 1.0 <= dx <= 40 and 1.0 <= dy <= 40 and abs(dx - dy) <= 2.0:
            ax, ay = pts(dx) / 2, pts(dy) / 2
            return fitz.Rect(full.x0 + ax, full.y0 + ay, full.x1 - ax, full.y1 - ay)
    return None

def _fix_add_crop_marks(in_path, out_path, context):
    """Draws standard 4-corner crop marks just outside the trim box, on the pages the client
    confirmed need them (context['pages']) -- same trim-box inference analyzer uses to decide
    a page qualifies (page = job size + equal margin on every side). Marks are pure K100,
    hairline width, length/gap scaled down if the margin is small so they never cross back
    into the trim area or off the page."""
    pages = set(context.get("pages") or [])
    width_mm, height_mm = context["width_mm"], context["height_mm"]
    if not pages:
        raise ValueError("add_crop_marks: no pages given")
    doc = fitz.open(in_path)
    for pno in pages:
        if not (1 <= pno <= doc.page_count):
            continue
        page = doc[pno - 1]
        full = page.rect
        trim = _infer_trim(full, (width_mm, height_mm))
        if trim is None:
            continue
        margin = min(trim.x0 - full.x0, full.x1 - trim.x1, trim.y0 - full.y0, full.y1 - trim.y1)
        if margin < pts(1.0):
            continue
        gap = min(pts(2.0), margin * 0.3)
        length = min(pts(3.0), margin * 0.6)
        shape = page.new_shape()
        for cx, cy, sx, sy in ((trim.x0, trim.y0, -1, -1), (trim.x1, trim.y0, 1, -1),
                               (trim.x0, trim.y1, -1, 1), (trim.x1, trim.y1, 1, 1)):
            shape.draw_line((cx + sx * gap, cy), (cx + sx * (gap + length), cy))
            shape.draw_line((cx, cy + sy * gap), (cx, cy + sy * (gap + length)))
        shape.finish(color=(0, 0, 0, 1), width=0.5, closePath=False)
        shape.commit()
    doc.save(out_path, garbage=4, deflate=True)


FIX_SPECS = {
    "rgb_to_cmyk": {
        "kind": "gs", "codes": {"rgb_color"},
        "gs_args": [
            "-sDEVICE=pdfwrite", "-sColorConversionStrategy=CMYK",
            "-dProcessColorModel=/DeviceCMYK", "-dCompatibilityLevel=1.4",
            "-dAutoRotatePages=/None",
        ],
    },
    "transparency_flatten": {
        "kind": "gs", "codes": {"transparency"},
        "gs_args": [
            "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.3", "-dAutoRotatePages=/None",
        ],
    },
    "force_single_colour": {
        "kind": "gs", "codes": {"single_colour_mix"},
        "gs_args": [
            "-sDEVICE=pdfwrite", "-sColorConversionStrategy=Gray",
            "-dProcessColorModel=/DeviceGray", "-dCompatibilityLevel=1.4",
            "-dAutoRotatePages=/None",
        ],
    },
    "pure_black": {"kind": "python", "codes": {"mix_black"}, "fn": _fix_pure_black},
    "remove_blank_pages": {"kind": "python", "codes": {"blank_page"}, "fn": _fix_remove_blank_pages},
    "add_crop_marks": {"kind": "python", "codes": {"crop_marks"}, "fn": _fix_add_crop_marks},
}

# fix_types whose page count can change (findings on later pages need renumbering, and the
# "after" preview should show the whole document, not just the originally-affected pages).
RENUMBERING_FIXES = {"remove_blank_pages"}


def resolved_codes(fix_type):
    spec = FIX_SPECS.get(fix_type)
    return spec["codes"] if spec else set()


def apply_fix(fix_type, in_path, out_path, context=None, timeout=120):
    """Runs the transform for fix_type on in_path, writing out_path. Raises on any failure
    (non-zero exit / missing-empty output for gs fixes, any exception for python fixes) --
    callers must not treat a partially-written file as success."""
    spec = FIX_SPECS.get(fix_type)
    if not spec:
        raise ValueError(f"unknown fix_type: {fix_type}")
    if spec["kind"] == "gs":
        cmd = ["gs", "-o", out_path, *spec["gs_args"], in_path]
        r = subprocess.run(cmd, capture_output=True, timeout=timeout)
        if r.returncode != 0 or not os.path.exists(out_path) or os.path.getsize(out_path) < 100:
            raise RuntimeError(
                f"ghostscript failed (code {r.returncode}) for {fix_type}: "
                f"{r.stderr.decode('utf-8', 'ignore')[:500]}"
            )
    else:
        spec["fn"](in_path, out_path, context or {})
        if not os.path.exists(out_path) or os.path.getsize(out_path) < 100:
            raise RuntimeError(f"{fix_type} produced no usable output file")
    return out_path
