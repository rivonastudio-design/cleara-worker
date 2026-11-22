"""Cleara preflight v2 (PDF + JPG/PNG). PyMuPDF + numpy only.

Severity rules:
  error   -> file result "error"
  warning -> file result "warning"
  confirm -> "please look once"; does NOT change the file result (file can still be "ok")
"""
import re, time
import warnings; warnings.filterwarnings("ignore")
import numpy as np
import pymupdf as fitz
from messages import build

# QR/barcode detection (zbar) -- optional: if the system zbar library isn't present for any
# reason, this check is simply skipped rather than crashing the whole analysis (same defensive
# pattern as the Hindi spelling dictionary, which is also loaded lazily/optionally elsewhere).
try:
    from pyzbar.pyzbar import decode as _zbar_decode, ZBarSymbol as _ZBarSymbol
    # every common commercial-print symbology except DATABAR/DATABAR_EXP: those two hit an
    # internal zbar assertion bug on some unrelated dense patterns (prints a scary-looking but
    # harmless warning to stderr) and are not a symbology Cleara's print jobs actually use
    _ZBAR_SYMBOLS = [s for s in _ZBarSymbol if s.name not in
                      ("NONE", "PARTIAL", "DATABAR", "DATABAR_EXP", "COMPOSITE", "SQCODE")]
except Exception:
    _zbar_decode = None

PT_MM = 25.4 / 72.0
def mm(pt): return pt * PT_MM
def pts(m): return m / PT_MM

DEFAULTS = {"bleed_mm": 5.0, "safe_mm": 6.0, "min_dpi_warn": 300, "min_dpi_err": 150,
            "min_text_pt": 6.0, "min_line_pt": 0.25, "max_tac": 300, "expected_mm": None,
            "mode": "single",          # "single" or "sheet" (mixed-job sheet)
            "shape_cut": False,        # shape / die cutting job -> needs cut_overlap_mm
            "single_colour": False,    # single-colour job -> mixed colours are an error
            "k_limit": 30,             # % black inside mixed colours / photos -> confirm
            "cut_overlap_mm": 6.0, "max_paths": 8000, "white_text_pt": 8.0,
            "qr_min_mm": 15.0}         # recommended minimum QR/barcode size for a reliable print scan
CAP = 12            # max findings of one kind in a report
PIXEL_PAGES = 60    # pages that get the ink (pixel) checks
QR_BARCODE_PAGES = 20   # pages that get the QR/barcode scan (needs its own sharper render, costs more time)
STREAM_LIMIT = 8_000_000

# alignment / layout design-quality thresholds (business card, letterhead, etc. -- "do things line
# up the way a professional design would"). Below ALIGN_TOL_MM = already aligned, don't flag.
# Above ALIGN_NEARMISS_MM = probably two unrelated/intentionally-different elements, don't flag.
# Only the in-between band (a few mm) looks like a genuine near-miss slip, so only that is flagged.
ALIGN_TOL_MM = 0.3
ALIGN_NEARMISS_MM = 2.5
ICON_MIN_MM, ICON_MAX_MM = 2.0, 14.0   # size range that looks like a contact icon, not a logo/photo


class Findings:
    def __init__(self):
        self.items, self.seen, self.count = [], set(), {}

    def add(self, code, sev, page=None, bbox=None, v="", e="", key=None):
        k = (code, page, key if key is not None else str(v))
        if k in self.seen: return
        self.seen.add(k)
        n = self.count.get(code, 0)
        if n >= CAP: return
        self.count[code] = n + 1
        msg, fix = build(code, v, e)
        self.items.append({"code": code, "severity": sev, "page": page,
                           "bbox": [round(float(x), 1) for x in bbox] if bbox else None,
                           "value": str(v), "expected": str(e), "msg": msg, "fix": fix})

    def has(self, code, page=None):
        return any(f["code"] == code and (page is None or f["page"] == page) for f in self.items)


# ---------------------------------------------------------------- content-stream scan
_TOK = re.compile(rb"\((?:\\.|[^\\()])*\)|<<|>>|<[0-9A-Fa-f\s]*>|/[^\s/\[\]()<>{}%]*"
                  rb"|[-+]?(?:\d+\.?\d*|\.\d+)|[A-Za-z'\"*]+|[\[\]]")
_INLINE = re.compile(rb"\bBI\b.*?\bEI\b", re.S)
_FILL = {b"f", b"F", b"f*", b"B", b"B*", b"b", b"b*"}
_STROKE = {b"S", b"s", b"B", b"B*", b"b", b"b*"}
_TEXT = {b"Tj", b"TJ", b"'", b'"'}
_THIN_FONT = re.compile(r"thin|hairline|ultra\s*light|extra\s*light|\blight\b", re.I)

def _white(c):
    if not c: return False
    k, v = c
    if k == "g": return v[0] >= 0.999
    if k == "rgb": return min(v) >= 0.999
    if k == "cmyk": return max(v) <= 0.001
    return False

def _reg(c):
    return bool(c) and c[0] == "cmyk" and min(c[1]) >= 0.99

def _mixblack(c):
    """a black that is built from several inks instead of K only"""
    if not c or c[0] != "cmyk": return False
    cy, m, y, k = c[1]
    return (k >= 0.6 and cy + m + y >= 0.3) or min(cy, m, y) >= 0.6

def scan_stream(data, gs_op):
    """Walk one content stream. Returns the print problems that only show in the drawing commands."""
    ev = {"white_op": False, "mix_text": False, "mix_line": False, "reg_fill": False,
          "reg_stroke": False, "rgb": False, "shading": False}
    data = _INLINE.sub(b" ", data[:STREAM_LIMIT])
    st = {"f": ("g", (0.0,)), "s": ("g", (0.0,)), "opf": False, "ops": False, "lw": 1.0}
    stack, nums, name = [], [], None
    for m in _TOK.finditer(data):
        t = m.group(); c = t[:1]
        if c in b"0123456789+-.":
            try: nums.append(float(t))
            except ValueError: pass
            continue
        if c == b"/": name = t[1:].decode("latin-1"); continue
        if c in b"(<[]>": continue
        op = t
        if op == b"q": stack.append(dict(st))
        elif op == b"Q":
            if stack: st = stack.pop()
        elif op in (b"g", b"G") and nums:
            st["f" if op == b"g" else "s"] = ("g", (nums[-1],))
        elif op in (b"rg", b"RG") and len(nums) >= 3:
            v = tuple(nums[-3:]); st["f" if op == b"rg" else "s"] = ("rgb", v)
            if min(v) < 0.999: ev["rgb"] = True
        elif op in (b"k", b"K") and len(nums) >= 4:
            st["f" if op == b"k" else "s"] = ("cmyk", tuple(nums[-4:]))
        elif op in (b"sc", b"scn", b"SC", b"SCN"):
            st["f" if op[:1] == b"s" else "s"] = ("cmyk", tuple(nums[-4:])) if len(nums) == 4 else None
        elif op in (b"cs", b"CS"):
            st["f" if op == b"cs" else "s"] = None
        elif op == b"w" and nums: st["lw"] = nums[-1]
        elif op == b"gs" and name in gs_op: st["opf"], st["ops"] = gs_op[name]
        elif op == b"sh": ev["shading"] = True
        else:
            if op in _FILL or op in _TEXT:
                if st["opf"] and _white(st["f"]): ev["white_op"] = True
                if _reg(st["f"]): ev["reg_fill"] = True
                if op in _TEXT and _mixblack(st["f"]) and not _reg(st["f"]): ev["mix_text"] = True
            if op in _STROKE:
                if st["ops"] and _white(st["s"]): ev["white_op"] = True
                if _reg(st["s"]): ev["reg_stroke"] = True
                elif st["lw"] < 1.0 and _mixblack(st["s"]): ev["mix_line"] = True
        nums, name = [], None
    return ev

def _gs_map(doc, xref):
    """ExtGState name -> (overprint fill, overprint stroke) for the resources of one page/form."""
    out = {}
    try:
        typ, val = doc.xref_get_key(xref, "Resources/ExtGState")
        if typ == "xref": val = doc.xref_object(int(val.split()[0]), compressed=True)
        elif typ != "dict": return out
    except Exception:
        return out
    def flags(txt):
        OP = re.search(r"/OP\s*true", txt) is not None
        m = re.search(r"/op\s*(true|false)", txt)
        return ((m.group(1) == "true") if m else OP, OP)
    for nm, x in re.findall(r"/([^\s/<>\[\]]+)\s+(\d+)\s+0\s+R", val):
        try: out[nm] = flags(doc.xref_object(int(x), compressed=True))
        except Exception: pass
    for nm, body in re.findall(r"/([^\s/<>\[\]]+)\s*<<(.*?)>>", val, re.S):
        out.setdefault(nm, flags(body))
    return out


# ---------------------------------------------------------------- page geometry
def _has_key(doc, page, key):
    try: return doc.xref_get_key(page.xref, key)[0] != "null"
    except Exception: return False

def _box_in_page(page, box):
    cb = page.cropbox
    r = fitz.Rect(box.x0 - cb.x0, box.y0 - cb.y0, box.x1 - cb.x0, box.y1 - cb.y0)
    if page.rotation:
        r = r * page.rotation_matrix; r.normalize()
    return r & page.rect

def _size_ok(w, h, ex):
    ew, eh = ex
    return (abs(w - ew) < 1.0 and abs(h - eh) < 1.0) or (abs(w - eh) < 1.0 and abs(h - ew) < 1.0)

def _infer_trim(full, ex):
    """No usable TrimBox: is the page = job size (+ equal extra on all sides)?"""
    W, H = mm(full.width), mm(full.height)
    for ew, eh in ((ex[0], ex[1]), (ex[1], ex[0])):
        if abs(W - ew) < 1.0 and abs(H - eh) < 1.0: return fitz.Rect(full), "exact"
    for ew, eh in ((ex[0], ex[1]), (ex[1], ex[0])):
        dx, dy = W - ew, H - eh
        if 1.0 <= dx <= 40 and 1.0 <= dy <= 40 and abs(dx - dy) <= 2.0:
            ax, ay = pts(dx) / 2, pts(dy) / 2
            return fitz.Rect(full.x0 + ax, full.y0 + ay, full.x1 - ax, full.y1 - ay), "inferred"
    return None, None

def _trim(doc, page, o):
    """returns (trim rect in page coords, source, size_ok). source: box / exact / inferred / none"""
    full, ex = page.rect, o["expected_mm"]
    if _has_key(doc, page, "TrimBox"):
        t = _box_in_page(page, page.trimbox)
        if not ex or _size_ok(mm(t.width), mm(t.height), ex): return t, "box", True
        t2, src = _infer_trim(full, ex)
        if t2 is not None: return t2, src, True
        return t, "box", False
    if ex:
        t2, src = _infer_trim(full, ex)
        if t2 is not None: return t2, src, True
        return fitz.Rect(full), "none", False
    return fitz.Rect(full), "none", True

def _thin_lines(drs):
    out = []
    for d in drs:
        r = d["rect"]
        if 4 <= max(r.width, r.height) < 60 and min(r.width, r.height) < 1.5 and len(d.get("items", [])) <= 2:
            out.append(r)
    return out

def _marks(drs, trim):
    """short thin lines outside the trim area = crop marks"""
    return sum(1 for r in _thin_lines(drs) if not r.intersects(trim)) >= 4

def _sheet_marks(drs):
    return len(_thin_lines(drs)) >= 8

def _item_islands(drs, img_infos, blocks, trim):
    """Group all page content (vector paths + images + text) into separate touching/overlapping
    clusters -- on a ganged sheet, this recovers each individual item's own footprint, since items
    are normally separated by a real gap (bleed + cut margin) while everything belonging to ONE
    item (its own text, logo, photo) sits close together."""
    cand = [fitz.Rect(d["rect"]) for d in drs if d["rect"].width >= 1 and d["rect"].height >= 1]
    cand += [fitz.Rect(info["bbox"]) for info in img_infos if info["bbox"][2]-info["bbox"][0] >= 1]
    for blk in blocks:
        for ln in blk.get("lines", []):
            for sp in ln["spans"]:
                r = fitz.Rect(sp["bbox"])
                if r.width >= 1 and r.height >= 1: cand.append(r)
    cand = [r for r in cand if r.intersects(trim)]
    pad = pts(2.0)   # merge pieces of the SAME item (gap < 2mm); real items on a sheet are spaced wider
    clusters, changed = cand, True
    while changed and len(clusters) > 1:
        changed = False
        out, used = [], [False] * len(clusters)
        for i in range(len(clusters)):
            if used[i]: continue
            cur = fitz.Rect(clusters[i]); used[i] = True
            for j in range(i + 1, len(clusters)):
                if used[j]: continue
                test = fitz.Rect(cur.x0 - pad, cur.y0 - pad, cur.x1 + pad, cur.y1 + pad)
                if test.intersects(clusters[j]):
                    cur |= clusters[j]; used[j] = True; changed = True
            out.append(cur)
        clusters = out
    return [r for r in clusters if r.width >= pts(5) and r.height >= pts(5)]   # drop tiny noise islands

def _grid_check(islands, tol_pt):
    """For straight-knife cutting, items must sit in a complete row/column grid -- every column's
    left edge lines up across every row, and every row's top edge lines up across every column, so
    one continuous straight cut separates a whole row or column at once. Returns
    (is_grid, same_size, rows, cols)."""
    if len(islands) < 2:
        return True, True, 1, len(islands)

    def cluster_vals(vals):
        vals = sorted(vals)
        groups = []
        for v in vals:
            if groups and v - groups[-1][0] <= tol_pt:
                groups[-1].append(v)
            else:
                groups.append([v])
        return [sum(g) / len(g) for g in groups]

    x0s, y0s = cluster_vals([r.x0 for r in islands]), cluster_vals([r.y0 for r in islands])

    def idx(val, cvals):
        return min(range(len(cvals)), key=lambda i: abs(cvals[i] - val))

    cells = set()
    for r in islands:
        cells.add((idx(r.y0, y0s), idx(r.x0, x0s)))
    is_grid = len(cells) == len(islands) == len(x0s) * len(y0s)

    widths = [r.width for r in islands]
    heights = [r.height for r in islands]
    same_size = (max(widths) - min(widths) <= pts(2)) and (max(heights) - min(heights) <= pts(2))
    return is_grid, same_size, len(y0s), len(x0s)


# ---------------------------------------------------------------- alignment / layout design-quality
def _text_lines(blocks):
    """one rect per visual line of text (merging that line's spans), not per span -- this is the
    right granularity for 'does this line start at the same x as that line' kind of checks."""
    out = []
    for blk in blocks:
        for ln in blk.get("lines", []):
            spans = [sp for sp in ln["spans"] if sp["text"].strip()]
            if not spans: continue
            r = fitz.Rect(spans[0]["bbox"])
            for sp in spans[1:]: r |= fitz.Rect(sp["bbox"])
            out.append(r)
    return out

def _icon_candidates(drs, img_infos, trim):
    """small, roughly-square clusters of vector paths or small images -- the size/shape a contact
    icon (phone, mail, location, whatsapp...) actually is, as opposed to a logo or photo."""
    cand = [fitz.Rect(d["rect"]) for d in drs if fitz.Rect(d["rect"]).width >= 0.5 and fitz.Rect(d["rect"]).height >= 0.5]
    pad = pts(0.8)   # merge the few paths that make up ONE icon glyph
    clusters, changed = cand, True
    while changed and len(clusters) > 1:
        changed = False
        out, used = [], [False] * len(clusters)
        for i in range(len(clusters)):
            if used[i]: continue
            cur = fitz.Rect(clusters[i]); used[i] = True
            for j in range(i + 1, len(clusters)):
                if used[j]: continue
                test = fitz.Rect(cur.x0 - pad, cur.y0 - pad, cur.x1 + pad, cur.y1 + pad)
                if test.intersects(clusters[j]):
                    cur |= clusters[j]; used[j] = True; changed = True
            out.append(cur)
        clusters = out
    icons = []
    for r in clusters:
        w, h = mm(r.width), mm(r.height)
        if ICON_MIN_MM <= w <= ICON_MAX_MM and ICON_MIN_MM <= h <= ICON_MAX_MM and 0.4 <= w / h <= 2.5 and r.intersects(trim):
            icons.append(r)
    for info in img_infos:
        r = fitz.Rect(info["bbox"]); w, h = mm(r.width), mm(r.height)
        if ICON_MIN_MM <= w <= ICON_MAX_MM and ICON_MIN_MM <= h <= ICON_MAX_MM and 0.4 <= w / h <= 2.5 and r.intersects(trim):
            icons.append(r)
    return icons

def _icon_text_pairs(icons, lines):
    """pair each icon with the nearest text line that sits beside it (same visual row, small gap)
    -- that's the icon's own label (e.g. the phone-icon's own phone number)."""
    pairs = []
    for ic in icons:
        best, best_gap = None, None
        for ln in lines:
            top, bot = max(ic.y0, ln.y0), min(ic.y1, ln.y1)
            if max(0, bot - top) < 0.3 * min(ic.height, ln.height): continue
            if ln.x0 >= ic.x1: gap = ln.x0 - ic.x1
            elif ic.x0 >= ln.x1: gap = ic.x0 - ln.x1
            else: continue   # overlapping horizontally -- not an icon-beside-text layout
            if gap > pts(15): continue
            if best_gap is None or gap < best_gap: best, best_gap = ln, gap
        if best is not None: pairs.append((ic, best))
    return pairs

def _stacks(lines):
    """group text lines into vertically-stacked blocks (an address/contact list, a name+title
    block) -- consecutive lines, sorted top to bottom, that sit close enough together (small gap
    relative to line height) to read as one running block, not unrelated far-apart text. Returns
    EVERY group, including lone single lines (a standalone title/heading is still a valid unit
    for the centering check) -- callers that need a genuine multi-line stack filter by length."""
    if not lines: return []
    ls = sorted(lines, key=lambda r: r.y0)
    stacks, cur = [], [ls[0]]
    for r in ls[1:]:
        prev = cur[-1]
        gap, lh = r.y0 - prev.y1, max(prev.height, r.height, 1)
        if -0.3 * lh < gap < 1.8 * lh:
            cur.append(r)
        else:
            stacks.append(cur); cur = [r]
    stacks.append(cur)
    return stacks

def _cluster1d(vals, tol):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    groups = []
    for i in order:
        if groups and vals[i] - vals[groups[-1][-1]] <= tol:
            groups[-1].append(i)
        else:
            groups.append([i])
    return groups

def _row_align_pairs(lines):
    """find two clearly-separate columns of short lines (a left column and a right column, like
    name on one side / phone number on the other of a business card) and pair up the lines that
    sit roughly in the same horizontal band -- those pairs are meant to be the same visual row."""
    short = [r for r in lines if r.width < 0.5 * max((x.width for x in lines), default=1) or len(lines) <= 6]
    if len(short) < 4: return []
    x0s = [r.x0 for r in short]
    groups = [[short[i] for i in g] for g in _cluster1d(x0s, pts(3.0))]
    cols = [g for g in groups if len(g) >= 2]
    if len(cols) < 2: return []
    cols.sort(key=lambda c: sum(r.x0 for r in c) / len(c))
    merged = []
    for c in cols:
        cx = sum(r.x0 for r in c) / len(c)
        if merged and cx - merged[-1][1] <= pts(15):
            merged[-1][0].extend(c)
        else:
            merged.append([c, cx])
    distinct = [c for c, _ in merged if len(c) >= 2]
    if len(distinct) < 2: return []
    A, B = distinct[0], distinct[1]
    out, used_b = [], [False] * len(B)
    for la in A:
        best_j, best_d = None, None
        for j, lb in enumerate(B):
            if used_b[j]: continue
            d = abs((la.y0 + la.y1) / 2 - (lb.y0 + lb.y1) / 2)
            if d > pts(6): continue
            if best_d is None or d < best_d: best_j, best_d = j, d
        if best_j is not None:
            used_b[best_j] = True
            out.append((la, B[best_j], mm(best_d)))
    return out


# ---------------------------------------------------------------- QR / barcode
def _scan_codes(page):
    """Render the page sharp enough for zbar to actually read a QR/barcode (the normal low-res
    preview render used for ink checks is too soft for small codes -- tested and confirmed this
    misses codes that a 300dpi render catches), then look for any QR/barcode on it.
    Returns a list of (type_label, size_mm, bbox_in_page_points)."""
    if _zbar_decode is None: return []
    r = page.rect
    scale = min(300 / 72.0, 3600 / max(r.width, r.height, 1))
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    from PIL import Image
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    out = []
    for z in _zbar_decode(im, symbols=_ZBAR_SYMBOLS):
        x, y, w, h = z.rect
        size_mm = mm(max(w, h) / scale)
        bbox = fitz.Rect(x / scale, y / scale, (x + w) / scale, (y + h) / scale)
        label = "QR Code" if z.type == "QRCODE" else "Barcode"
        out.append((label, size_mm, bbox))
    return out


# ---------------------------------------------------------------- pixel (ink) helpers
def _cmyk(page, max_px=1400):
    r = page.rect
    s = min(2.0, max_px / max(r.width, r.height))
    pix = page.get_pixmap(matrix=fitz.Matrix(s, s), colorspace=fitz.csCMYK, alpha=False)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :4]
    return a, s

def _crop(a, r, s):
    h, w = a.shape[:2]
    x0, y0 = max(0, int(round(r.x0 * s))), max(0, int(round(r.y0 * s)))
    x1, y1 = min(w, int(round(r.x1 * s))), min(h, int(round(r.y1 * s)))
    return a[y0:y1, x0:x1]

def _darkness(a):
    """how dark a pixel looks (0-255); yellow counts little"""
    f = a.astype(np.float32)
    return np.maximum.reduce([f[:, :, 3], 0.7 * f[:, :, 0], 0.7 * f[:, :, 1], 0.2 * f[:, :, 2]])

def _pct(x): return f"{x:.0f}%"


# ---------------------------------------------------------------- PDF
def analyze(path, profile="offset_coated", opts=None):
    t0 = time.time()
    o = dict(DEFAULTS); o.update({k: v for k, v in (opts or {}).items() if v is not None})
    sheet = str(o["mode"]) == "sheet"
    F = Findings(); add = F.add

    try:
        doc = fitz.open(path)
        if doc.needs_pass or doc.page_count == 0: raise ValueError("locked")
    except Exception:
        add("corrupt", "error")
        return _pack(F.items, {"pages": 0}, t0, corrupt=True)

    fact = {"pages": doc.page_count, "page_sizes_mm": [], "fonts": [], "min_dpi": None,
            "images": 0, "colorspaces": set(), "spot_colors": []}

    # ---- whole file: special colours, transparency, overprint, gradients, form streams
    spot_names, has_trans, has_op, has_shading = set(), False, False, False
    form_ev = {}
    scanned = 0
    for x in range(1, doc.xref_length()):
        try: obj = doc.xref_object(x, compressed=False)
        except Exception: continue
        if "/Separation" in obj:
            for m in re.findall(r"/Separation\s*/([^\s/\]\[]+)", obj):
                if m not in ("All", "None"): spot_names.add(m.replace("#20", " "))
        if "/ExtGState" in obj or "/Type/ExtGState" in obj.replace(" ", ""):
            # check each /ca (fill alpha) and /CA (stroke alpha) value on its own -- an ExtGState
            # dict very commonly sets one to a real fraction (e.g. a semi-transparent fill) while
            # leaving the other at its default of 1 (fully-opaque stroke); scanning the whole
            # object text for "is there a 1 ANYWHERE" would wrongly cancel out the real fraction
            for av in re.finditer(r"/(?:ca|CA)\s+([\d.]+)", obj):
                try:
                    if float(av.group(1)) < 0.999: has_trans = True; break
                except ValueError: pass
            if re.search(r"/(OP|op)\s+true", obj): has_op = True
        if re.search(r"/SMask\s+\d+\s+0\s+R", obj): has_trans = True
        if "/ShadingType" in obj: has_shading = True
        if "/Subtype/Form" in obj.replace(" ", "").replace("\n", "") and scanned < 5 * STREAM_LIMIT:
            try:
                data = doc.xref_stream(x) or b""
                scanned += len(data)
                for k, v in scan_stream(data, _gs_map(doc, x)).items():
                    form_ev[k] = form_ev.get(k, False) or v
            except Exception: pass
    fact["spot_colors"] = sorted(spot_names)
    for n in sorted(spot_names):
        if o["shape_cut"] and re.search(r"cut|die|kiss|crease|perf", n, re.I): continue   # cutting line layer
        add("spot_color", "error", v=n)
    if has_trans: add("transparency", "warning", key="t")
    if has_op: add("overprint", "confirm", key="o")
    if has_shading or form_ev.get("shading"): add("not_bitmap_gradient", "error", key="g")
    if form_ev.get("white_op"): add("white_overprint", "error", key="wo")
    if form_ev.get("rgb"): add("rgb_color", "error", v="vector/text", key="rgbform")
    if form_ev.get("mix_text"): add("mix_black", "warning", v="text", key="mt")
    if form_ev.get("mix_line"): add("mix_black", "warning", v="line", key="ml")
    if form_ev.get("reg_fill"): add("registration_black", "error", key="rb")

    fonts_seen, dark_done, dark_pos_done, page_nums, first_size = set(), set(), set(), {}, None
    for pno, page in enumerate(doc, start=1):
        full = page.rect
        trim, src, size_ok = _trim(doc, page, o)
        w, h = mm(trim.width), mm(trim.height)
        fact["page_sizes_mm"].append([round(w, 1), round(h, 1)])
        try: drs = page.get_drawings()
        except Exception: drs = []
        try: blocks = page.get_text("dict")["blocks"]
        except Exception: blocks = []
        marks = _marks(drs, trim)

        # 28: all pages the same size
        fs = sorted([round(mm(full.width)), round(mm(full.height))])
        if first_size is None: first_size = fs
        elif abs(fs[0] - first_size[0]) > 1 or abs(fs[1] - first_size[1]) > 1:
            add("page_size_mixed", "error", pno, v=f"{pno} ({mm(full.width):.0f}x{mm(full.height):.0f} mm)",
                e=f"{first_size[0]}x{first_size[1]} mm", key="psz")

        # 2: size vs selected size
        if o["expected_mm"] and not sheet and not size_ok:
            ew, eh = o["expected_mm"]
            add("size_mismatch", "error", pno, v=f"{w:.0f}x{h:.0f} mm", e=f"{ew:.0f}x{eh:.0f} mm")

        # 18: too many loose vector elements
        if len(drs) > o["max_paths"]:
            add("not_bitmap_many", "error", pno, v=str(len(drs)), key="many")

        # QR/barcode present -- can't guarantee a printed copy will scan, always ask for a scan test
        if pno <= QR_BARCODE_PAGES:
            try:
                for label, size_mm, bb in _scan_codes(page):
                    add("qr_barcode_found", "confirm", pno, bb, v=f"{label} ~{size_mm:.0f} mm",
                        e=f"{o['qr_min_mm']:.0f} mm", key=f"{label}_{round(size_mm)}_{round(bb.x0)}")
            except Exception: pass

        # drawing commands of the page
        try: ev = scan_stream(page.read_contents(), _gs_map(doc, page.xref))
        except Exception: ev = {}
        if ev.get("shading"): add("not_bitmap_gradient", "error", key="g")
        if ev.get("white_op"): add("white_overprint", "error", pno, key="wo")
        if ev.get("mix_text"): add("mix_black", "warning", pno, v="text", key="mt")
        if ev.get("mix_line"): add("mix_black", "warning", pno, v="line", key="ml")
        if ev.get("reg_fill") or (ev.get("reg_stroke") and not marks and not (sheet and _sheet_marks(drs))):
            add("registration_black", "error", pno, key="rb")
        if ev.get("rgb"):
            rgb_bb = None
            for d in drs:
                f = d.get("fill") or d.get("color")
                if f and len(f) == 3 and not (abs(f[0]-f[1]) < 0.01 and abs(f[1]-f[2]) < 0.01):
                    r = fitz.Rect(d["rect"])
                    if r.width > 1 and r.height > 1 and r.get_area() < 0.85 * full.get_area() and (rgb_bb is None or r.get_area() > rgb_bb.get_area()):
                        rgb_bb = r
            add("rgb_color", "error", pno, rgb_bb, "vector/text", key="rgbv")

        # 9: fonts
        used_fonts = {sp["font"].split("+")[-1] for blk in blocks for ln in blk.get("lines", [])
                      for sp in ln["spans"] if sp["text"].strip()}
        for f in page.get_fonts(full=True):
            name = f[3].split("+")[-1]
            if not any(name == u or name in u or u in name for u in used_fonts): continue
            fonts_seen.add(name)
            if f[1] == "n/a" and f[2] != "Type3":
                add("font_not_embedded", "error", pno, v=name, key=name)

        # ink picture of the page (CMYK)
        A = s = None
        if pno <= PIXEL_PAGES:
            try: A, s = _cmyk(page)
            except Exception: A = None
        T = _crop(A, trim, s) if A is not None else None
        blank = False
        if T is not None and T.size:
            mx = T.max(axis=2)
            blank = int(mx.max()) < 8
            if blank: add("blank_page", "warning", pno, key="blank")

        # 10, 11, 30, 22: text
        safe = pts(o["safe_mm"])
        inner = fitz.Rect(trim.x0+safe, trim.y0+safe, trim.x1-safe, trim.y1-safe)
        nums_here = []
        has_vector_text = False
        for blk in blocks:
            for ln in blk.get("lines", []):
                for sp in ln["spans"]:
                    txt = sp["text"].strip()
                    if not txt: continue
                    has_vector_text = True
                    r = fitz.Rect(sp["bbox"])
                    if sp["size"] < o["min_text_pt"]:
                        add("small_text", "warning", pno, r, f"{sp['size']:.1f} pt", f"{o['min_text_pt']:.0f} pt", key=round(r.x0))
                    elif sp["size"] < o["min_text_pt"] + 3 and _THIN_FONT.search(sp["font"].split("+")[-1]):
                        add("thin_font_small", "warning", pno, r, f"{sp['size']:.1f} pt ({sp['font'].split('+')[-1]})",
                            f"{o['min_text_pt']:.0f} pt", key=round(r.x0))
                    if not sheet and r.intersects(trim) and not inner.contains(r):
                        d = min(r.x0-trim.x0, r.y0-trim.y0, trim.x1-r.x1, trim.y1-r.y1)
                        add("safe_margin", "error", pno, r, f"{max(mm(d),0):.1f} mm", f"{o['safe_mm']:.0f} mm", key=round(r.x0)*1000+round(r.y0))
                    if sp.get("color") == 0xFFFFFF and sp["size"] < o["white_text_pt"] and A is not None:
                        bg = _crop(A, r + (-1, -1, 1, 1), s)
                        if bg.size and float(_darkness(bg).mean()) > 115:
                            add("white_small_text", "warning", pno, r, f"{sp['size']:.1f} pt", f"{o['white_text_pt']:.0f} pt", key=round(r.x0)*1000+round(r.y0))
                    m = re.fullmatch(r"(?:page\s*)?[-–|\s]*(\d{1,4})[-–|\s]*", txt, re.I)
                    if m and (r.y1 < full.y0 + 0.13 * full.height or r.y0 > full.y1 - 0.13 * full.height):
                        nums_here.append(int(m.group(1)))
        page_nums[pno] = nums_here

        # 12, 5, 13: images
        try:
            img_infos, huge = list(page.get_image_info(xrefs=True)), False
        except Exception:
            img_infos, huge = _huge_image_fallback(doc, page), True
        scan_like = False
        for info in img_infos:
            fact["images"] += 1
            bb = fitz.Rect(info["bbox"])
            if bb.width < 1 or bb.height < 1: continue
            if (bb & trim).get_area() >= 0.8 * trim.get_area(): scan_like = True
            # 11: safe margin -- a photo/logo placed close to the cutting edge, not a full-bleed background
            if (not sheet and bb.get_area() < 0.85 * trim.get_area() and bb.intersects(trim) and not inner.contains(bb)):
                d = min(bb.x0-trim.x0, bb.y0-trim.y0, trim.x1-bb.x1, trim.y1-bb.y1)
                add("safe_margin", "error", pno, bb, f"{max(mm(d),0):.1f} mm", f"{o['safe_mm']:.0f} mm",
                    key=round(bb.x0)*1000+round(bb.y0))
            dpi = min(info["width"] / (bb.width/72), info["height"] / (bb.height/72))
            xr = info.get("xref", 0)
            # a gradient/shading fill (no raster data at all) is reported by get_image_info() as a
            # fake "image" with no xref, rasterised internally at exactly 1 pixel per PDF point --
            # which always computes to dpi == 72.000 regardless of its actual size. A real embedded
            # image landing on that exact value is not a realistic coincidence, so this is how we
            # tell a vector gradient apart from an actual low-res photo -- without this check, every
            # gradient in a design was wrongly getting "72 dpi, will print blurry" AND "RGB image,
            # needs CMYK" on top of the correct not_bitmap_gradient finding it already gets elsewhere.
            if xr == 0 and abs(dpi - 72.0) < 0.01: continue
            fact["min_dpi"] = dpi if fact["min_dpi"] is None else min(fact["min_dpi"], dpi)
            pos = f"{xr}_{round(bb.x0)}_{round(bb.y0)}"   # same image reused at a different spot is a separate problem
            if dpi < o["min_dpi_err"]:
                add("low_dpi", "error", pno, bb, f"{dpi:.0f} dpi", f"{o['min_dpi_warn']} dpi", key=pos)
            elif dpi < o["min_dpi_warn"] - 1:
                add("low_dpi", "warning", pno, bb, f"{dpi:.0f} dpi", f"{o['min_dpi_warn']} dpi", key=pos)
            if info.get("huge"): continue   # too large to decode: dpi is checked, colour/darkness are not
            cs_name = info.get("cs-name") or ""
            fact["colorspaces"].add(cs_name or "?")
            if info.get("colorspace", 3) == 3:
                add("rgb_color", "error", pno, bb, "image", key=f"img{xr}_{round(bb.x0)}_{round(bb.y0)}")
            pos_key = (pno, round(bb.x0), round(bb.y0), round(bb.x1), round(bb.y1))
            if xr and xr not in dark_done and pos_key not in dark_pos_done and len(dark_done) < 8:
                dark_done.add(xr)
                try:
                    pil = _pdf_image_pil(doc, xr)
                    dk = _is_dark_photo(pil) if pil else None
                    if dk is not None:
                        # several images can be stacked at the exact same spot (layered design) —
                        # only the first dark one found there is reported, so it isn't repeated.
                        dark_pos_done.add(pos_key)
                        add("dark_image", "warning", pno, bb, _pct(dk*100), key=f"dark{xr}")
                except Exception: pass
        if huge and img_infos:
            add("huge_image_skip", "confirm", pno, key="huge")
        # scanned/flattened page: no real (vector) text at all, just one big picture covering it —
        # any text inside that picture can't be measured, so just a soft heads-up, not an error
        if scan_like and not has_vector_text and not blank:
            add("scanned_maybe_blurry", "confirm", pno, key="scan")

        # 11: safe margin (vector shapes/logos) -- cluster touching/overlapping pieces first, so one
        # multi-path logo near the edge gives ONE finding instead of one per path fragment
        if not sheet:
            min_elem = pts(2.0)   # ignore tiny path fragments/anti-alias noise below 2mm
            cand = [fitz.Rect(d["rect"]) for d in drs
                    if fitz.Rect(d["rect"]).width >= min_elem and fitz.Rect(d["rect"]).height >= min_elem
                    and fitz.Rect(d["rect"]).get_area() < 0.85 * trim.get_area()]
            pad = pts(3.0)
            clusters, changed = cand, True
            while changed and len(clusters) > 1:
                changed = False
                out, used = [], [False] * len(clusters)
                for i in range(len(clusters)):
                    if used[i]: continue
                    cur = fitz.Rect(clusters[i]); used[i] = True
                    for j in range(i + 1, len(clusters)):
                        if used[j]: continue
                        test = fitz.Rect(cur.x0 - pad, cur.y0 - pad, cur.x1 + pad, cur.y1 + pad)
                        if test.intersects(clusters[j]):
                            cur |= clusters[j]; used[j] = True; changed = True
                    out.append(cur)
                clusters = out
            for r in clusters:
                if r.get_area() < 0.85 * trim.get_area() and r.intersects(trim) and not inner.contains(r):
                    dd = min(r.x0-trim.x0, r.y0-trim.y0, trim.x1-r.x1, trim.y1-r.y1)
                    add("safe_margin", "error", pno, r, f"{max(mm(dd),0):.1f} mm", f"{o['safe_mm']:.0f} mm",
                        key=round(r.x0)*1000+round(r.y0))

        # 33: alignment / layout design-quality -- do things line up the way a professional
        # design would (row-align across two columns, left-edge/column align in a stacked block,
        # icon-to-label align, even spacing between stacked rows, centered elements actually
        # centered). All Warning-only: this is a design-quality nudge, not a print defect.
        if not sheet and not blank:
            lines = _text_lines(blocks)
            if lines:
                stacks = _stacks(lines)
                icons = _icon_candidates(drs, img_infos, trim)
                for ic, ln in _icon_text_pairs(icons, lines):
                    dy = mm(abs((ic.y0+ic.y1)/2 - (ln.y0+ln.y1)/2))
                    if ALIGN_TOL_MM < dy <= ALIGN_NEARMISS_MM:
                        r = ic | ln
                        add("icon_text_misaligned", "warning", pno, r, f"{dy:.1f} mm", f"{ALIGN_TOL_MM} mm",
                            key=round(r.x0)*1000+round(r.y0))
                for la, lb, dy in _row_align_pairs(lines):
                    if ALIGN_TOL_MM < dy <= ALIGN_NEARMISS_MM:
                        r = la | lb
                        add("row_misaligned", "warning", pno, r, f"{dy:.1f} mm", f"{ALIGN_TOL_MM} mm",
                            key=round(r.x0)*1000+round(r.y0))
                for stack in stacks:
                    if len(stack) >= 3 and max(r.width for r in stack) < 0.6 * trim.width:
                        x0s = [r.x0 for r in stack]
                        spread = mm(max(x0s) - min(x0s))
                        if ALIGN_TOL_MM < spread <= ALIGN_NEARMISS_MM:
                            med = sorted(x0s)[len(x0s)//2]
                            worst = max(stack, key=lambda r: abs(r.x0 - med))
                            add("column_misaligned", "warning", pno, worst, f"{spread:.1f} mm", f"{ALIGN_TOL_MM} mm",
                                key=round(worst.x0)*1000+round(worst.y0))
                        gaps = [mm(stack[i+1].y0 - stack[i].y1) for i in range(len(stack)-1)]
                        gaps = [g for g in gaps if g >= 0]
                        if len(gaps) >= 2:
                            mx_, mn_ = max(gaps), min(gaps)
                            if mn_ > 0 and mx_ - mn_ > 1.0 and mx_ > 1.4 * mn_:
                                r = stack[0] | stack[-1]
                                add("uneven_spacing", "warning", pno, r, f"{mn_:.1f}-{mx_:.1f} mm", "",
                                    key=round(r.x0)*1000+round(r.y0))
                    # off-centre: a standalone title/logo or a whole stacked block that was
                    # probably meant to sit centered (any size group, not just 3+ line stacks).
                    # A minimum width excludes incidental small running elements (a page number,
                    # a folio, a lone bullet) that happen to sit near the middle but were never
                    # meant to be a "centered design element" in the business-card/letterhead sense.
                    r = stack[0]
                    for ln2 in stack[1:]: r |= ln2
                    if mm(r.width) >= 10 and r.width < 0.7 * trim.width:
                        ml, mr = mm(r.x0 - trim.x0), mm(trim.x1 - r.x1)
                        if ml > 2 and mr > 2:
                            diff = abs(ml - mr)
                            if ALIGN_TOL_MM < diff <= 8.0 and max(ml, mr) / min(ml, mr) <= 2.5:
                                add("off_center", "warning", pno, r, f"{diff:.1f} mm", f"{ALIGN_TOL_MM} mm",
                                    key=round(r.x0)*1000+round(r.y0))

        # 14: thin lines   29: border close to the cutting edge
        for d in drs:
            r = fitz.Rect(d["rect"])
            w_ = d.get("width")
            if "s" not in (d.get("type") or ""): continue
            if d.get("stroke_opacity", 1) != 0 and w_ is not None and w_ < o["min_line_pt"]:
                add("hairline", "warning", pno, r, f"{w_:.2f} pt", f"{o['min_line_pt']} pt", key=round(r.x0)*1000+round(r.y0))
            if (not sheet and len(d.get("items", [])) <= 8 and trim.contains(r)
                    and r.width >= 0.75 * trim.width and r.height >= 0.75 * trim.height):
                dist = mm(min(r.x0-trim.x0, r.y0-trim.y0, trim.x1-r.x1, trim.y1-r.y1))
                if 0.3 <= dist < o["safe_mm"] - 0.2:
                    add("border_near_edge", "warning", pno, r, f"{dist:.1f} mm", f"{o['safe_mm']:.0f} mm", key="border")

        # 20 / 4: cutting marks
        if sheet:
            if not _sheet_marks(drs) and not blank: add("sheet_marks_missing", "error", pno, key="sm")
        elif src == "inferred" and not marks and not blank:
            add("crop_marks", "confirm", pno, key="c")

        # 21: straight-knife cutting needs a complete, aligned row/column grid of same-size items
        if sheet and not blank:
            islands = _item_islands(drs, img_infos, blocks, trim)
            if len(islands) >= 2:
                is_grid, same_size, rows, cols = _grid_check(islands, pts(2.0))
                if not is_grid:
                    add("sheet_not_grid", "warning", pno, v=str(len(islands)), key="grid")
                elif not same_size:
                    add("sheet_mixed_sizes", "warning", pno, v=str(len(islands)), key="mix")

        if T is None or not T.size or blank: continue
        H_, W_ = T.shape[:2]
        C, M_, Y, K = (T[:, :, i].astype(np.int16) for i in range(4))
        inked = mx > 20
        # RGB areas get colour-converted by the renderer when we rasterise to CMYK, which can
        # show misleading ink numbers there -- exclude just those pixels from ink checks below
        # (not the whole page: a photo being RGB elsewhere shouldn't hide real over-ink in the
        # rest of a genuinely-CMYK design).
        rgb_findings = [f for f in F.items if f["code"] == "rgb_color" and f["page"] == pno]
        rgb_unlocalised = any(f["bbox"] is None for f in rgb_findings)
        excl = None
        if rgb_findings and not rgb_unlocalised:
            excl = np.zeros((H_, W_), dtype=bool)
            ox, oy = int(round(trim.x0 * s)), int(round(trim.y0 * s))
            for f in rgb_findings:
                bx0, by0, bx1, by1 = f["bbox"]
                px0 = max(0, int(round(bx0 * s)) - ox); py0 = max(0, int(round(by0 * s)) - oy)
                px1 = min(W_, int(round(bx1 * s)) - ox); py1 = min(H_, int(round(by1 * s)) - oy)
                if px1 > px0 and py1 > py0: excl[py0:py1, px0:px1] = True

        # 3 / 19: bleed
        if not sheet:
            need = max(o["cut_overlap_mm"], o["bleed_mm"]) if o["shape_cut"] else o["bleed_mm"]
            code = "cut_overlap" if o["shape_cut"] else "bleed_missing"
            b = mm(min(trim.x0-full.x0, trim.y0-full.y0, full.x1-trim.x1, full.y1-trim.y1))
            ip = max(2, int(pts(1.5) * s))
            inside = {"l": inked[:, :ip], "r": inked[:, -ip:], "t": inked[:ip, :], "b": inked[-ip:, :]}
            touch = [k for k, v in inside.items() if v.size and float(v.mean()) >= 0.05]
            if touch:
                if src == "none":
                    add("bleed_unknown", "confirm", pno, e=f"{need:.0f} mm", key="bu")
                elif b < need - 0.2:
                    add(code, "error", pno, v=f"{max(b,0):.1f} mm", e=f"{need:.0f} mm", key="b")
                else:
                    op = max(2, int(pts(need) * s)); fmx = A.max(axis=2) > 20
                    x0, y0 = int(round(trim.x0*s)), int(round(trim.y0*s)); x1, y1 = x0 + W_, y0 + H_
                    outside = {"l": fmx[y0:y1, max(0, x0-op):x0], "r": fmx[y0:y1, x1:x1+op],
                               "t": fmx[max(0, y0-op):y0, x0:x1], "b": fmx[y1:y1+op, x0:x1]}
                    for k in touch:
                        ov = outside[k]
                        if not ov.size or float(ov.mean()) < 0.5 * float(inside[k].mean()):
                            add(code, "error", pno, v="0 mm", e=f"{need:.0f} mm", key="b"); break

        # 7: registration colour inside the design
        if int(((T.min(axis=2)) >= 250).sum()) >= 12: add("registration_black", "error", pno, key="rb")

        if not rgb_unlocalised:
            keep = ~excl if excl is not None else None
            # 8: total ink
            tot = (C + M_ + Y + K) / 2.55
            tot_m = tot[keep] if keep is not None else tot
            if tot_m.size and float((tot_m > o["max_tac"] + 5).mean()) >= 0.005:
                add("tac_high", "warning", pno, v=_pct(float(np.percentile(tot_m, 99.9))), e=_pct(o["max_tac"]), key="tac")
            # 6: black above the limit inside mixed colours / photos
            kcond = (K > o["k_limit"] * 2.55 + 2) & (np.maximum(np.maximum(C, M_), Y) > 25)
            kcond_m = kcond[keep] if keep is not None else kcond
            share = float(kcond_m.mean()) if kcond_m.size else 0.0
            if share >= 0.02: add("k_heavy", "confirm", pno, v=_pct(share*100), e=_pct(o["k_limit"]), key="kh")
            # 23: single-colour job
            if o["single_colour"]:
                used = [n for n, ch in zip("CMYK", (C, M_, Y, K))
                        if float(((ch[keep] if keep is not None else ch) > 20).mean()) > 0.002]
                if len(used) > 1: add("single_colour_mix", "error", pno, v="+".join(used), key="sc")

        dk = _darkness(T)
        ink = dk[mx > 8]
        # 25: design very light
        if ink.size >= 0.003 * mx.size and int((dk > 31).sum()) < max(20, 0.0002 * mx.size):
            add("light_design", "warning", pno, v=_pct(float(np.percentile(ink, 99)) / 2.55), key="light")
        # 26: watermark in the middle too dark
        try:
            cy0, cy1, cx0, cx1 = int(H_*0.2), int(H_*0.8), int(W_*0.2), int(W_*0.8)
            Cn = dk[cy0:cy1, cx0:cx1]; n = 6
            hh, ww = (Cn.shape[0] // n) * n, (Cn.shape[1] // n) * n
            if hh and ww:
                Bk = Cn[:hh, :ww].reshape(hh // n, n, ww // n, n)
                mean, std = Bk.mean(axis=(1, 3)), Bk.std(axis=(1, 3))
                flat = (mean >= 8) & (mean < 140) & (std < 10)
                if (float(flat.mean()) >= 0.08 and float((mx < 8).mean()) >= 0.45
                        and float((Cn >= 178).mean()) <= 0.08):
                    wd = float(mean[flat].mean()) / 2.55
                    if wd > 20:
                        add("dark_watermark", "warning", pno, fitz.Rect(trim.x0 + trim.width*0.2, trim.y0 + trim.height*0.2,
                            trim.x0 + trim.width*0.8, trim.y0 + trim.height*0.8), _pct(wd), key="wm")
        except Exception: pass

    # 22: page number sequence   32: book pages
    n = doc.page_count
    if n >= 4:
        withn = [p for p in range(1, n + 1) if page_nums.get(p)]
        if len(withn) >= max(3, n // 2):
            for p in range(1, n):
                a, b = page_nums.get(p), page_nums.get(p + 1)
                if a and b and not any(y == x + 1 for x in a for y in b):
                    add("page_seq_break", "confirm", p + 1, v=f"page {p}: {a[0]}, page {p+1}: {b[0]}", key="seq"); break
        elif not withn:
            add("page_seq_none", "confirm", v=str(n), key="seqn")
    if n >= 8 and n % 4: add("pages_not_x4", "confirm", v=str(n), key="x4")

    fact["fonts"] = sorted(fonts_seen)
    fact["colorspaces"] = sorted(fact["colorspaces"])
    fact["min_dpi"] = round(fact["min_dpi"]) if fact["min_dpi"] else None
    return _pack(F.items, fact, t0)


# ---------------------------------------------------------------- photos
def _dark_stats(im):
    g = im.convert("L"); g.thumbnail((200, 200))
    px = np.asarray(g, dtype=np.float32)
    return float(px.mean()), float(px.std()), float((px < 30).mean())

def _is_dark_photo(im):
    mean, std, dark = _dark_stats(im)
    if std < 3: return None  # flat fill / logo, not a photo
    if (mean < 80 and dark >= 0.30) or dark >= 0.45: return dark
    return None

_CM_DO = re.compile(rb"(?:([-\d.]+(?:\s+[-\d.]+){5})\s+cm\b)|(/[^\s/()<>\[\]]+)\s+Do\b|(\bq\b)|(\bQ\b)")

def _xobject_map(doc, xref):
    out = {}
    try:
        typ, val = doc.xref_get_key(xref, "Resources/XObject")
        if typ == "xref": val = doc.xref_object(int(val.split()[0]), compressed=True)
        elif typ != "dict": return out
    except Exception:
        return out
    for nm, x in re.findall(r"/([^\s/<>\[\]]+)\s+(\d+)\s+0\s+R", val):
        out[nm] = int(x)
    return out

def _huge_image_fallback(doc, page):
    """Used only when PyMuPDF cannot decode an image on this page at all because it is very
    large (a real, legitimate high-resolution image can still hit this). Gets the width/height
    straight from the PDF's own object (no decode needed, so this always works) and the
    on-page position by walking the page's own drawing commands (cm/Do), so the resolution
    (dpi) can still be checked even though the picture itself cannot be opened."""
    out = []
    try:
        xobj = _xobject_map(doc, page.xref)
        by_xref = {}
        for info in page.get_images(full=True):
            xref, smask, w, h, bpc, cs, altcs, name, filt, ref = info
            by_xref[xref] = (w, h, cs)
        H = page.mediabox.height
        stack, ctm = [], fitz.Matrix(1, 0, 0, 1, 0, 0)
        for m in _CM_DO.finditer(page.read_contents()):
            cm, do, q, qq = m.groups()
            if q: stack.append(ctm)
            elif qq:
                if stack: ctm = stack.pop()
            elif cm:
                ctm = fitz.Matrix(*(float(x) for x in cm.split())) * ctm
            elif do:
                name = do[1:].decode("latin-1")
                xref = xobj.get(name)
                if xref not in by_xref: continue
                r = fitz.Rect(0, 0, 1, 1) * ctm
                x0, x1 = sorted((r.x0, r.x1)); y0, y1 = sorted((r.y0, r.y1))
                rr = fitz.Rect(x0, H - y1, x1, H - y0)      # PDF space (bottom-up) -> page.rect space (top-down)
                if page.rotation: rr = rr * page.rotation_matrix; rr.normalize()
                rr = rr & page.rect
                if rr.is_empty: continue
                w, h, cs = by_xref[xref]
                out.append({"xref": xref, "width": w, "height": h, "bbox": rr,
                            "cs-name": cs, "colorspace": None, "huge": True})
    except Exception:
        pass
    return out

def _pdf_image_pil(doc, xref):
    from PIL import Image
    pix = fitz.Pixmap(doc, xref)
    if pix.width * pix.height > 25_000_000: return None
    if pix.colorspace is None or pix.colorspace.n != 3 or pix.alpha:
        pix = fitz.Pixmap(fitz.csRGB, pix) if not pix.alpha else fitz.Pixmap(fitz.csRGB, fitz.Pixmap(pix, 0))
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def _severity_label(sev, idx):
    """the number/letter shown on the marker dot and in the problem list, per owner's scheme
    (22 Nov): Errors get plain numbers (1,2,3...), Warnings get letters (A,B,C...,Z,AA,AB...,
    Excel-column style so it never runs out), Confirms get no label at all (empty dot)."""
    if sev == "error":
        return str(idx)
    if sev == "warning":
        s = ""
        n = idx
        while n > 0:
            n, r = divmod(n - 1, 26)
            s = chr(65 + r) + s
        return s
    return ""   # confirm -- intentionally blank, per owner's design


def _pack(findings, fact, t0, corrupt=False):
    BIG = 10**9
    def sort_key(f):
        # page order first, then top-to-bottom / left-to-right on that page — so the numbers
        # read in the same order as scanning the preview image. Findings with no exact page/spot
        # (whole-document or whole-page issues) sort to the end of their group.
        page = f["page"] if f["page"] is not None else BIG
        bb = f.get("bbox")
        y0 = bb[1] if bb else BIG
        x0 = bb[0] if bb else BIG
        return (page, y0, x0)
    findings.sort(key=sort_key)
    sev_counters = {"error": 0, "warning": 0, "confirm": 0}
    for i, f in enumerate(findings, start=1):
        f["no"] = i          # fixed 1..N label across ALL findings -- kept for internal/jump-link use.
        sev_counters[f["severity"]] += 1
        f["label"] = _severity_label(f["severity"], sev_counters[f["severity"]])   # what the UI shows on the dot: Error "1,2,3", Warning "A,B,C", Confirm "" (blank)
    e = sum(f["severity"] == "error" for f in findings)
    w = sum(f["severity"] == "warning" for f in findings)
    c = sum(f["severity"] == "confirm" for f in findings)
    result = "error" if e else ("warning" if w else "ok")   # confirm items do not change the result
    ms = int((time.time()-t0)*1000)
    return {"result": result, "corrupt": corrupt, "processing_ms": ms, "fact_sheet": fact,
            "report": {"version": 2, "summary": {"errors": e, "warnings": w, "confirms": c, "result": result}, "findings": findings}}


# ---------------------------------------------------------------- JPG / PNG
def analyze_image(path, profile="digital_toner", opts=None):
    from PIL import Image
    t0 = time.time()
    o = dict(DEFAULTS); o.update({k: v for k, v in (opts or {}).items() if v is not None})
    F = Findings()
    def add(code, sev, v="", e=""): F.add(code, sev, 1, None, v, e)
    try:
        im = Image.open(path); im.load()
    except Exception:
        add("corrupt", "error")
        return _pack(F.items, {"pages": 0}, t0, corrupt=True)
    px_w, px_h = im.size
    fact = {"pages": 1, "pixels": [px_w, px_h], "mode": im.mode, "page_sizes_mm": [], "fonts": [], "images": 1}
    ex = o["expected_mm"]
    if ex:
        ew, eh = ex
        if (px_w > px_h) != (ew > eh): ew, eh = eh, ew
        dpi = min(px_w / (ew / 25.4), px_h / (eh / 25.4))
        fact["page_sizes_mm"] = [[ew, eh]]
        fact["min_dpi"] = round(dpi)
        if abs(px_w / px_h - ew / eh) / (ew / eh) > 0.03:
            add("size_mismatch", "error", f"{px_w}x{px_h} px", f"{ew:.0f}x{eh:.0f} mm")
        if dpi < o["min_dpi_err"]: add("low_dpi", "error", f"{dpi:.0f} dpi", f"{o['min_dpi_warn']} dpi")
        elif dpi < o["min_dpi_warn"] - 1: add("low_dpi", "warning", f"{dpi:.0f} dpi", f"{o['min_dpi_warn']} dpi")
    if im.mode not in ("CMYK", "L", "LA", "1"):
        add("rgb_color", "error", "image")
    if _zbar_decode is not None:
        try:
            for z in _zbar_decode(im, symbols=_ZBAR_SYMBOLS):
                label = "QR Code" if z.type == "QRCODE" else "Barcode"
                # mm size only knowable if the client told us the printed size (size/preset selected)
                v = f"{label} ~{max(z.rect.width, z.rect.height) / dpi * 25.4:.0f} mm" if ex else label
                add("qr_barcode_found", "confirm", v, f"{o['qr_min_mm']:.0f} mm")
        except Exception: pass
    try:
        small = im.copy(); small.thumbnail((500, 500))
        g = np.asarray(small.convert("L"), dtype=np.float32)
        inked = g < 235
        ip = max(2, int(min(g.shape) * 0.012))
        edges = [inked[:, :ip], inked[:, -ip:], inked[:ip, :], inked[-ip:, :]]
        if any(float(v.mean()) >= 0.05 for v in edges):
            add("bleed_unknown", "confirm", "", f"{o['bleed_mm']:.0f} mm")  # design touches the edge of the picture
        if not inked.any():
            add("blank_page", "warning")
        elif inked.mean() >= 0.003 and float(np.percentile(g[inked], 5)) > 224:
            add("light_design", "warning", _pct((255 - float(np.percentile(g[inked], 5))) / 2.55))
        if small.mode == "CMYK":
            a = np.asarray(small).astype(np.int16)
            C, M_, Y, K = (a[:, :, i] for i in range(4))
            tot = (C + M_ + Y + K) / 2.55
            if float((tot > o["max_tac"] + 5).mean()) >= 0.005:
                add("tac_high", "warning", _pct(float(np.percentile(tot, 99.9))), _pct(o["max_tac"]))
            share = float(((K > o["k_limit"] * 2.55 + 2) & (np.maximum(np.maximum(C, M_), Y) > 25)).mean())
            if share >= 0.02: add("k_heavy", "confirm", _pct(share*100), _pct(o["k_limit"]))
            if o["single_colour"]:
                used = [n for n, ch in zip("CMYK", (C, M_, Y, K)) if float((ch > 20).mean()) > 0.002]
                if len(used) > 1: add("single_colour_mix", "error", "+".join(used))
    except Exception: pass
    try:
        dk = _is_dark_photo(im)
        if dk is not None: add("dark_image", "warning", _pct(dk*100))
    except Exception: pass
    return _pack(F.items, fact, t0)
