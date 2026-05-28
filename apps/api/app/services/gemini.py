from __future__ import annotations

import json
from typing import Any

import httpx

from app.core.config import get_settings


GEMINI_MODEL = "gemini-1.5-flash"


def _strip_code_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()
    return cleaned


def _safe_json(text: str) -> dict[str, Any]:
    try:
        return json.loads(_strip_code_fences(text))
    except json.JSONDecodeError:
        return {}


async def generate_json(prompt: str) -> dict[str, Any]:
    settings = get_settings()
    if not settings.gemini_api_key:
        return {}

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={settings.gemini_api_key}"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.4,
            "response_mime_type": "application/json",
        },
    }

    async with httpx.AsyncClient(timeout=40) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError):
        return {}

    return _safe_json(text)
