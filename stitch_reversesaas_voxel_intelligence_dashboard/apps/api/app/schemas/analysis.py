from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, HttpUrl


class AnalyzeRequest(BaseModel):
    url: HttpUrl


class AnalyzeResponse(BaseModel):
    id: str
    status: Literal["pending", "processing", "completed", "failed"]


class TechnologySignal(BaseModel):
    name: str
    confidence: float


class TechnologyStack(BaseModel):
    frontend: list[TechnologySignal]
    backend: list[TechnologySignal]
    database: list[TechnologySignal]
    hosting: list[TechnologySignal]
    analytics: list[TechnologySignal]
    payments: list[TechnologySignal]


class FeatureItem(BaseModel):
    title: str
    description: str


class CompetitorItem(BaseModel):
    name: str
    description: str


class CostBreakdown(BaseModel):
    hosting: float
    database: float
    storage: float
    bandwidth: float
    total: float


class CostEstimate(BaseModel):
    users_100: CostBreakdown
    users_1000: CostBreakdown
    users_10000: CostBreakdown
    users_100000: CostBreakdown


class ArchitectureNode(BaseModel):
    id: str
    label: str
    category: str
    x: float
    y: float


class ArchitectureEdge(BaseModel):
    id: str
    source: str
    target: str


class ArchitectureGraph(BaseModel):
    nodes: list[ArchitectureNode]
    edges: list[ArchitectureEdge]


class AIInsights(BaseModel):
    startup_summary: str
    target_customers: str
    problem_solved: str
    core_features: list[str]
    business_model: str
    revenue_strategy: str
    competitive_advantages: list[str]
    weaknesses: list[str]
    market_category: str
    roadmap: list[str]


class AnalysisResponse(BaseModel):
    id: str
    url: str
    company_name: str | None
    description: str | None
    industry: str | None
    created_at: datetime
    status: Literal["pending", "processing", "completed", "failed"]
    error: str | None = None
    ai_insights: AIInsights | None = None
    architecture: ArchitectureGraph | None = None
    features: list[FeatureItem] = []
    competitors: list[CompetitorItem] = []
    cost_estimate: CostEstimate | None = None
    technology_stack: TechnologyStack | None = None
    metadata: dict[str, Any] | None = None


class TechnologyResponse(BaseModel):
    analysis_id: str
    stack: TechnologyStack | None


class CompetitorsResponse(BaseModel):
    analysis_id: str
    competitors: list[CompetitorItem]


class CostsResponse(BaseModel):
    analysis_id: str
    costs: CostEstimate | None
