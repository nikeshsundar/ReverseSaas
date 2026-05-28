import time

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.schemas.analysis import (
    AnalyzeRequest,
    AnalyzeResponse,
    AnalysisResponse,
    CompetitorsResponse,
    CostsResponse,
    TechnologyResponse,
)
from app.core.config import get_settings
from app.core.errors import too_many_requests
from app.services.analysis_service import (
    get_analysis,
    get_competitors,
    get_costs,
    get_report_pdf,
    get_technology,
    start_analysis,
)

router = APIRouter()
_rate_bucket: dict[str, list[float]] = {}


def _get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


def _enforce_rate_limit(request: Request) -> None:
    now = time.time()
    settings = get_settings()
    rate_limit = settings.rate_limit_per_minute
    window_seconds = settings.rate_limit_window_seconds
    if rate_limit <= 0:
        return
    if window_seconds <= 0:
        window_seconds = 60
    ip = _get_client_ip(request)
    window_start = now - window_seconds
    bucket = [ts for ts in _rate_bucket.get(ip, []) if ts > window_start]
    if len(bucket) >= rate_limit:
        raise too_many_requests("Rate limit exceeded. Try again shortly.")
    bucket.append(now)
    _rate_bucket[ip] = bucket


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: Request, payload: AnalyzeRequest) -> AnalyzeResponse:
    _enforce_rate_limit(request)
    return await start_analysis(str(payload.url))


@router.get("/analysis/{analysis_id}", response_model=AnalysisResponse)
async def analysis_detail(analysis_id: str) -> AnalysisResponse:
    return await get_analysis(analysis_id)


@router.get("/technology/{analysis_id}", response_model=TechnologyResponse)
async def technology_detail(analysis_id: str) -> TechnologyResponse:
    return await get_technology(analysis_id)


@router.get("/competitors/{analysis_id}", response_model=CompetitorsResponse)
async def competitors_detail(analysis_id: str) -> CompetitorsResponse:
    return await get_competitors(analysis_id)


@router.get("/costs/{analysis_id}", response_model=CostsResponse)
async def costs_detail(analysis_id: str) -> CostsResponse:
    return await get_costs(analysis_id)


@router.get("/analysis/{analysis_id}/report")
async def analysis_report(analysis_id: str) -> StreamingResponse:
    pdf_bytes = await get_report_pdf(analysis_id)
    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=analysis-{analysis_id}.pdf",
        },
    )
