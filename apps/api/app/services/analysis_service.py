from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any

from app.core.db import prisma
from app.core.errors import not_found
from app.schemas.analysis import (
    AIInsights,
    AnalyzeResponse,
    AnalysisResponse,
    CompetitorItem,
    CompetitorsResponse,
    CostEstimate,
    CostsResponse,
    FeatureItem,
    TechnologyResponse,
    TechnologyStack,
)
from app.schemas.architecture import ArchitectureGraph
from app.schemas.scrape import ScrapeResult
from app.services.ai_analysis import generate_ai_analysis
from app.services.architecture import generate_architecture
from app.services.competitor_discovery import discover_competitors
from app.services.cost_estimator import estimate_costs
from app.services.reporting import generate_pdf_report
from app.services.scraper import scrape_site
from app.services.tech_detector import detect_technology
from app.services.url_safety import ensure_public_url


logger = logging.getLogger(__name__)


async def mark_stale_analyses(max_age_minutes: int = 30) -> None:
    cutoff = datetime.utcnow() - timedelta(minutes=max_age_minutes)
    await prisma.analysis.update_many(
        where={"status": "processing", "created_at": {"lt": cutoff}},
        data={"status": "failed", "error": "Analysis timed out."},
    )


def _normalize_ai(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "startup_summary": payload.get("startup_summary", ""),
        "target_customers": payload.get("target_customers", ""),
        "problem_solved": payload.get("problem_solved", ""),
        "core_features": payload.get("core_features") or [],
        "business_model": payload.get("business_model", ""),
        "revenue_strategy": payload.get("revenue_strategy", ""),
        "competitive_advantages": payload.get("competitive_advantages") or [],
        "weaknesses": payload.get("weaknesses") or [],
        "market_category": payload.get("market_category", ""),
        "roadmap": payload.get("roadmap") or [],
    }


async def start_analysis(url: str) -> AnalyzeResponse:
    await ensure_public_url(url)
    analysis = await prisma.analysis.create(
        data={
            "url": url,
            "status": "processing",
        }
    )
    asyncio.create_task(_process_analysis(analysis.id, url))
    return AnalyzeResponse(id=analysis.id, status=analysis.status)


async def _process_analysis(analysis_id: str, url: str) -> None:
    try:
        scrape_result = await scrape_site(url)
        tech_stack = detect_technology(scrape_result)
        ai_payload = await generate_ai_analysis(scrape_result, tech_stack)
        competitor_payload = await discover_competitors(scrape_result, tech_stack)
        costs = estimate_costs(tech_stack)
        architecture = generate_architecture(tech_stack)

        await _store_results(
            analysis_id,
            scrape_result,
            tech_stack,
            ai_payload,
            competitor_payload,
            costs,
            architecture,
        )
    except Exception as exc:
        logger.exception("Analysis failed for %s", analysis_id)
        await prisma.analysis.update(
            where={"id": analysis_id},
            data={"status": "failed", "error": str(exc)},
        )


async def _store_results(
    analysis_id: str,
    scrape_result: ScrapeResult,
    tech_stack: TechnologyStack,
    ai_payload: dict[str, Any],
    competitor_payload: dict[str, Any],
    costs: CostEstimate,
    architecture: ArchitectureGraph,
) -> None:
    ai_insights = _normalize_ai(ai_payload)
    metadata = {
        "scrape_summary": ai_payload.get("scrape_summary"),
        "tech_stack": ai_payload.get("tech_stack"),
        "competitor_insights": competitor_payload,
        "pages": [page.model_dump() for page in scrape_result.pages],
    }

    await prisma.analysis.update(
        where={"id": analysis_id},
        data={
            "company_name": ai_payload.get("company_name"),
            "description": ai_payload.get("description"),
            "industry": ai_payload.get("industry"),
            "status": "completed",
            "ai_insights": ai_insights,
            "architecture": architecture.model_dump(),
            "metadata": metadata,
        },
    )

    await prisma.feature.delete_many(where={"analysis_id": analysis_id})
    await prisma.competitor.delete_many(where={"analysis_id": analysis_id})

    await prisma.technology_stack.upsert(
        where={"analysis_id": analysis_id},
        data={
            "create": {
                "analysis_id": analysis_id,
                "frontend": [item.model_dump() for item in tech_stack.frontend],
                "backend": [item.model_dump() for item in tech_stack.backend],
                "database": [item.model_dump() for item in tech_stack.database],
                "hosting": [item.model_dump() for item in tech_stack.hosting],
                "analytics": [item.model_dump() for item in tech_stack.analytics],
                "payments": [item.model_dump() for item in tech_stack.payments],
            },
            "update": {
                "frontend": [item.model_dump() for item in tech_stack.frontend],
                "backend": [item.model_dump() for item in tech_stack.backend],
                "database": [item.model_dump() for item in tech_stack.database],
                "hosting": [item.model_dump() for item in tech_stack.hosting],
                "analytics": [item.model_dump() for item in tech_stack.analytics],
                "payments": [item.model_dump() for item in tech_stack.payments],
            },
        },
    )

    core_features = ai_insights.get("core_features") or []
    if not isinstance(core_features, list):
        core_features = []
    core_features = core_features[:12]
    feature_rows = [
        {
            "analysis_id": analysis_id,
            "title": feature,
            "description": ai_payload.get("startup_summary", "AI-identified feature."),
        }
        for feature in core_features
    ]
    if feature_rows:
        await prisma.feature.create_many(data=feature_rows)

    top_competitors = competitor_payload.get("top_competitors") or []
    if not isinstance(top_competitors, list):
        top_competitors = []
    top_competitors = top_competitors[:12]
    competitor_rows = []
    for competitor in top_competitors:
        if isinstance(competitor, dict):
            name = competitor.get("name", "Competitor")
            description = competitor.get("description", "")
        else:
            name = str(competitor)
            description = ""
        competitor_rows.append(
            {
                "analysis_id": analysis_id,
                "name": name,
                "description": description,
            }
        )
    if competitor_rows:
        await prisma.competitor.create_many(data=competitor_rows)

    await prisma.cost_estimate.upsert(
        where={"analysis_id": analysis_id},
        data={
            "create": {
                "analysis_id": analysis_id,
                "users_100": costs.users_100.model_dump(),
                "users_1000": costs.users_1000.model_dump(),
                "users_10000": costs.users_10000.model_dump(),
                "users_100000": costs.users_100000.model_dump(),
            },
            "update": {
                "users_100": costs.users_100.model_dump(),
                "users_1000": costs.users_1000.model_dump(),
                "users_10000": costs.users_10000.model_dump(),
                "users_100000": costs.users_100000.model_dump(),
            },
        },
    )


async def get_analysis(analysis_id: str) -> AnalysisResponse:
    record = await prisma.analysis.find_unique(
        where={"id": analysis_id},
        include={
            "features": True,
            "competitors": True,
            "technology_stack": True,
            "cost_estimate": True,
        },
    )

    if not record:
        raise not_found("Analysis")

    stack = _map_technology(record.technology_stack)
    costs = _map_costs(record.cost_estimate)
    features = [FeatureItem(title=item.title, description=item.description) for item in record.features]
    competitors = [
        CompetitorItem(name=item.name, description=item.description)
        for item in record.competitors
    ]
    ai_insights = _map_ai(record.ai_insights)
    architecture = _map_architecture(record.architecture)

    return AnalysisResponse(
        id=record.id,
        url=record.url,
        company_name=record.company_name,
        description=record.description,
        industry=record.industry,
        created_at=record.created_at,
        status=record.status,
        error=record.error,
        ai_insights=ai_insights,
        architecture=architecture,
        features=features,
        competitors=competitors,
        cost_estimate=costs,
        technology_stack=stack,
        metadata=_sanitize_metadata(record.metadata),
    )


async def get_technology(analysis_id: str) -> TechnologyResponse:
    record = await prisma.technology_stack.find_unique(
        where={"analysis_id": analysis_id}
    )
    if not record:
        return TechnologyResponse(analysis_id=analysis_id, stack=None)
    return TechnologyResponse(analysis_id=analysis_id, stack=_map_technology(record))


async def get_competitors(analysis_id: str) -> CompetitorsResponse:
    records = await prisma.competitor.find_many(where={"analysis_id": analysis_id})
    competitors = [
        CompetitorItem(name=item.name, description=item.description) for item in records
    ]
    return CompetitorsResponse(analysis_id=analysis_id, competitors=competitors)


async def get_costs(analysis_id: str) -> CostsResponse:
    record = await prisma.cost_estimate.find_unique(where={"analysis_id": analysis_id})
    return CostsResponse(analysis_id=analysis_id, costs=_map_costs(record))


async def get_report_pdf(analysis_id: str) -> bytes:
    analysis = await get_analysis(analysis_id)
    return generate_pdf_report(analysis)


def _map_technology(record: Any | None) -> TechnologyStack | None:
    if not record:
        return None
    return TechnologyStack(
        frontend=record.frontend or [],
        backend=record.backend or [],
        database=record.database or [],
        hosting=record.hosting or [],
        analytics=record.analytics or [],
        payments=record.payments or [],
    )


def _map_costs(record: Any | None) -> CostEstimate | None:
    if not record:
        return None
    return CostEstimate(
        users_100=record.users_100,
        users_1000=record.users_1000,
        users_10000=record.users_10000,
        users_100000=record.users_100000,
    )


def _map_ai(ai_data: Any | None) -> AIInsights | None:
    if not ai_data:
        return None
    return AIInsights(**_normalize_ai(ai_data))


def _map_architecture(data: Any | None) -> ArchitectureGraph | None:
    if not data:
        return None
    return ArchitectureGraph(**data)


def _sanitize_metadata(metadata: Any | None) -> dict[str, Any] | None:
    if not isinstance(metadata, dict):
        return None
    allowed = {
        "scrape_summary": metadata.get("scrape_summary"),
        "tech_stack": metadata.get("tech_stack"),
        "competitor_insights": metadata.get("competitor_insights"),
    }
    return {key: value for key, value in allowed.items() if value is not None}
