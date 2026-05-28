from __future__ import annotations

from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.schemas.analysis import AnalysisResponse


def _draw_section(c: canvas.Canvas, title: str, lines: list[str], y: float) -> float:
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, title)
    y -= 16
    c.setFont("Helvetica", 10)
    for line in lines:
        if y < 72:
            c.showPage()
            y = 740
            c.setFont("Helvetica", 10)
        c.drawString(60, y, line[:110])
        y -= 14
    return y - 6


def generate_pdf_report(analysis: AnalysisResponse) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    y = 760

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "ReverseSaaS Report")
    y -= 24

    summary_lines = [
        f"Company: {analysis.company_name or 'Unknown'}",
        f"URL: {analysis.url}",
        f"Industry: {analysis.industry or 'N/A'}",
        f"Created: {analysis.created_at.isoformat()}",
    ]
    y = _draw_section(c, "Overview", summary_lines, y)

    if analysis.ai_insights:
        ai = analysis.ai_insights
        y = _draw_section(
            c,
            "AI Insights",
            [
                f"Summary: {ai.startup_summary}",
                f"Target customers: {ai.target_customers}",
                f"Problem solved: {ai.problem_solved}",
                f"Business model: {ai.business_model}",
                f"Revenue strategy: {ai.revenue_strategy}",
                f"Market category: {ai.market_category}",
            ],
            y,
        )

    if analysis.technology_stack:
        stack_lines = [
            f"Frontend: {[item.name for item in analysis.technology_stack.frontend]}",
            f"Backend: {[item.name for item in analysis.technology_stack.backend]}",
            f"Database: {[item.name for item in analysis.technology_stack.database]}",
            f"Hosting: {[item.name for item in analysis.technology_stack.hosting]}",
            f"Analytics: {[item.name for item in analysis.technology_stack.analytics]}",
            f"Payments: {[item.name for item in analysis.technology_stack.payments]}",
        ]
        y = _draw_section(c, "Technology Stack", stack_lines, y)

    if analysis.features:
        feature_lines = [f"{item.title}: {item.description}" for item in analysis.features]
        y = _draw_section(c, "Core Features", feature_lines, y)

    if analysis.competitors:
        comp_lines = [f"{item.name}: {item.description}" for item in analysis.competitors]
        y = _draw_section(c, "Competitors", comp_lines, y)

    if analysis.cost_estimate:
        cost = analysis.cost_estimate
        cost_lines = [
            f"100 users: ${cost.users_100.total}",
            f"1,000 users: ${cost.users_1000.total}",
            f"10,000 users: ${cost.users_10000.total}",
            f"100,000 users: ${cost.users_100000.total}",
        ]
        _draw_section(c, "Cost Estimates", cost_lines, y)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()
