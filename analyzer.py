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

PT_MM = 25.4 / 72.0
def mm(pt): return pt * PT_MM
def pts(m): return m / PT_MM

DEFAULTS = {"bleed_mm": 3.0, "safe_mm": 5.0, "min_dpi_warn": 300, "min_dpi_err": 150,
            "min_text_pt": 5.0, "min_line_pt": 0.25, "max_tac": 300, "expected_mm": None,
            "mode": "single",          # "single" or "sheet" (mixed-job sheet)
            "shape_cut": False,        # shape / die cutting job -> needs cut_overlap_mm
            "single_colour": False,    # single-colour job -> mixed colours are an error
            "k_limit": 40,             # % black inside mixed colours / photos -> confirm
            "cut_overlap_mm": 5.0, "max_paths": 8000, "white_text_pt": 8.0}
CAP = 12            # max findings of one kind in a report
PIXEL_PAGES = 60    # pages that get the ink (pixel) checks
STREAM_LIMIT = 8_000_000


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
            if re.search(r"/(ca|CA)\s+0?\.\d+", obj) and not re.search(r"/(ca|CA)\s+1(\.0+)?\b", obj): has_trans = True
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

    fonts_seen, dark_done, page_nums, first_size = set(), set(), {}, None
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
        for blk in blocks:
            for ln in blk.get("lines", []):
                for sp in ln["spans"]:
                    txt = sp["text"].strip()
                    if not txt: continue
                    r = fitz.Rect(sp["bbox"])
                    if sp["size"] < o["min_text_pt"]:
                        add("small_text", "warning", pno, r, f"{sp['size']:.1f} pt", f"{o['min_text_pt']:.0f} pt", key=round(r.x0))
                    if not sheet and r.intersects(trim) and not inner.contains(r):
                        d = min(r.x0-trim.x0, r.y0-trim.y0, trim.x1-r.x1, trim.y1-r.y1)
                        add("safe_margin", "warning", pno, r, f"{max(mm(d),0):.1f} mm", f"{o['safe_mm']:.0f} mm", key=round(r.x0)*1000+round(r.y0))
                    if sp.get("color") == 0xFFFFFF and sp["size"] < o["white_text_pt"] and A is not None:
                        bg = _crop(A, r + (-1, -1, 1, 1), s)
                        if bg.size and float(_darkness(bg).mean()) > 115:
                            add("white_small_text", "warning", pno, r, f"{sp['size']:.1f} pt", f"{o['white_text_pt']:.0f} pt", key=round(r.x0)*1000+round(r.y0))
                    m = re.fullmatch(r"(?:page\s*)?[-–|\s]*(\d{1,4})[-–|\s]*", txt, re.I)
                    if m and (r.y1 < full.y0 + 0.13 * full.height or r.y0 > full.y1 - 0.13 * full.height):
                        nums_here.append(int(m.group(1)))
        page_nums[pno] = nums_here

        # 12, 5, 13: images
        for info in page.get_image_info(xrefs=True):
            fact["images"] += 1
            bb = fitz.Rect(info["bbox"])
            if bb.width < 1 or bb.height < 1: continue
            dpi = min(info["width"] / (bb.width/72), info["height"] / (bb.height/72))
            fact["min_dpi"] = dpi if fact["min_dpi"] is None else min(fact["min_dpi"], dpi)
            xr = info.get("xref", 0)
            if dpi < o["min_dpi_err"]:
                add("low_dpi", "error", pno, bb, f"{dpi:.0f} dpi", f"{o['min_dpi_warn']} dpi", key=xr)
            elif dpi < o["min_dpi_warn"] - 1:
                add("low_dpi", "warning", pno, bb, f"{dpi:.0f} dpi", f"{o['min_dpi_warn']} dpi", key=xr)
            cs_name = info.get("cs-name") or ""
            fact["colorspaces"].add(cs_name or "?")
            if cs_name in ("DeviceRGB", "CalRGB", "ICCBased") and info.get("colorspace", 3) == 3:
                add("rgb_color", "error", pno, bb, "image", key=f"img{xr}")
            if xr and xr not in dark_done and len(dark_done) < 8:
                dark_done.add(xr)
                try:
                    pil = _pdf_image_pil(doc, xr)
                    dk = _is_dark_photo(pil) if pil else None
                    if dk is not None: add("dark_image", "warning", pno, bb, _pct(dk*100), key=f"dark{xr}")
                except Exception: pass

        # 14: thin lines   29: border close to the cutting edge
        for d in drs:
            w_ = d.get("width")
            if "s" not in (d.get("type") or ""): continue
            r = fitz.Rect(d["rect"])
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

        if T is None or not T.size or blank: continue
        H_, W_ = T.shape[:2]
        C, M_, Y, K = (T[:, :, i].astype(np.int16) for i in range(4))
        inked = mx > 20
        has_rgb = F.has("rgb_color", pno)

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
                    add("bleed_unknown", "confirm", pno, key="bu")
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

        if not has_rgb:
            # 8: total ink
            tot = (C + M_ + Y + K) / 2.55
            if float((tot > o["max_tac"] + 5).mean()) >= 0.005:
                add("tac_high", "warning", pno, v=_pct(float(np.percentile(tot, 99.9))), e=_pct(o["max_tac"]), key="tac")
            # 6: black above the limit inside mixed colours / photos
            share = float(((K > o["k_limit"] * 2.55 + 2) & (np.maximum(np.maximum(C, M_), Y) > 25)).mean())
            if share >= 0.02: add("k_heavy", "confirm", pno, v=_pct(share*100), e=_pct(o["k_limit"]), key="kh")
            # 23: single-colour job
            if o["single_colour"]:
                used = [n for n, ch in zip("CMYK", (C, M_, Y, K)) if float((ch > 20).mean()) > 0.002]
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

def _pdf_image_pil(doc, xref):
    from PIL import Image
    pix = fitz.Pixmap(doc, xref)
    if pix.width * pix.height > 25_000_000: return None
    if pix.colorspace is None or pix.colorspace.n != 3 or pix.alpha:
        pix = fitz.Pixmap(fitz.csRGB, pix) if not pix.alpha else fitz.Pixmap(fitz.csRGB, fitz.Pixmap(pix, 0))
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def _pack(findings, fact, t0, corrupt=False):
    order = {"error": 0, "warning": 1, "confirm": 2}
    findings.sort(key=lambda f: (order[f["severity"]], f["page"] or 0))
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
    try:
        small = im.copy(); small.thumbnail((500, 500))
        g = np.asarray(small.convert("L"), dtype=np.float32)
        inked = g < 235
        ip = max(2, int(min(g.shape) * 0.012))
        edges = [inked[:, :ip], inked[:, -ip:], inked[:ip, :], inked[-ip:, :]]
        if any(float(v.mean()) >= 0.05 for v in edges):
            add("bleed_unknown", "confirm")                 # design touches the edge of the picture
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
