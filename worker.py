"""Cleara worker: polls Supabase for queued jobs, analyzes PDFs, writes report back."""
import os, sys, time, tempfile, traceback
import requests
from analyzer import analyze, analyze_image

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
        opts = {}
        if pr:
            opts = {"expected_mm": (float(pr["width_mm"]), float(pr["height_mm"])),
                    "bleed_mm": float(pr["bleed_mm"]), "safe_mm": float(pr["safe_mm"])}
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "in." + ft); sb.download(job["file_path"], p)
            fn = analyze if ft == "pdf" else analyze_image
            res = fn(p, job.get("profile") or "offset_coated", opts)
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
