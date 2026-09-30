from pathlib import Path
from backend.ppt.ppt_generator import PPTGenerator

# Exact sample values from Sample MBR PPT_Formatted.pptx
REFERENCE_DATA = {
    "customer_name": "ABC Ltd",
    "csm_block": {
        "csm_name": "By: Mr. XYZ",
        "csm_designation": "Customer success Manager-Udaipur",
        "csm_company": "Ishan Technologies"
    },
    "mom_table": [
        ["1", "Customer required 100 Mbps link at Ahmedabad", "ASG", "Open", "15 Aug"]
    ],
    "overall_service_status": "All services operating normally.",
    "service_request_trend": "Stable",
    "customer_sentiment_csat": "N/A",
    "customer_sentiment_nps": "N/A",
    "action_taken": "Standard maintenance",
    
    "customer_entities": "02",
    "total_links": "52",
    "inventory_table": [
        ["ABC Ltd", "ILL", 52],
        ["ABC Ltd", "L2", 50]
    ],
    
    "sla_trend_chart": {
        "categories": ["Apr", "May", "Jun"],
        "series": {"SLA %": [99.5, 99.8, 99.4]}
    },
    "service_request_chart": {
        "categories": ["Apr", "May", "Jun"],
        "series": {"Requests": [25, 24, 28]}
    },
    "location_sla_chart": {
        "categories": ["Mumbai", "Bangalore"],
        "series": {"Uptime %": [99.0, 99.1]}
    },
    
    "total_service_requests": "35",
    "total_requests": "5",
    "total_complaints": "30",
    "complaints_chart": {
        "categories": ["Proactive", "Reactive", "Ishan End", "Customer End"],
        "series": {"Count": [5, 25, 18, 7]}
    },
    "proactive_reactive": "Proactive 5 Reactive 25",
    "issue_ishan_end_count": "18",
    "issue_customer_end_count": "7",
    
    "incident_table": [
        ["Mumbai", 1, 0, 0],
        ["Bangalore", 0, 1, 0]
    ],
    "projects_table": [
        ["Kalina", "In Progress", "Fiber laid", "15 Aug"]
    ],
    "retention_table": [
        ["Kalina", "Pending", "15 Aug"]
    ],
    "invoice_table": [
        ["INV-001", "July", "4,10,000", "Unpaid", "30 Days"],
        ["INV-002", "July", "10,000", "Unpaid", "30 Days"],
        ["INV-003", "July", "5,000", "Unpaid", "30 Days"]
    ],
    "total_outstanding": "₹4,10,000",
    "open_invoices": "03",
    "escalation_table": [
        ["L1", "Support", "support@ishan.com", "1800-123"]
    ]
}

if __name__ == "__main__":
    template = Path("backend/templates/MBR_Template_v1.pptx")
    manifest = Path("backend/templates/template_manifest.yaml")
    output = Path("backend/output/presentations/Regression_Test.pptx")
    
    generator = PPTGenerator(template, manifest)
    generator.generate(REFERENCE_DATA, output)
    print(f"Regression reference PPT generated at {output}")
