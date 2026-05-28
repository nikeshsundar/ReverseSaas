from __future__ import annotations

from dataclasses import dataclass

from app.schemas.technology import TechnologySignal, TechnologyStack
from app.schemas.scrape import ScrapeResult


@dataclass(frozen=True)
class TechSignature:
    name: str
    category: str
    tokens: tuple[str, ...]


SIGNATURES: list[TechSignature] = [
    TechSignature("Next.js", "frontend", ("__next_data__", "_next", "next/router")),
    TechSignature("React", "frontend", ("react", "data-reactroot", "react-dom")),
    TechSignature("Vue", "frontend", ("vue", "data-v-", "__vue")),
    TechSignature("Angular", "frontend", ("ng-version", "angular", "ng-app")),
    TechSignature("Stripe", "payments", ("stripe", "js.stripe.com", "checkout.stripe.com")),
    TechSignature("Supabase", "database", ("supabase", "supabase.co")),
    TechSignature("Firebase", "database", ("firebase", "firebaseio.com")),
    TechSignature("PostHog", "analytics", ("posthog", "app.posthog.com")),
    TechSignature("Plausible", "analytics", ("plausible", "plausible.io")),
    TechSignature("Cloudflare", "hosting", ("cloudflare", "cf-ray")),
    TechSignature("Vercel", "hosting", ("vercel", "vercel-insights")),
    TechSignature("AWS", "hosting", ("amazonaws.com", "aws-", "cloudfront")),
]


def _collect_haystack(scrape_result: ScrapeResult) -> str:
    parts: list[str] = []
    for page in scrape_result.pages:
        parts.extend(page.headings)
        parts.extend(page.descriptions)
        parts.extend(page.pricing)
        parts.extend(page.links)
        for key, value in (page.metadata or {}).items():
            if isinstance(value, str):
                parts.append(value)
            elif isinstance(value, list):
                parts.extend([str(item) for item in value])
    return " ".join(parts).lower()


def _score(matches: int) -> float:
    if matches <= 0:
        return 0.0
    return min(0.95, 0.35 + 0.2 * matches)


def detect_technology(scrape_result: ScrapeResult) -> TechnologyStack:
    haystack = _collect_haystack(scrape_result)
    buckets = {
        "frontend": [],
        "backend": [],
        "database": [],
        "hosting": [],
        "analytics": [],
        "payments": [],
    }

    for signature in SIGNATURES:
        matches = sum(1 for token in signature.tokens if token in haystack)
        confidence = _score(matches)
        if confidence <= 0.0:
            continue
        buckets[signature.category].append(
            TechnologySignal(name=signature.name, confidence=round(confidence, 2))
        )

    return TechnologyStack(
        frontend=buckets["frontend"],
        backend=buckets["backend"],
        database=buckets["database"],
        hosting=buckets["hosting"],
        analytics=buckets["analytics"],
        payments=buckets["payments"],
    )
