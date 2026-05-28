from __future__ import annotations

from pydantic import BaseModel


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
