from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ScrapePage(BaseModel):
    url: str
    title: str | None
    headings: list[str]
    pricing: list[str]
    descriptions: list[str]
    links: list[str]
    metadata: dict[str, Any]


class ScrapeResult(BaseModel):
    base_url: str
    pages: list[ScrapePage]
