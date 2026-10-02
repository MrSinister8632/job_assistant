"""Verifier subagent: sanity-checks generated artifacts before they reach the user."""

from __future__ import annotations

from ..config import Settings
from ..llm import complete

SYSTEM = (
    "You verify a tailored resume against the source profile. Check for: "
    "(1) fabricated companies/degrees/dates, (2) claims not in the source, "
    "(3) missing critical sections. Reply JSON only: "
    '{"ok": true|false, "issues": [...]}'
)


def verify_resume(settings: Settings, tex: str, profile: str) -> dict:
    import json as _json
    import re

    prompt = (
        f"SOURCE PROFILE:\n{profile[:5000]}\n\nGENERATED LATEX RESUME:\n{tex[:5000]}\n\nJSON only."
    )
    try:
        out = complete(settings, prompt, SYSTEM)
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "issues": [str(e)]}
    m = re.search(r"\{.*\}", out, re.DOTALL)
    if not m:
        return {"ok": False, "issues": ["bad verifier output"]}
    try:
        d = _json.loads(m.group(0))
        return {"ok": bool(d.get("ok")), "issues": list(d.get("issues", []))}
    except (_json.JSONDecodeError, ValueError):
        return {"ok": False, "issues": ["bad verifier JSON"]}


def verify_summary(settings: Settings, summary: str, description: str) -> dict:
    import json as _json
    import re

    prompt = (
        f"JD:\n{description[:4000]}\n\nSUMMARY:\n{summary[:3000]}\n\n"
        "Does the summary invent pay/company facts not in the JD? Reply JSON only: "
        '{"ok": true|false, "issues": [...]}'
    )
    try:
        out = complete(settings, prompt, "You are a fact-checker. JSON only.")
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "issues": [str(e)]}
    m = re.search(r"\{.*\}", out, re.DOTALL)
    if not m:
        return {"ok": False, "issues": ["bad verifier output"]}
    try:
        d = _json.loads(m.group(0))
        return {"ok": bool(d.get("ok")), "issues": list(d.get("issues", []))}
    except (_json.JSONDecodeError, ValueError):
        return {"ok": False, "issues": ["bad verifier JSON"]}
