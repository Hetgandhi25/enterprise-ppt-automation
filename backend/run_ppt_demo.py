import logging
from pathlib import Path

from backend.utils.logger import setup_logging
from backend.processors.process_inventory import InventoryProcessor
from backend.processors.process_sla import SLAProcessor
from backend.processors.process_incident import IncidentProcessor
from backend.charts.chart_generator import generate_sla_chart, generate_ticket_chart
from backend.ppt.ppt_generator import PPTGenerator

def run_ppt_demo():
    setup_logging()
    logger = logging.getLogger("ppt_demo")
    
    base_dir = Path(__file__).parent
    fixtures_dir = base_dir / "tests" / "fixtures"
    template_path = base_dir / "templates" / "ServiceReview.pptx"
    out_dir = base_dir / "output" / "presentations"
    
    logger.info("Starting PPT Demo pipeline.")
    
    customer_id = "ASG India"
    month = "2026-07"
    
    # 1. Processors
    inv_proc = InventoryProcessor(fixtures_dir / "Customer_Service_Report.xlsx")
    inv_records = inv_proc.process([customer_id])
    
    sla_proc = SLAProcessor(fixtures_dir / "SLA_Report.xlsx", fixtures_dir / "Location_SLA_Report.xlsx")
    sla_records, below_sla, major_dt = sla_proc.process([customer_id], ["2026-05", "2026-06", month])
    
    inc_proc = IncidentProcessor(fixtures_dir / "Incident_Report.xlsx")
    inc_records = inc_proc.process([customer_id])
    
    # 2. Charts
    clean_cust = customer_id.replace(" ", "_")
    sla_chart = generate_sla_chart(sla_records, clean_cust, month)
    ticket_chart = generate_ticket_chart(sla_records, clean_cust, month)
    
    # 3. PPT
    generator = PPTGenerator(template_path)
    data = {
        "customer_name": customer_id,
        "report_month": month,
        "inventory_records": inv_records,
        "sla_chart_path": sla_chart,
        "ticket_chart_path": ticket_chart,
        "below_sla": below_sla,
        "major_dt": major_dt,
        "incident_records": inc_records
    }
    
    final_path = out_dir / f"{clean_cust}_{month}.pptx"
    generator.generate(data, final_path)
    logger.info(f"Demo complete! Output: {final_path}")
    print(f"Final Presentation generated at: {final_path}")

if __name__ == "__main__":
    run_ppt_demo()
