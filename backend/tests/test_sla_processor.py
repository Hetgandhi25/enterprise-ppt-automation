import pytest
from pathlib import Path
from backend.processors.process_sla import SLAProcessor

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_sla_processor_happy_path():
    processor = SLAProcessor(
        FIXTURES_DIR / "SLA_Report.xlsx", 
        FIXTURES_DIR / "Location_SLA_Report.xlsx"
    )
    records, below_sla, major_dt = processor.process(
        customer_names=["ASG India"],
        target_months=["2026-05", "2026-06", "2026-07"]
    )
    
    assert len(records) > 0
    assert records[0].month in ["2026-05", "2026-06", "2026-07"]
    assert isinstance(below_sla, list)
    assert isinstance(major_dt, list)
