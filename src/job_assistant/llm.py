"""LLM client wrappers for Groq and Gemini."""

from __future__ import annotations

from .config import Settings


def groq_complete(settings: Settings, prompt: str, system: str = "", model: str = "llama-3.3-70b-versatile") -> str:
    if not settings.groq_api_key:
        raise RuntimeError("Groq API key not set")
    from groq import Groq

    client = Groq(api_key=settings.groq_api_key)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(model=model, messages=messages)
    return resp.choices[0].message.content or ""


def gemini_complete(settings: Settings, prompt: str, system: str = "", model: str = "gemini-2.0-flash") -> str:
    if not settings.gemini_api_key:
        raise RuntimeError("Gemini API key not set")
    from google import genai

    client = genai.Client(api_key=settings.gemini_api_key)
    if system:
        prompt = f"{system}\n\n{prompt}"
    resp = client.models.generate_content(model=model, contents=prompt)
    return resp.text or ""


def complete(settings: Settings, prompt: str, system: str = "", prefer: str = "groq") -> str:
    """Try preferred provider, fall back to the other."""
    providers = [groq_complete, gemini_complete] if prefer == "groq" else [gemini_complete, groq_complete]
    last_err: Exception | None = None
    for fn in providers:
        try:
            return fn(settings, prompt, system)
        except Exception as e:  # noqa: BLE001
            last_err = e
    raise RuntimeError(f"All LLM providers failed: {last_err}")
