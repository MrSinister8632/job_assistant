"""LLM client wrappers for Groq and Gemini."""

from __future__ import annotations

from .config import Settings


def gemini_complete(settings: Settings, prompt: str, system: str = "", model: str = "gemini-2.0-flash") -> str:
    if not settings.gemini_api_key:
        raise RuntimeError("Gemini API key not set")
    from google import genai

    client = genai.Client(api_key=settings.gemini_api_key)
    if system:
        prompt = f"{system}\n\n{prompt}"
    resp = client.models.generate_content(model=model, contents=prompt)
    return resp.text or ""


def complete(settings: Settings, prompt: str, system: str = "") -> str:
    """Single provider: Gemini only."""
    return gemini_complete(settings, prompt, system)
