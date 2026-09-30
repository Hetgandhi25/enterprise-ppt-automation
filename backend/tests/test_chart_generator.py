import pytest
from pathlib import Path
from backend.charts.chart_generator import generate_sla_chart, generate_ticket_chart
from backend.models.domain import SLARecord

def test_generate_sla_chart():
    records = [SLARecord.model_construct(month="2026-05", sla_percentage=99.0, ticket_count=10)]
    output_path = generate_sla_chart(records, "TEST_CUST", "2026-05")
    assert output_path.exists()
    assert "sla_trend_TEST_CUST_2026-05.png" in output_path.name
    output_path.unlink() # cleanup

def test_generate_ticket_chart():
    records = [SLARecord.model_construct(month="2026-05", sla_percentage=99.0, ticket_count=10)]
    output_path = generate_ticket_chart(records, "TEST_CUST", "2026-05")
    assert output_path.exists()
    assert "ticket_trend_TEST_CUST_2026-05.png" in output_path.name
    output_path.unlink() # cleanup
