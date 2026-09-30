import pytest
from pathlib import Path
from backend.charts.ticket_chart import TicketTrendChart
from backend.models.domain import SLARecord
from backend.utils.exceptions import ChartGenerationError

def test_ticket_chart_happy_path(tmp_path):
    output = tmp_path / "ticket_trend.png"
    data = [
        SLARecord(month="2026-05", sla_percentage=99.8, ticket_count=10),
        SLARecord(month="2026-06", sla_percentage=98.5, ticket_count=15),
        SLARecord(month="2026-07", sla_percentage=100.0, ticket_count=5),
    ]
    
    chart = TicketTrendChart(data, output)
    result_path = chart.generate()
    
    assert result_path.exists()
    assert result_path.stat().st_size > 0

def test_ticket_chart_negative_tickets(tmp_path):
    output = tmp_path / "ticket_trend.png"
    # Although pydantic model should block this, we test the validation layer in chart logic
    # We bypass pydantic validation for test using model_construct
    data = [SLARecord.model_construct(month="2026-05", sla_percentage=99.8, ticket_count=-5)]
    chart = TicketTrendChart(data, output)
    
    with pytest.raises(ChartGenerationError, match="Negative ticket count"):
        chart.generate()
