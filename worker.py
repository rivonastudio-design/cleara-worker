"""Cleara worker: polls Supabase for queued jobs, analyzes PDFs, writes report back."""
import os, sys, time, tempfile, traceback
import requests
import analyzer
from engine import analyze_full, analyze_image, render_previews, image_preview
from messages import build as build_msg
from fixes import apply_fix, resolved_codes, RENUMBERING_FIXES


def _crash_report():
    """Used when something unexpected breaks the job (not a 'bad file' we already recognise,
    e.g. an unsupported format or a download hiccup). Without this, the report would be left
    empty and the client would just see 'Not Printable' with no explanation at all."""
    msg, fix = build_msg("processing_failed")
    finding = {"code": "processing_failed", "severity": "error", "page": None, "bbox": None,
               "value": "", "expected": "", "msg": msg, "fix": fix, "no": 1}
    return {"version": 2, "summary": {"errors": 1, "warnings": 0, "confirms": 0, "result": "error"},
            "findings": [finding]}

def load_env():
    if os.path.exists(".env"):
        for line in open(".env", encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

class Sb:
    def __init__(self, url, key):
        self.url = url.rstrip("/")
        self.h = {"apikey": key, "Authorization": f"Bearer {key}"}
    def queued(self, n=5):
        r = requests.get(f"{self.url}/rest/v1/jobs", headers=self.h, timeout=30,
            params={"status": "eq.queued", "order": "created_at.asc", "limit": n, "select": "*"})
        r.raise_for_status(); return r.json()
    def claim(self, jid):  # atomic: only succeeds if still queued
        r = requests.patch(f"{self.url}/rest/v1/jobs", headers={**self.h, "Prefer": "return=representation"}, timeout=30,
            params={"id": f"eq.{jid}", "status": "eq.queued"}, json={"status": "processing"})
        r.raise_for_status(); return bool(r.json())
    def preset(self, pid):
        if not pid: return None
        r = requests.get(f"{self.url}/rest/v1/presets", headers=self.h, timeout=30, params={"id": f"eq.{pid}", "select": "*"})
        r.raise_for_status(); j = r.json(); return j[0] if j else None
    def upload_preview(self, path, fn):
        h = {**self.h, "Content-Type": "image/jpeg", "x-upsert": "true"}
        r = requests.post(f"{self.url}/storage/v1/object/previews/{path}", headers=h, data=open(fn, "rb").read(), timeout=120)
        r.raise_for_status()
    def update(self, jid, data):
        r = requests.patch(f"{self.url}/rest/v1/jobs", headers=self.h, timeout=30, params={"id": f"eq.{jid}"}, json=data)
        r.raise_for_status()
    def download(self, path, dest):
        path = path.lstrip("/")
        if path.startswith("uploads/"): path = path[len("uploads/"):]
        r = requests.get(f"{self.url}/storage/v1/object/uploads/{path}", headers=self.h, timeout=120)
        r.raise_for_status(); open(dest, "wb").write(r.content)

    # -------- Auto-Fix (added 27 Nov) --------
    def get_job(self, jid):
        r = requests.get(f"{self.url}/rest/v1/jobs", headers=self.h, timeout=30, params={"id": f"eq.{jid}", "select": "*"})
        r.raise_for_status(); j = r.json(); return j[0] if j else None
    def queued_fixes(self, n=5):
        r = requests.get(f"{self.url}/rest/v1/fix_requests", headers=self.h, timeout=30,
            params={"status": "eq.queued", "order": "created_at.asc", "limit": n, "select": "*"})
        r.raise_for_status(); return r.json()
    def applying_fixes(self, n=5):
        r = requests.get(f"{self.url}/rest/v1/fix_requests", headers=self.h, timeout=30,
            params={"status": "eq.applying", "order": "updated_at.asc", "limit": n, "select": "*"})
        r.raise_for_status(); return r.json()
    def claim_fix(self, fid, from_status, to_status):  # atomic: only succeeds if still in from_status
        r = requests.patch(f"{self.url}/rest/v1/fix_requests", headers={**self.h, "Prefer": "return=representation"}, timeout=30,
            params={"id": f"eq.{fid}", "status": f"eq.{from_status}"}, json={"status": to_status})
        r.raise_for_status(); return bool(r.json())
    def update_fix(self, fid, data):
        r = requests.patch(f"{self.url}/rest/v1/fix_requests", headers=self.h, timeout=30, params={"id": f"eq.{fid}"}, json=data)
        r.raise_for_status()
    def upload_report_file(self, path, fn):
        h = {**self.h, "Content-Type": "application/pdf", "x-upsert": "true"}
        r = requests.post(f"{self.url}/storage/v1/object/reports/{path}", headers=h, data=open(fn, "rb").read(), timeout=120)
        r.raise_for_status()
    def rpc(self, fn, params):
        r = requests.post(f"{self.url}/rest/v1/rpc/{fn}", headers=self.h, timeout=30, json=params)
        r.raise_for_status()
        try: return r.json()
        except Exception: return None

def mark_findings(findings, previews):
    """Attach a marker (% position on that page's preview picture) to every finding that
    has an exact spot (bbox). Lets the report draw the same numbered circle on the preview
    that is shown next to that problem and its solution."""
    by_page = {p["page"]: p for p in previews}
    for f in findings:
        pv = by_page.get(f.get("page"))
        bbox = f.get("bbox")
        if not pv or not bbox or not pv.get("w_pt") or not pv.get("h_pt"):
            continue
        try:
            x0, y0, x1, y1 = bbox
            f["marker"] = {
                "page": f["page"],
                "x_pct": round(max(0, min(100, x0 / pv["w_pt"] * 100)), 2),
                "y_pct": round(max(0, min(100, y0 / pv["h_pt"] * 100)), 2),
                "w_pct": round(max(0, x1 - x0) / pv["w_pt"] * 100, 2),
                "h_pct": round(max(0, y1 - y0) / pv["h_pt"] * 100, 2),
            }
        except Exception:
            pass

def process(sb, job):
    jid = job["id"]
    if not sb.claim(jid): return
    print(f"[{job.get('job_no')}] {job.get('file_name')} ...", end=" ", flush=True)
    try:
        ft = str(job.get("file_type") or "pdf").lower()
        if ft not in ("pdf", "png", "jpg"):
            raise ValueError("file type not supported yet: " + ft)
        pr = sb.preset(job.get("preset_id"))
        # job options; shape_cut / single_colour are read only if the jobs table has those columns
        opts = {"mode": job.get("mode") or "single", "shape_cut": bool(job.get("shape_cut")),
                "single_colour": bool(job.get("single_colour"))}
        if pr:
            opts.update({"expected_mm": (float(pr["width_mm"]), float(pr["height_mm"])),
                         "bleed_mm": float(pr["bleed_mm"]), "safe_mm": float(pr["safe_mm"])})
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "in." + ft); sb.download(job["file_path"], p)
            fn = analyze_full if ft == "pdf" else analyze_image
            res = fn(p, job.get("profile") or "offset_coated", opts)
            try:
                pv = render_previews(p, td) if ft == "pdf" else image_preview(p, td)
                prev = []
                for x in pv:
                    path = f"{job['agency_id']}/{jid}/p{x['page']}.jpg"
                    sb.upload_preview(path, x["file"])
                    prev.append({"page": x["page"], "path": path, "w_pt": x["w_pt"], "h_pt": x["h_pt"], "px_w": x["px_w"], "px_h": x["px_h"]})
                res["fact_sheet"]["previews"] = prev
                mark_findings(res["report"]["findings"], prev)
            except Exception as e:
                print("preview skipped:", e)
        s = res["report"]["summary"]
        if res["corrupt"]:
            sb.update(jid, {"status": "failed", "result": "error", "report": res["report"],
                            "fact_sheet": res["fact_sheet"], "processing_ms": res["processing_ms"]})
        else:
            sb.update(jid, {"status": "done", "result": res["result"], "report": res["report"],
                            "fact_sheet": res["fact_sheet"], "processing_ms": res["processing_ms"],
                            "review_flag": s["confirms"] > 0})
        print(res["result"], f"({res['processing_ms']} ms)")
    except Exception as e:
        traceback.print_exc()
        try:
            sb.update(jid, {"status": "failed", "result": "error", "report": _crash_report(),
                            "fact_sheet": {"pages": 0}})
        except Exception: pass
        print("FAILED")

def process_fix_generate(sb, fr):
    """Auto-Fix step 1 (added 27 Nov, extended 28 Nov for 4 more fix types). fr is a
    fix_requests row with status='queued' (client tapped 'Fix this', no credit charged yet --
    preview is free). Downloads the job's original file, runs the transform for fr['fix_type']
    (fixes.py -- either a Ghostscript pass or a PyMuPDF content edit), renders an 'after'
    preview, uploads both, and moves the row to preview_ready so the client can see
    before/after. Any failure marks the row failed with a reason (nothing to refund yet at
    this step, since no credit was charged).

    For most fix types the preview only needs the pages that had the finding. remove_blank_pages
    is different -- it changes the page count, so every page shifts; the preview renders the
    WHOLE new document instead (RENUMBERING_FIXES), and add_crop_marks additionally needs the
    job's preset size (the same trim-box info analyzer used to decide the page qualifies)."""
    fid = fr["id"]
    if not sb.claim_fix(fid, "queued", "generating"): return
    print(f"[fix {fid}] {fr['fix_type']} generating ...", end=" ", flush=True)
    try:
        job = sb.get_job(fr["job_id"])
        if not job: raise RuntimeError("job not found")
        fix_type = fr["fix_type"]
        codes = resolved_codes(fix_type)
        findings = (job.get("report") or {}).get("findings") or []
        affected_pages = sorted({f["page"] for f in findings if f.get("code") in codes and f.get("page")})
        context = {"pages": affected_pages}
        if fix_type == "add_crop_marks":
            pr = sb.preset(job.get("preset_id"))
            if not pr: raise RuntimeError("job has no preset -- can't know the trim size for crop marks")
            context["width_mm"] = float(pr["width_mm"]); context["height_mm"] = float(pr["height_mm"])
        with tempfile.TemporaryDirectory() as td:
            ft = str(job.get("file_type") or "pdf").lower()
            in_path = os.path.join(td, "in." + ft)
            sb.download(job["file_path"], in_path)
            out_path = os.path.join(td, "fixed.pdf")
            apply_fix(fix_type, in_path, out_path, context=context)
            report_path = f"{fr['agency_id']}/{fr['job_id']}/fixed_{fix_type}.pdf"
            sb.upload_report_file(report_path, out_path)
            preview_pages = None if fix_type in RENUMBERING_FIXES else (affected_pages or None)
            pv = render_previews(out_path, td, pages=preview_pages)
            after = []
            for x in pv:
                ppath = f"{fr['agency_id']}/{fr['job_id']}/fix_{fix_type}_after_p{x['page']}.jpg"
                sb.upload_preview(ppath, x["file"])
                after.append({"page": x["page"], "path": ppath, "w_pt": x["w_pt"], "h_pt": x["h_pt"],
                              "px_w": x["px_w"], "px_h": x["px_h"]})
        sb.update_fix(fid, {"status": "preview_ready", "after_preview": after, "fixed_file_path": report_path})
        print("ok")
    except Exception as e:
        traceback.print_exc()
        try: sb.update_fix(fid, {"status": "failed", "error_message": str(e)[:500]})
        except Exception: pass
        print("FAILED")

def process_fix_finalize(sb, fr):
    """Auto-Fix step 2 (added 27 Nov, extended 28 Nov). fr is a fix_requests row with
    status='applying' -- the client already chose 'After' and request_fix_apply() already
    charged 1 credit. Takes the job's existing report, drops every finding whose code this
    fix resolves, re-packs the report (same analyzer._pack used for fresh jobs, so
    numbering/labels/summary/pages_status stay consistent), swaps in the already-generated
    after-preview images, and writes it all back onto the job row so the client sees an
    updated report. On any failure, refunds the credit via fix_request_refund() so the client
    isn't charged for a fix that didn't actually land.

    remove_blank_pages is the one fix that changes the page count (RENUMBERING_FIXES): every
    remaining finding's page number has to shift down by however many deleted pages came
    before it, findings that were ON a deleted page are dropped (that page no longer exists),
    fact_sheet.pages shrinks, and the previews array is replaced wholesale with the
    already-rendered after_preview (which covered the WHOLE new document, not just specific
    pages, since old page numbers don't line up with the new ones)."""
    fid = fr["id"]
    if not sb.claim_fix(fid, "applying", "finalizing"): return
    print(f"[fix {fid}] {fr['fix_type']} finalizing ...", end=" ", flush=True)
    try:
        job = sb.get_job(fr["job_id"])
        if not job: raise RuntimeError("job not found")
        fix_type = fr["fix_type"]
        codes = resolved_codes(fix_type)
        report = job.get("report") or {}
        fact = dict(job.get("fact_sheet") or {})
        old_findings = report.get("findings") or []

        if fix_type in RENUMBERING_FIXES:
            deleted_pages = sorted({f["page"] for f in old_findings if f.get("code") in codes and f.get("page")})
            def remap(p):
                if p is None: return None
                return p - sum(1 for d in deleted_pages if d < p)
            remaining = []
            for f in old_findings:
                if f.get("code") in codes or f.get("page") in deleted_pages:
                    continue  # the resolved finding itself, or anything on a now-deleted page
                f = dict(f); f["page"] = remap(f.get("page")); remaining.append(f)
            if fact.get("pages"):
                fact["pages"] = max(0, fact["pages"] - len(deleted_pages))
            fact["previews"] = fr.get("after_preview") or []
        else:
            remaining = [f for f in old_findings if f.get("code") not in codes]

        packed = analyzer._pack(remaining, fact, time.time())
        new_report = packed["report"]

        if fix_type not in RENUMBERING_FIXES:
            by_page = {p["page"]: p for p in (fr.get("after_preview") or [])}
            previews = fact.get("previews") or []
            for p in previews:
                if p.get("page") in by_page:
                    p.update({k: v for k, v in by_page[p["page"]].items() if k != "page"})
            fact["previews"] = previews
        mark_findings(new_report["findings"], fact["previews"])

        sb.update(fr["job_id"], {"report": new_report, "fact_sheet": fact, "result": new_report["summary"]["result"],
                                  "review_flag": new_report["summary"]["confirms"] > 0})
        sb.update_fix(fid, {"status": "applied"})
        print("ok")
    except Exception as e:
        traceback.print_exc()
        try:
            sb.rpc("fix_request_refund", {"p_fix_request_id": fid})
            sb.update_fix(fid, {"status": "failed", "error_message": str(e)[:500]})
        except Exception: pass
        print("FAILED")

def main():
    load_env()
    url, key = os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key: sys.exit("Fill SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in the .env file first.")
    sb = Sb(url, key); print("Cleara worker started. Ctrl+C to stop.")
    while True:
        try:
            for job in sb.queued(): process(sb, job)
            for fr in sb.queued_fixes(): process_fix_generate(sb, fr)
            for fr in sb.applying_fixes(): process_fix_finalize(sb, fr)
        except Exception as e:
            print("poll error:", e)
        time.sleep(int(os.environ.get("POLL_SECONDS", "5")))

if __name__ == "__main__": main()
