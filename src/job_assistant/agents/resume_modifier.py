"""Resume Modifier subagent: tailor base resume to a JD at a fixed page count."""

from __future__ import annotations

import re
from pathlib import Path

from ..config import Settings, DATA_DIR
from ..llm import complete
from ..pdf import compile_pdf, pdf_page_count

SYSTEM = (
    "You are a professional resume writer. You receive a base resume, a job "
    "description, and extra project/knowledge notes. Produce a LaTeX resume "
    "that fits the \\documentclass[11pt]{article} template with geometry margin=0.6in. "
    "Keep it concise enough to fill exactly the requested number of pages. "
    "Never fabricate employers, dates, or degrees. Only use facts from the base "
    "resume and knowledge notes. Output ONLY the full LaTeX source."
)

TEMPLATE_PATH = Path(__file__).resolve().parents[3] / "templates" / "resume.tex"


def _read_base_resume(settings: Settings) -> str:
    p = Path(settings.resume_path)
    if not p.exists():
        return "(no base resume file found)"
    if p.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader
            return "\n".join(page.extract_text() or "" for page in PdfReader(str(p)).pages)
        except Exception:  # noqa: BLE001
            return "(could not read PDF resume)"
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:  # noqa: BLE001
        return "(could not read resume file)"


def tailor_resume(settings: Settings, job_title: str, company: str, description: str, extra_info: str = "") -> tuple[str, Path, int]:
    base = _read_base_resume(settings)
    knowledge = ""
    if settings.knowledge_path and Path(settings.knowledge_path).exists():
        knowledge = Path(settings.knowledge_path).read_text(encoding="utf-8", errors="ignore")

    history = ""
    tex = ""
    for attempt in range(3):
        prompt = (
            f"Base resume:\n{base[:5000]}\n\nKnowledge notes:\n{knowledge[:3000]}\n\n"
            f"Target job: {job_title} at {company}\nJD:\n{description[:4000]}\n\n"
            f"Extra info from user: {extra_info}\n\n"
            f"Requested length: exactly {settings.resume_pages} page(s).\n"
            f"{history}"
            "Output full LaTeX only."
        )
        out = complete(settings, prompt, SYSTEM)
        m = re.search(r"\\documentclass.*?\\end\{document\}", out, re.DOTALL)
        tex = m.group(0) if m else out
        try:
            pdf = compile_pdf(tex)
        except RuntimeError as e:
            history = f"Previous attempt failed to compile:\n{e}\nFix the LaTeX.\n\n"
            continue
        pages = pdf_page_count(pdf)
        if pages == settings.resume_pages:
            return tex, pdf, pages
        if pages > settings.resume_pages:
            history = f"Previous attempt was {pages} page(s); make it shorter to fit {settings.resume_pages}.\n\n"
        else:
            history = f"Previous attempt was {pages} page(s); expand slightly to fill {settings.resume_pages}.\n\n"
    # last attempt result
    return tex, DATA_DIR / "output" / "resume.pdf", -1


def cover_letter(settings: Settings, job_title: str, company: str, description: str, extra_info: str = "") -> str:
    base = _read_base_resume(settings)
    system = (
        "Write a concise, professional cover letter (under 300 words) for the given job. "
        "Use only facts from the resume. Plain text output only."
    )
    prompt = (
        f"Resume:\n{base[:4000]}\n\nJob: {job_title} at {company}\nJD:\n{description[:3000]}\n"
        f"Extra info: {extra_info}"
    )
    try:
        return complete(settings, prompt, system)
    except Exception as e:  # noqa: BLE001
        return f"Cover letter generation failed: {e}"
