from __future__ import annotations

import asyncio
import re
from typing import Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from app.core.config import get_settings
from app.schemas.scrape import ScrapePage, ScrapeResult
from app.services.url_safety import ensure_public_url


DEFAULT_PATHS = ["/", "/pricing", "/features", "/docs", "/about"]
PRICE_TOKENS = ("$", "pricing", "per month", "/mo", "/month", "/yr", "/year")
BLOCKED_RESOURCE_TYPES = {"image", "media", "font"}
MAX_CONCURRENT_PAGES = 3


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def _extract_pricing(text: str) -> list[str]:
    lines = re.split(r"\n|\r", text)
    candidates: list[str] = []
    for line in lines:
        cleaned = " ".join(line.split())
        if not cleaned:
            continue
        lowered = cleaned.lower()
        if any(token in lowered for token in PRICE_TOKENS):
            candidates.append(cleaned)
    return _dedupe(candidates)[:12]


def _extract_headings(soup: BeautifulSoup) -> list[str]:
    headings: list[str] = []
    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = tag.get_text(" ", strip=True)
        if text:
            headings.append(text)
    return _dedupe(headings)[:24]


def _extract_descriptions(soup: BeautifulSoup) -> list[str]:
    descriptions: list[str] = []
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        descriptions.append(meta["content"].strip())
    for paragraph in soup.find_all("p")[:10]:
        text = paragraph.get_text(" ", strip=True)
        if text and len(text) > 40:
            descriptions.append(text)
    return _dedupe(descriptions)[:12]


def _extract_links(soup: BeautifulSoup, base_url: str) -> list[str]:
    links: list[str] = []
    for anchor in soup.find_all("a"):
        href = anchor.get("href")
        if not href:
            continue
        absolute = urljoin(base_url, href)
        links.append(absolute)
    return _dedupe(links)[:50]


def _extract_metadata(soup: BeautifulSoup) -> dict[str, Any]:
    meta_map: dict[str, Any] = {}
    for meta in soup.find_all("meta"):
        key = meta.get("name") or meta.get("property")
        content = meta.get("content")
        if key and content:
            meta_map[key] = content
    return meta_map


async def scrape_site(base_url: str, paths: list[str] | None = None) -> ScrapeResult:
    settings = get_settings()
    target_paths = paths or DEFAULT_PATHS

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=settings.playwright_headless)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            )
        )

        async def handle_route(route, request) -> None:
            if request.resource_type in BLOCKED_RESOURCE_TYPES:
                await route.abort()
            else:
                await route.continue_()

        await context.route("**/*", handle_route)

        semaphore = asyncio.Semaphore(MAX_CONCURRENT_PAGES)

        async def fetch_path(path: str) -> ScrapePage:
            url = urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
            async with semaphore:
                page = await context.new_page()
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=20000)
                    await ensure_public_url(page.url)
                    html = await page.content()
                    title = await page.title()
                    soup = BeautifulSoup(html, "lxml")

                    headings = _extract_headings(soup)
                    descriptions = _extract_descriptions(soup)
                    links = _extract_links(soup, url)
                    pricing = _extract_pricing(soup.get_text("\n", strip=True))

                    scripts = [
                        script.get("src")
                        for script in soup.find_all("script")
                        if script.get("src")
                    ]

                    metadata = _extract_metadata(soup)
                    metadata["scripts"] = _dedupe(scripts)
                    metadata["html_snippet"] = html[:5000]

                    return ScrapePage(
                        url=url,
                        title=title,
                        headings=headings,
                        pricing=pricing,
                        descriptions=descriptions,
                        links=links,
                        metadata=metadata,
                    )
                except Exception:
                    return ScrapePage(
                        url=url,
                        title=None,
                        headings=[],
                        pricing=[],
                        descriptions=[],
                        links=[],
                        metadata={"error": "failed_to_fetch"},
                    )
                finally:
                    await page.close()

        pages = await asyncio.gather(*[fetch_path(path) for path in target_paths])

        await context.close()
        await browser.close()

    return ScrapeResult(base_url=base_url, pages=pages)
