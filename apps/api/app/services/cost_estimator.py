from __future__ import annotations

from app.schemas.costs import CostBreakdown, CostEstimate
from app.schemas.technology import TechnologyStack


def _build_breakdown(hosting: float, database: float, storage: float, bandwidth: float) -> CostBreakdown:
    total = hosting + database + storage + bandwidth
    return CostBreakdown(
        hosting=round(hosting, 2),
        database=round(database, 2),
        storage=round(storage, 2),
        bandwidth=round(bandwidth, 2),
        total=round(total, 2),
    )


def estimate_costs(stack: TechnologyStack) -> CostEstimate:
    hosting_base = 45.0
    database_base = 30.0
    storage_base = 12.0
    bandwidth_base = 18.0

    host_names = {item.name for item in stack.hosting}
    if "AWS" in host_names:
        hosting_base += 25.0
    if "Vercel" in host_names:
        hosting_base += 10.0
    if "Cloudflare" in host_names:
        bandwidth_base -= 3.0

    scale = {
        100: 1.0,
        1000: 3.5,
        10000: 10.5,
        100000: 32.0,
    }

    return CostEstimate(
        users_100=_build_breakdown(
            hosting_base * scale[100],
            database_base * scale[100],
            storage_base * scale[100],
            bandwidth_base * scale[100],
        ),
        users_1000=_build_breakdown(
            hosting_base * scale[1000],
            database_base * scale[1000],
            storage_base * scale[1000],
            bandwidth_base * scale[1000],
        ),
        users_10000=_build_breakdown(
            hosting_base * scale[10000],
            database_base * scale[10000],
            storage_base * scale[10000],
            bandwidth_base * scale[10000],
        ),
        users_100000=_build_breakdown(
            hosting_base * scale[100000],
            database_base * scale[100000],
            storage_base * scale[100000],
            bandwidth_base * scale[100000],
        ),
    )
