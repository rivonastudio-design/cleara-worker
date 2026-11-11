"""Cleara Phase-1 PDF preflight. Uses PyMuPDF only. Unsure => 'confirm', never a false error."""
import re, time
import warnings; warnings.filterwarnings("ignore")
import pymupdf as fitz
from messages import build

PT_MM = 25.4 / 72.0
def mm(pt): return pt * PT_MM

DEFAULTS = {"bleed_mm": 3.0, "safe_mm": 5.0, "min_dpi_warn": 300, "min_dpi_err": 150,
            "min_text_pt": 5.0, "min_line_pt": 0.25, "max_tac": 300, "expected_mm": None}

def analyze(path, profile="offset_coated", opts=None):
    t0 = time.time()
    o = dict(DEFAULTS); o.update(opts or {})
    offset = profile.startswith("offset")
    findings, seen = [], set()

    def add(code, sev, page=None, bbox=None, v="", e="", key=None):
        k = (code, page, key if key is not None else str(v))
        if k in seen: return
        seen.add(k)
        msg, fix = build(code, v, e)
        findings.append({"code": code, "severity": sev, "page": page,
                         "bbox": [round(x, 1) for x in bbox] if bbox else None,
                         "value": str(v), "expected": str(e), "msg": msg, "fix": fix})

    try:
        doc = fitz.open(path)
        if doc.needs_pass or doc.page_count == 0: raise ValueError("locked")
    except Exception:
        add("corrupt", "error")
        return _pack(findings, {"pages": 0}, t0, corrupt=True)

    fact = {"pages": doc.page_count, "page_sizes_mm": [], "fonts": [], "min_dpi": None,
            "images": 0, "colorspaces": set(), "spot_colors": []}
    spot_names = set()

    # document-level: spot colours, overprint, transparency via object scan
    has_trans = has_op = False
    for x in range(1, doc.xref_length()):
        try: obj = doc.xref_object(x, compressed=False)
        except Exception: continue
        if "/Separation" in obj:
            for m in re.findall(r"/Separation\s*/([^\s/\]\[]+)", obj):
                if m not in ("All", "None"): spot_names.add(m.replace("#20", " "))
        if "/Type/ExtGState" in obj.replace(" ", "") or "/ExtGState" in obj:
            if re.search(r"/(ca|CA)\s+0?\.\d+", obj) and not re.search(r"/(ca|CA)\s+1(\.0+)?\b", obj): has_trans = True
            if re.search(r"/(OP|op)\s+true", obj): has_op = True
        if re.search(r"/SMask\s+\d+\s+0\s+R", obj): has_trans = True
    fact["spot_colors"] = sorted(spot_names)
    for n in sorted(spot_names): add("spot_color", "confirm", v=n)
    if has_trans: add("transparency", "warning" if offset else "confirm", key="t")
    if has_op: add("overprint", "confirm", key="o")

    fonts_seen = set()
    for pno, page in enumerate(doc, start=1):
        media = page.mediabox
        trim = page.trimbox if page.trimbox and page.trimbox != media or _has_key(doc, page, "TrimBox") else None
        has_trim = _has_key(doc, page, "TrimBox")
        trim = page.trimbox if has_trim else media
        w, h = mm(trim.width), mm(trim.height)
        fact["page_sizes_mm"].append([round(w, 1), round(h, 1)])

        # size vs expected (preset)
        if o["expected_mm"]:
            ew, eh = o["expected_mm"]
            ok = (abs(w-ew) < 1.0 and abs(h-eh) < 1.0) or (abs(w-eh) < 1.0 and abs(h-ew) < 1.0)
            if not ok: add("size_mismatch", "error", pno, v=f"{w:.0f}x{h:.0f} mm", e=f"{ew:.0f}x{eh:.0f} mm")

        # bleed
        if has_trim:
            b = min(trim.x0-media.x0, trim.y0-media.y0, media.x1-trim.x1, media.y1-trim.y1)
            if mm(b) < o["bleed_mm"] - 0.2:
                add("bleed_missing", "error", pno, v=f"{max(mm(b),0):.1f} mm", e=f"{o['bleed_mm']:.0f} mm", key="b")
            if mm(b) > o["bleed_mm"] + 4 or _marks(page, trim):
                pass
            elif mm(b) >= o["bleed_mm"] - 0.2 and not _marks(page, trim):
                add("crop_marks", "confirm", pno, key="c")
        else:
            add("bleed_unknown", "confirm", pno, key="bu")

        # content-stream colours
        try: cs = page.read_contents().decode("latin-1")
        except Exception: cs = ""
        if re.search(r"(?<![\w/])[\d.\-]+\s+[\d.\-]+\s+[\d.\-]+\s+(rg|RG)\b", cs):
            rgb_bb = None
            try:
                for d in page.get_drawings():
                    f = d.get("fill") or d.get("color")
                    if f and len(f) == 3 and not (abs(f[0]-f[1]) < 0.01 and abs(f[1]-f[2]) < 0.01):
                        r = fitz.Rect(d["rect"])
                        if r.width > 1 and r.height > 1 and r.get_area() < 0.85 * media.get_area() and (rgb_bb is None or r.get_area() > rgb_bb.get_area()):
                            rgb_bb = r
            except Exception:
                rgb_bb = None
            add("rgb_color", "error" if offset else "warning", pno, rgb_bb, "vector/text", key="rgbv")
        tac_max = 0
        for m in re.finditer(r"([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+(k|K)\b", cs):
            c, mg, y, k = (float(m.group(i)) for i in range(1, 5))
            tac_max = max(tac_max, (c+mg+y+k)*100)
            if min(c, mg, y, k) >= 0.99: add("registration_black", "error", pno, v="", key="rb")
        if tac_max > o["max_tac"] + 5 and offset:
            add("tac_high", "warning", pno, v=f"{tac_max:.0f}%", e=f"{o['max_tac']}%", key="tac")

        # fonts
        for f in page.get_fonts(full=True):
            name = f[3].split("+")[-1]
            fonts_seen.add(name)
            if f[1] == "n/a" and f[2] != "Type3":
                base14 = re.match(r"(Helvetica|Times|Courier|Symbol|ZapfDingbats|Arial)", name) is not None
                add("font_not_embedded", "warning" if base14 else "error", pno, v=name, key=name)

        # text: size + safe margin + low-contrast none
        safe = o["safe_mm"] / PT_MM
        inner = fitz.Rect(trim.x0+safe, trim.y0+safe, trim.x1-safe, trim.y1-safe)
        try:
            blocks = page.get_text("dict")["blocks"]
        except Exception: blocks = []
        for blk in blocks:
            for ln in blk.get("lines", []):
                for sp in ln["spans"]:
                    if not sp["text"].strip(): continue
                    r = fitz.Rect(sp["bbox"])
                    if sp["size"] < o["min_text_pt"]:
                        add("small_text", "warning", pno, r, f"{sp['size']:.1f} pt", f"{o['min_text_pt']:.0f} pt", key=round(r.x0))
                    if r.intersects(trim) and not inner.contains(r) and not _outside(r, trim):
                        d = min(r.x0-trim.x0, r.y0-trim.y0, trim.x1-r.x1, trim.y1-r.y1)
                        add("safe_margin", "warning", pno, r, f"{max(mm(d),0):.1f} mm", f"{o['safe_mm']:.0f} mm", key=round(r.x0)*1000+round(r.y0))

        # images
        for info in page.get_image_info(xrefs=True):
            fact["images"] += 1
            bb = fitz.Rect(info["bbox"])
            if bb.width < 1 or bb.height < 1: continue
            dpi = min(info["width"] / (bb.width/72), info["height"] / (bb.height/72))
            fact["min_dpi"] = dpi if fact["min_dpi"] is None else min(fact["min_dpi"], dpi)
            if dpi < o["min_dpi_err"]:
                add("low_dpi", "error", pno, bb, f"{dpi:.0f} dpi", f"{o['min_dpi_warn']} dpi", key=info.get("xref", 0))
            elif dpi < o["min_dpi_warn"] - 1:
                add("low_dpi", "warning", pno, bb, f"{dpi:.0f} dpi", f"{o['min_dpi_warn']} dpi", key=info.get("xref", 0))
            cs_name = info.get("cs-name") or ""
            fact["colorspaces"].add(cs_name or "?")
            if cs_name in ("DeviceRGB", "CalRGB", "ICCBased") and info.get("colorspace", 3) == 3:
                add("rgb_color", "error" if offset else "warning", pno, bb, "image", key=f"img{info.get('xref',0)}")

        # hairlines
        try:
            for d in page.get_drawings():
                w_ = d.get("width")
                if d.get("stroke_opacity", 1) != 0 and w_ is not None and 0 < w_ < o["min_line_pt"] and "s" in d.get("type", ""):
                    add("hairline", "warning", pno, d["rect"], f"{w_:.2f} pt", f"{o['min_line_pt']} pt", key=round(d["rect"].x0)*1000+round(d["rect"].y0))
        except Exception: pass

    fact["fonts"] = sorted(fonts_seen)
    fact["colorspaces"] = sorted(fact["colorspaces"])
    fact["min_dpi"] = round(fact["min_dpi"]) if fact["min_dpi"] else None
    return _pack(findings, fact, t0)

def _has_key(doc, page, key):
    try: return doc.xref_get_key(page.xref, key)[0] != "null"
    except Exception: return False

def _outside(r, trim):  # object fully in bleed area (decorative), not content
    return not r.intersects(trim)

def _marks(page, trim):
    """heuristic: short thin lines outside the trim box = crop marks"""
    n = 0
    try:
        for d in page.get_drawings():
            r = d["rect"]
            if not r.intersects(trim) and max(r.width, r.height) < 40 and min(r.width, r.height) < 1.5: n += 1
    except Exception: return False
    return n >= 4

def _pack(findings, fact, t0, corrupt=False):
    order = {"error": 0, "warning": 1, "confirm": 2}
    findings.sort(key=lambda f: (order[f["severity"]], f["page"] or 0))
    e = sum(f["severity"] == "error" for f in findings)
    w = sum(f["severity"] == "warning" for f in findings)
    c = sum(f["severity"] == "confirm" for f in findings)
    result = "error" if e else ("warning" if (w or c) else "ok")
    ms = int((time.time()-t0)*1000)
    return {"result": result, "corrupt": corrupt, "processing_ms": ms, "fact_sheet": fact,
            "report": {"version": 1, "summary": {"errors": e, "warnings": w, "confirms": c, "result": result}, "findings": findings}}


def analyze_image(path, profile="digital_toner", opts=None):
    """PNG/JPG: effective DPI at the preset size, colour mode, bleed unknown."""
    from PIL import Image
    t0 = time.time()
    o = dict(DEFAULTS); o.update(opts or {})
    findings, seen = [], set()
    def add(code, sev, v="", e=""):
        msg, fix = build(code, v, e)
        findings.append({"code": code, "severity": sev, "page": 1, "bbox": None, "value": str(v),
                         "expected": str(e), "msg": msg, "fix": fix})
    try:
        im = Image.open(path); im.load()
    except Exception:
        add("corrupt", "error")
        return _pack(findings, {"pages": 0}, t0, corrupt=True)
    px_w, px_h = im.size
    fact = {"pages": 1, "pixels": [px_w, px_h], "mode": im.mode, "page_sizes_mm": [], "fonts": [], "images": 1}
    ex = o["expected_mm"]
    if ex:
        ew, eh = ex
        if (px_w > px_h) != (ew > eh): ew, eh = eh, ew
        dpi = min(px_w / (ew / 25.4), px_h / (eh / 25.4))
        fact["page_sizes_mm"] = [[ew, eh]]
        fact["min_dpi"] = round(dpi)
        if dpi < o["min_dpi_err"]: add("low_dpi", "error", f"{dpi:.0f} dpi", f"{o['min_dpi_warn']} dpi")
        elif dpi < o["min_dpi_warn"] - 1: add("low_dpi", "warning", f"{dpi:.0f} dpi", f"{o['min_dpi_warn']} dpi")
        ar_img, ar_exp = px_w / px_h, ew / eh
        if abs(ar_img - ar_exp) / ar_exp > 0.03:
            add("size_mismatch", "warning", f"{px_w}x{px_h} px", f"{ew:.0f}x{eh:.0f} mm")
    else:
        add("bleed_unknown", "confirm")
    if im.mode in ("RGB", "RGBA", "P", "L", "LA"):
        if im.mode != "L": add("rgb_color", "warning" if profile.startswith("offset") else "confirm", "image")
    add("bleed_unknown", "confirm")
    return _pack(findings, fact, t0)
