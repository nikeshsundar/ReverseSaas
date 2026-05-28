from __future__ import annotations

from app.schemas.architecture import ArchitectureEdge, ArchitectureGraph, ArchitectureNode
from app.schemas.technology import TechnologyStack


def generate_architecture(stack: TechnologyStack) -> ArchitectureGraph:
    nodes: list[ArchitectureNode] = []
    edges: list[ArchitectureEdge] = []

    nodes.append(ArchitectureNode(id="user", label="Users", category="client", x=0, y=0))
    nodes.append(
        ArchitectureNode(
            id="frontend",
            label=stack.frontend[0].name if stack.frontend else "Web App",
            category="frontend",
            x=180,
            y=0,
        )
    )
    nodes.append(ArchitectureNode(id="api", label="API", category="backend", x=360, y=0))
    nodes.append(
        ArchitectureNode(
            id="database",
            label=stack.database[0].name if stack.database else "PostgreSQL",
            category="database",
            x=540,
            y=0,
        )
    )
    nodes.append(ArchitectureNode(id="auth", label="Auth", category="security", x=360, y=120))
    nodes.append(
        ArchitectureNode(id="cache", label="Cache", category="infra", x=540, y=120)
    )
    nodes.append(
        ArchitectureNode(id="storage", label="Object Storage", category="infra", x=540, y=-120)
    )

    if stack.payments:
        nodes.append(
            ArchitectureNode(
                id="payments",
                label=stack.payments[0].name,
                category="payments",
                x=360,
                y=-120,
            )
        )
        edges.append(ArchitectureEdge(id="api-payments", source="api", target="payments"))

    if stack.analytics:
        nodes.append(
            ArchitectureNode(
                id="analytics",
                label=stack.analytics[0].name,
                category="analytics",
                x=180,
                y=120,
            )
        )
        edges.append(
            ArchitectureEdge(id="frontend-analytics", source="frontend", target="analytics")
        )

    edges.extend(
        [
            ArchitectureEdge(id="user-frontend", source="user", target="frontend"),
            ArchitectureEdge(id="frontend-api", source="frontend", target="api"),
            ArchitectureEdge(id="api-db", source="api", target="database"),
            ArchitectureEdge(id="api-auth", source="api", target="auth"),
            ArchitectureEdge(id="api-cache", source="api", target="cache"),
            ArchitectureEdge(id="api-storage", source="api", target="storage"),
        ]
    )

    return ArchitectureGraph(nodes=nodes, edges=edges)
