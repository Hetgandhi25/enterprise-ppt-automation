import pytest
from pathlib import Path
from backend.ppt.ppt_generator import PPTGenerator
from backend.ppt.ppt_loader import load_presentation
from backend.utils.exceptions import PPTGenerationError

def test_ppt_loader_not_found(tmp_path):
    with pytest.raises(PPTGenerationError, match="Template not found"):
        load_presentation(tmp_path / "non_existent.pptx")

def test_ppt_generator_happy_path(tmp_path):
    # This requires the dummy template to exist.
    template_path = Path(__file__).parent.parent.parent / "templates" / "ServiceReview.pptx"
    if not template_path.exists():
        pytest.skip("Dummy template not generated yet.")
        
    generator = PPTGenerator(template_path)
    
    # Create dummy images for charts
    from PIL import Image
    img_path = tmp_path / "dummy.png"
    img = Image.new('RGB', (10, 10), color = 'red')
    img.save(img_path)
    
    output_path = tmp_path / "output.pptx"
    
    data = {
        "customer_name": "ASG India",
        "report_month": "July 2026",
        "inventory_records": [],
        "sla_chart_path": img_path,
        "ticket_chart_path": img_path,
        "below_sla": [],
        "major_dt": [],
        "incident_records": []
    }
    
    result = generator.generate(data, output_path)
    assert result.exists()
    
    # Load and verify it can be read
    prs = load_presentation(result)
    assert len(prs.slides) == 4
