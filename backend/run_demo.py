from pathlib import Path
import logging
from backend.processors.process_sla import SLAProcessor
from backend.charts.chart_generator import generate_sla_chart, generate_ticket_chart
from backend.utils.logger import setup_logging

def run_demo():
    setup_logging()
    logger = logging.getLogger("demo")
    
    base_dir = Path(__file__).parent
    fixtures_dir = base_dir / "tests" / "fixtures"
    output_dir = base_dir / "output" / "charts"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("Starting demo generation.")
    
    # Process Data
    processor = SLAProcessor(
        fixtures_dir / "SLA_Report.xlsx", 
        fixtures_dir / "Location_SLA_Report.xlsx"
    )
    customer_id = "ASG_India"
    
    # Try finding ASG India
    try:
        sla_records, below_sla, major_dt = processor.process(
            customer_names=["ASG India"],
            target_months=["2026-05", "2026-06", "2026-07"]
        )
        logger.info(f"Successfully processed data for {customer_id}")
    except Exception as e:
        logger.error(f"Failed to process data: {e}")
        return
        
    # Generate Charts
    month = "2026-07"
    sla_chart_path = generate_sla_chart(sla_records, customer_id, month)
    ticket_chart_path = generate_ticket_chart(sla_records, customer_id, month)
    
    logger.info("Demo complete.")
    print(f"Generated {sla_chart_path}")
    print(f"Generated {ticket_chart_path}")

if __name__ == "__main__":
    run_demo()
