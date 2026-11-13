"""Cleara worker: polls Supabase for queued jobs, analyzes PDFs, writes report back."""
import os, sys, time, tempfile, traceback
import requests
from engine import analyze_full, analyze_image, render_previews, image_preview

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
        try: sb.update(jid, {"status": "failed", "result": "error"})
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
        except Exception as e:
            print("poll error:", e)
        time.sleep(int(os.environ.get("POLL_SECONDS", "5")))

if __name__ == "__main__": main()
