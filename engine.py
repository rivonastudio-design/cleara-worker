"""Extra layer on top of analyzer.py: spelling (confirm-only) and page previews."""
import io, os, re, time
import warnings; warnings.filterwarnings("ignore")
import pymupdf as fitz
import analyzer
from analyzer import analyze, analyze_image, DEFAULTS
from messages import build, LANGS

SPELL_MSG = {
 "en": ("Possible spelling mistake: '{v}'. Did you mean '{e}'?", "Check the spelling. Ignore if it is a name or brand."),
 "hi": ("संभावित स्पेलिंग गलती: '{v}'। क्या आपका मतलब '{e}' है?", "स्पेलिंग जाँचें। नाम या ब्रांड हो तो अनदेखा करें।"),
 "gu": ("સંભવિત સ્પેલિંગ ભૂલ: '{v}'. શું તમારો મતલબ '{e}' છે?", "સ્પેલિંગ તપાસો. નામ કે બ્રાન્ડ હોય તો અવગણો."),
 "hinglish": ("Spelling galti ho sakti hai: '{v}'. Kya aap '{e}' kehna chahte the?", "Spelling check karo. Naam ya brand ho to ignore karo."),
}
_SPELL = None

def _finding(code, sev, page, bbox, v, e):
    if code == "spelling":
        msg = {l: SPELL_MSG[l][0].format(v=v, e=e) for l in LANGS}
        fix = {l: SPELL_MSG[l][1] for l in LANGS}
    else:
        msg, fix = build(code, v, e)
    return {"code": code, "severity": sev, "page": page,
            "bbox": [round(x, 1) for x in bbox] if bbox else None,
            "value": str(v), "expected": str(e), "msg": msg, "fix": fix}

def _spelling(doc):
    """English only, confirm-level: skips names, ALL-CAPS, short words and pages that are mostly not English."""
    global _SPELL
    from spellchecker import SpellChecker
    if _SPELL is None: _SPELL = SpellChecker()
    out, seen = [], set()
    for pno, page in enumerate(doc, start=1):
        spans = [sp for blk in page.get_text("dict")["blocks"] for ln in blk.get("lines", []) for sp in ln["spans"]]
        words = {w.lower() for sp in spans for w in re.findall(r"[A-Za-z]{4,}", sp["text"]) if not w.isupper()}
        if words:
            unknown = _SPELL.unknown(words)
            if len(words) >= 6 and len(unknown) / len(words) > 0.35: continue   # not an English page
        for sp in spans:
            for w in re.findall(r"[A-Za-z]{4,}", sp["text"]):
                lw = w.lower()
                if w.isupper() or lw in seen: continue
                if _SPELL.known([lw]): continue
                sug = _SPELL.correction(lw)
                if not sug or sug == lw: continue
                # Capitalised words may be names: flag only a clear one-letter typo of a longer word
                if w[0].isupper() and (len(lw) < 6 or sug not in _SPELL.edit_distance_1(lw)): continue
                seen.add(lw)
                out.append(_finding("spelling", "confirm", pno, fitz.Rect(sp["bbox"]), w, sug))
                if len(out) >= 8: return out
    return out

def analyze_full(path, profile="offset_coated", opts=None):
    t0 = time.time()
    res = analyze(path, profile, opts)
    if res["corrupt"]: return res
    extra = []
    try:
        extra += _spelling(fitz.open(path))
    except Exception:
        pass
    if not extra: return res
    findings = res["report"]["findings"] + extra
    return analyzer._pack(findings, res["fact_sheet"], t0)

def render_previews(path, outdir, max_px=1100):
    """bbox values are in PDF points; UI scales by px_w / w_pt."""
    out = []
    try:
        doc = fitz.open(path)
        for i, page in enumerate(doc, start=1):
            if i > 12: break
            r = page.rect; s = min(2.0, max_px / max(r.width, r.height))
            pix = page.get_pixmap(matrix=fitz.Matrix(s, s), alpha=False)
            fn = os.path.join(outdir, f"p{i}.jpg"); pix.save(fn, jpg_quality=80)
            out.append({"page": i, "file": fn, "w_pt": round(r.width, 2), "h_pt": round(r.height, 2), "px_w": pix.width, "px_h": pix.height})
    except Exception:
        pass
    return out

def image_preview(path, outdir, max_px=1100):
    from PIL import Image
    try:
        im = Image.open(path).convert("RGB"); im.thumbnail((max_px, max_px))
        fn = os.path.join(outdir, "p1.jpg"); im.save(fn, quality=80)
        return [{"page": 1, "file": fn, "w_pt": im.width, "h_pt": im.height, "px_w": im.width, "px_h": im.height}]
    except Exception:
        return []
