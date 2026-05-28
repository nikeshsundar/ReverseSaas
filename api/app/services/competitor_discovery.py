from __future__ import annotations

from typing import Any

from app.schemas.scrape import ScrapeResult
from app.schemas.technology import TechnologyStack
from app.services.gemini import generate_json


def _fallback_competitors() -> dict[str, Any]:
    return {
        "top_competitors": [
            {"name": "Similar SaaS A", "description": "Adjacent product in the space."},
            {"name": "Similar SaaS B", "description": "Competes on pricing."},
        ],
        "alternative_products": ["Manual research", "Generic analytics tools"],
        "market_positioning": "Emerging SaaS intelligence platform.",
        "advantages": ["Speed to insights", "Clean reporting"],
        "disadvantages": ["Needs deeper data integrations"],
    }


async def discover_competitors(
    scrape_result: ScrapeResult, tech_stack: TechnologyStack
) -> dict[str, Any]:
    prompt = (
        "You are a market analyst. Return ONLY JSON with the exact schema below."
        "\n\nSchema:"
        "{"
        '"top_competitors": [{"name": string, "description": string}],'
        '"alternative_products": string[],'
        '"market_positioning": string,'
        '"advantages": string[],'
        '"disadvantages": string[]'
        "}"
        "\n\nInput data:"
        f"\nBase URL: {scrape_result.base_url}"
        f"\nHeadlines: {[page.headings[:5] for page in scrape_result.pages]}"
        f"\nStack: {[item.name for item in tech_stack.frontend + tech_stack.backend]}"
    )

    data = await generate_json(prompt)
    if not data:
        return _fallback_competitors()

    return data
