from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from app.schemas.scrape import ScrapeResult
from app.schemas.technology import TechnologyStack
from app.services.gemini import generate_json


def _fallback_company_name(url: str) -> str:
    host = urlparse(url).netloc
    if not host:
        return "Unknown"
    return host.split(":")[0].split(".")[0].replace("-", " ").title()


def _compact_scrape(scrape_result: ScrapeResult) -> dict[str, Any]:
    pages = []
    for page in scrape_result.pages:
        pages.append(
            {
                "url": page.url,
                "title": page.title,
                "headings": page.headings[:6],
                "pricing": page.pricing[:6],
                "descriptions": page.descriptions[:4],
                "metadata": {
                    k: page.metadata.get(k)
                    for k in ["description", "og:title", "og:description"]
                    if page.metadata.get(k)
                },
            }
        )
    return {"base_url": scrape_result.base_url, "pages": pages}


def _format_tech_stack(stack: TechnologyStack) -> dict[str, list[str]]:
    return {
        "frontend": [item.name for item in stack.frontend],
        "backend": [item.name for item in stack.backend],
        "database": [item.name for item in stack.database],
        "hosting": [item.name for item in stack.hosting],
        "analytics": [item.name for item in stack.analytics],
        "payments": [item.name for item in stack.payments],
    }


def _fallback_ai(scrape_result: ScrapeResult, stack: TechnologyStack) -> dict[str, Any]:
    company_name = _fallback_company_name(scrape_result.base_url)
    description = (
        scrape_result.pages[0].descriptions[0]
        if scrape_result.pages and scrape_result.pages[0].descriptions
        else "AI-assisted product analysis."
    )
    return {
        "company_name": company_name,
        "description": description,
        "industry": "SaaS",
        "startup_summary": description,
        "target_customers": "Digital-first teams evaluating new SaaS products.",
        "problem_solved": "Helps teams understand product positioning and stack quickly.",
        "core_features": [
            "Website analysis",
            "Technology detection",
            "AI insights report",
        ],
        "business_model": "Subscription SaaS",
        "revenue_strategy": "Tiered plans based on report volume and depth",
        "competitive_advantages": ["Speed", "Actionable insights"],
        "weaknesses": ["Limited data sources without full crawl"],
        "market_category": "Market intelligence",
        "roadmap": [
            "Deep crawl coverage",
            "Competitor benchmarking",
            "Team collaboration",
        ],
        "tech_stack": _format_tech_stack(stack),
        "scrape_summary": _compact_scrape(scrape_result),
    }


async def generate_ai_analysis(
    scrape_result: ScrapeResult, tech_stack: TechnologyStack
) -> dict[str, Any]:
    prompt = (
        "You are an analyst generating a structured JSON report for a SaaS product. "
        "Return ONLY valid JSON with the exact keys in the schema below."
        "\n\nSchema:"
        "{"
        '"company_name": string,'
        '"description": string,'
        '"industry": string,'
        '"startup_summary": string,'
        '"target_customers": string,'
        '"problem_solved": string,'
        '"core_features": string[],'
        '"business_model": string,'
        '"revenue_strategy": string,'
        '"competitive_advantages": string[],'
        '"weaknesses": string[],'
        '"market_category": string,'
        '"roadmap": string[]'
        "}"
        "\n\nInput data:"
        f"\nScrape: {_compact_scrape(scrape_result)}"
        f"\nDetected stack: {_format_tech_stack(tech_stack)}"
    )

    data = await generate_json(prompt)
    if not data:
        return _fallback_ai(scrape_result, tech_stack)

    data.setdefault("company_name", _fallback_company_name(scrape_result.base_url))
    data.setdefault("industry", "SaaS")
    data["tech_stack"] = _format_tech_stack(tech_stack)
    data["scrape_summary"] = _compact_scrape(scrape_result)
    return data
