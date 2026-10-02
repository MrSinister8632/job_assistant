"""LaTeX -> PDF via Tectonic."""

from __future__ import annotations

import subprocess
from pathlib import Path

from .config import DATA_DIR

BIN_DIR = Path(__file__).resolve().parents[2] / "bin"
if getattr(__import__("sys"), "frozen", False):  # PyInstaller bundle
    BIN_DIR = Path(getattr(__import__("sys"), "_MEIPASS")) / "bin"
TECTONIC = BIN_DIR / "tectonic.exe"


def compile_pdf(tex_source: str, out_dir: Path | None = None) -> Path:
    out_dir = out_dir or (DATA_DIR / "output")
    out_dir.mkdir(parents=True, exist_ok=True)
    tex_path = out_dir / "resume.tex"
    tex_path.write_text(tex_source, encoding="utf-8")
    tectonic = str(TECTONIC if TECTONIC.exists() else "tectonic")
    proc = subprocess.run(
        [tectonic, "--outdir", str(out_dir), str(tex_path)],
        capture_output=True, text=True, timeout=300,
    )
    pdf = out_dir / "resume.pdf"
    if proc.returncode != 0 or not pdf.exists():
        raise RuntimeError(f"Tectonic failed:\n{proc.stderr}\n{proc.stdout}")
    return pdf


def pdf_page_count(pdf_path: Path) -> int:
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(pdf_path)).pages)
    except ImportError:
        # fallback: count /Type /Page occurrences
        data = pdf_path.read_bytes()
        return data.count(b"/Type /Page") - data.count(b"/Type /Pages")
