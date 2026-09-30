from pathlib import Path
from backend.ppt.ppt_generator import PPTGenerator

# Test 1
TEST_1 = {
    "customer_name": "ASG India",
    "csm_block": {"csm_name": "csm_asg"}
}

# Test 2
TEST_2 = {
    "customer_name": "ABC Ltd",
    "csm_block": {"csm_name": "rahul_patel"}
}

# Test 3
TEST_3 = {
    "customer_name": "XYZ Technologies",
    "csm_block": {"csm_name": "neha_shah"}
}

def fill_missing(data):
    # Fills the required charts/tables with empty defaults to prevent crashes during the test
    base = {
        "mom_table": [],
        "inventory_table": [],
        "sla_trend_chart": {"categories": [], "series": {}},
        "service_request_chart": {"categories": [], "series": {}},
        "location_sla_chart": {"categories": [], "series": {}},
        "complaints_chart": {"categories": [], "series": {}},
        "incident_table": [],
        "projects_table": [],
        "retention_table": [],
        "invoice_table": [],
        "escalation_table": []
    }
    base.update(data)
    return base

if __name__ == "__main__":
    template = Path("backend/templates/MBR_Template_v1.pptx")
    manifest = Path("backend/templates/template_manifest.yaml")
    
    generator = PPTGenerator(template, manifest)
    
    # Run tests
    for i, test_data in enumerate([TEST_1, TEST_2, TEST_3], 1):
        output = Path(f"backend/output/presentations/Regression_Test_{i}.pptx")
        generator.generate(fill_missing(test_data), output)
        print(f"Generated Regression_Test_{i}.pptx for {test_data['customer_name']} / {test_data['csm_block']['csm_name']}")
