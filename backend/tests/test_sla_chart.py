import pytest
from pathlib import Path
from backend.charts.sla_chart import SLATrendChart
from backend.models.domain import SLARecord
from backend.utils.exceptions import ChartGenerationError

def test_sla_chart_happy_path(tmp_path):
    output = tmp_path / "sla_trend.png"
    data = [
        SLARecord(month="2026-05", sla_percentage=99.8, ticket_count=10),
        SLARecord(month="2026-06", sla_percentage=98.5, ticket_count=15),
        SLARecord(month="2026-07", sla_percentage=100.0, ticket_count=5),
    ]
    
    chart = SLATrendChart(data, output)
    result_path = chart.generate()
    
    assert result_path.exists()
    assert result_path.stat().st_size > 0

def test_sla_chart_empty_data(tmp_path):
    output = tmp_path / "sla_trend.png"
    chart = SLATrendChart([], output)
    
    with pytest.raises(ChartGenerationError, match="Empty data"):
        chart.generate()

def test_sla_chart_invalid_sla(tmp_path):
    output = tmp_path / "sla_trend.png"
    data = [SLARecord.model_construct(month="2026-05", sla_percentage=105.0, ticket_count=10)]
    chart = SLATrendChart(data, output)
    
    with pytest.raises(ChartGenerationError, match="Invalid SLA percentage"):
        chart.generate()

def test_sla_chart_duplicate_months(tmp_path):
    output = tmp_path / "sla_trend.png"
    data = [
        SLARecord(month="2026-05", sla_percentage=99.8, ticket_count=10),
        SLARecord(month="2026-05", sla_percentage=98.5, ticket_count=15),
    ]
    chart = SLATrendChart(data, output)
    
    with pytest.raises(ChartGenerationError, match="Duplicate month"):
        chart.generate()
