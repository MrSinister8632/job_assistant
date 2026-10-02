"""Eligibility scorer: does the candidate qualify for this job?"""

from __future__ import annotations

import json
import re

from ..config import Settings
from ..llm import complete

SYSTEM = (
    "You are a strict job-eligibility evaluator. Given a job description and a "
    "candidate profile, respond with JSON only: "
    '{"eligible": true|false, "score": 0.0-1.0, "missing_skills": [...]}'
)


def score_job(settings: Settings, description: str, profile: str) -> dict:
    prompt = (
        f"CANDIDATE PROFILE:\n{profile[:6000]}\n\n"
        f"JOB DESCRIPTION:\n{description[:6000]}\n\n"
        "Return the JSON object only."
    )
    try:
        out = complete(settings, prompt, SYSTEM)
    except Exception as e:  # noqa: BLE001
        return {"eligible": False, "score": 0.0, "missing_skills": [], "error": str(e)}

    match = re.search(r"\{.*\}", out, re.DOTALL)
    if not match:
        return {"eligible": False, "score": 0.0, "missing_skills": [], "error": "bad LLM output"}
    try:
        data = json.loads(match.group(0))
        return {
            "eligible": bool(data.get("eligible")),
            "score": float(data.get("score", 0.0)),
            "missing_skills": list(data.get("missing_skills", [])),
        }
    except (json.JSONDecodeError, ValueError):
        return {"eligible": False, "score": 0.0, "missing_skills": [], "error": "bad JSON"}
