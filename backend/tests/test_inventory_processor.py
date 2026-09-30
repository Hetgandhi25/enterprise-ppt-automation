import pytest
from pathlib import Path
from backend.processors.process_inventory import InventoryProcessor
from backend.utils.exceptions import ExcelValidationError, CustomerNotFoundError

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_inventory_processor_happy_path():
    processor = InventoryProcessor(FIXTURES_DIR / "Customer_Service_Report.xlsx")
    records, metrics = processor.process(["ASG India"])
    
    assert len(records) > 0
    assert records[0].customer_name == "ASG India"
    assert records[0].link_count >= 0

def test_inventory_processor_customer_not_found():
    processor = InventoryProcessor(FIXTURES_DIR / "Customer_Service_Report.xlsx")
    with pytest.raises(CustomerNotFoundError):
        processor.process(["Unknown Customer Corp"])
