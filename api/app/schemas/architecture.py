from __future__ import annotations

from pydantic import BaseModel


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
