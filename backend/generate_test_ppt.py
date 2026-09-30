import logging
from pathlib import Path
from backend.ppt.ppt_generator import PPTGenerator

logging.basicConfig(level=logging.INFO)

def run():
    template_path = Path("backend/templates/MBR_Template_v1.pptx")
    manifest_path = Path("backend/templates/template_manifest.yaml")
    output_path = Path("backend/generated/ABC_Ltd_114475_August_2026.pptx")
    
    generator = PPTGenerator(template_path, manifest_path)
    
    # Mock Normalized Data Object
    mock_data = {
        # Slide 1
        "customer_name": "ABC Ltd - TEST RUN",
        "csm_name": "By: Mr. AI Agent",
        
        # Slide 3
        "mom_table": [
            ["1", "Discussed SLA drops", "Network Team", "Resolved", "2026-08-01"],
            ["2", "Upgrade Link bandwidth", "Sales", "In Progress", "2026-08-15"]
        ],
        
        # Slide 4
        "overall_service_status": "All services are operating at 99.9% uptime",
        "service_request_trend": "Trend is downward this month",
        "customer_sentiment_csat": "4.8/5",
        "customer_sentiment_nps": "75",
        "action_taken": "Proactive monitoring deployed on critical links.",
        
        # Slide 5
        "customer_entities": "5",
        "total_links": "120",
        "inventory_table": [
            ["HQ", "MPLS", "1"],
            ["Branch", "ILL", "10"],
            ["Store", "Broadband", "109"]
        ],
        
        # Slide 6
        "sla_trend_chart": {
            "categories": ["June", "July", "August"],
            "series": {
                "SLA %": [99.5, 99.8, 99.9]
            }
        },
        "service_request_chart": {
            "categories": ["June", "July", "August"],
            "series": {
                "Requests": [40, 35, 20]
            }
        },
        
        # Slide 7
        "location_sla_chart": {
            "categories": ["HQ", "Branch A", "Branch B"],
            "series": {
                "Uptime %": [100.0, 99.9, 99.5]
            }
        },
        
        # Slide 8
        "total_service_requests": "55",
        "total_requests": "10",
        "total_complaints": "45",
        "complaints_chart": {
            "categories": ["Power Issue", "Fiber Cut", "Router Fault"],
            "series": {
                "Count": [15, 20, 10]
            }
        },
        "proactive_reactive": "Proactive 10  Reactive 35",
        "issue_ishan_end_count": "20",
        "issue_customer_end_count": "25",
        
        # Slide 9
        "incident_table": [
            ["INC-001", "Fiber Cut", "10 hrs", "Resolved"],
            ["INC-002", "Router Config", "2 hrs", "Resolved"]
        ],
        
        # Slide 10
        "projects_table": [
            ["PRJ-99", "New Branch Setup", "On Track", "Sept 2026"]
        ],
        
        # Slide 11
        "retention_table": [
            ["Link 44", "Pending Customer Approval", "Aug 30"]
        ],
        
        # Slide 12
        "invoice_table": [
            ["INV-01", "July Service", "1,00,000", "Overdue", "15 Days"],
            ["INV-02", "August Service", "3,10,000", "Pending", "-"]
        ],
        "total_outstanding": "4,10,000",
        "open_invoices": "02",
        
        # Slide 13
        "escalation_table": [
            ["L1", "Support Desk", "support@abc.com", "9876543210"],
            ["L2", "Manager", "mgr@abc.com", "9876543211"]
        ]
    }
    
    generator.generate(mock_data, output_path)
    print(f"Test PPT successfully generated at: {output_path}")

if __name__ == "__main__":
    run()
