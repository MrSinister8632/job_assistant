"""Job Details Summarizer subagent: JD → concise list summary."""

from __future__ import annotations

from ..config import Settings
from ..llm import complete

SYSTEM = (
    "You summarize job postings for a job seeker. Output a concise markdown list with "
    "these sections: **Role**, **Responsibilities**, **Requirements**, **Pay**, **Company** "
    "(what the company does). Use '- ' bullets. If pay or company info is not in the "
    "posting, write 'Not specified' — never invent it."
)


def summarize_job(settings: Settings, title: str, company: str, description: str) -> str:
    prompt = f"Job title: {title}\nCompany: {company}\n\nDescription:\n{description[:6000]}"
    try:
        return complete(settings, prompt, SYSTEM)
    except Exception as e:  # noqa: BLE001
        return f"Summary unavailable: {e}"
