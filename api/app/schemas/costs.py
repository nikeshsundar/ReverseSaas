from __future__ import annotations

from pydantic import BaseModel


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
