from __future__ import annotations

from pydantic import BaseModel


class GeminiAnalysis(BaseModel):
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


class CompetitorInsight(BaseModel):
    top_competitors: list[str]
    alternative_products: list[str]
    market_positioning: str
    advantages: list[str]
    disadvantages: list[str]
