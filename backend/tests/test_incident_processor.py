import pytest
from pathlib import Path
from backend.processors.process_incident import IncidentProcessor

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_incident_processor_happy_path():
    processor = IncidentProcessor(FIXTURES_DIR / "Incident_Report.xlsx")
    results = processor.process(["ASG India"])
    
    assert len(results) > 0
    # The dummy data should produce some records with locations
    assert results[0].location is not None
    assert results[0].cable_issue >= 0
