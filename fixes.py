"""Auto-Fix: deterministic whole-document repairs for a small set of safe finding types.

Each fix_type maps to one Ghostscript-based transform plus the set of analyzer finding codes
it clears from the report once applied. v1 scope (owner, 27 Nov 2026): only two fixes --
RGB->CMYK conversion and transparency flattening -- picked because both are reliable,
deterministic file-level transforms that do not depend on having the original font files or
guessing design intent (unlike font-embedding, which would need the real font, or bleed
extension / text repositioning, which can change the look of the design). See
claude/future_features.md for the fuller safe / risky / never list.
"""
import os
import subprocess

FIX_SPECS = {
    "rgb_to_cmyk": {
        "codes": {"rgb_color"},
        "gs_args": [
            "-sDEVICE=pdfwrite", "-sColorConversionStrategy=CMYK",
            "-dProcessColorModel=/DeviceCMYK", "-dCompatibilityLevel=1.4",
            "-dAutoRotatePages=/None",
        ],
    },
    "transparency_flatten": {
        "codes": {"transparency"},
        "gs_args": [
            "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.3", "-dAutoRotatePages=/None",
        ],
    },
}


def resolved_codes(fix_type):
    spec = FIX_SPECS.get(fix_type)
    return spec["codes"] if spec else set()


def apply_fix(fix_type, in_path, out_path, timeout=120):
    """Runs the Ghostscript transform for fix_type on in_path, writing out_path.
    Raises on any failure (non-zero exit, missing/empty output) -- callers must not
    treat a partially-written file as success."""
    spec = FIX_SPECS.get(fix_type)
    if not spec:
        raise ValueError(f"unknown fix_type: {fix_type}")
    cmd = ["gs", "-o", out_path, *spec["gs_args"], in_path]
    r = subprocess.run(cmd, capture_output=True, timeout=timeout)
    if r.returncode != 0 or not os.path.exists(out_path) or os.path.getsize(out_path) < 100:
        raise RuntimeError(
            f"ghostscript failed (code {r.returncode}) for {fix_type}: "
            f"{r.stderr.decode('utf-8', 'ignore')[:500]}"
        )
    return out_path
