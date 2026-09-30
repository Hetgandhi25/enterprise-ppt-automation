from pathlib import Path
from typing import List

from backend.charts.sla_chart import SLATrendChart
from backend.charts.ticket_chart import TicketTrendChart
from backend.charts.location_sla_chart import LocationSLAChart
from backend.charts.service_request_chart import ServiceRequestChart
from backend.charts.incident_summary_chart import IncidentSummaryChart
from backend.models.domain import SLARecord, IncidentRecord
from typing import Dict

def generate_sla_chart(records: List[SLARecord], customer_id: str, month: str) -> Path:
    """Helper to generate the SLA chart for a customer."""
    output_path = Path("output") / "charts" / f"sla_trend_{customer_id}_{month}.png"
    chart = SLATrendChart(records, output_path)
    return chart.generate()

def generate_ticket_chart(records: List[SLARecord], customer_id: str, month: str) -> Path:
    """Helper to generate the Ticket chart for a customer."""
    output_path = Path("output") / "charts" / f"ticket_trend_{customer_id}_{month}.png"
    chart = TicketTrendChart(records, output_path)
    return chart.generate()

def generate_location_sla_chart(data: Dict[str, float], customer_id: str, month: str) -> Path:
    output_path = Path("output") / "charts" / f"location_sla_{customer_id}_{month}.png"
    chart = LocationSLAChart(data, output_path)
    return chart.generate()

def generate_sr_chart(flowchart_data: Dict[str, str], customer_id: str, month: str) -> Path:
    output_path = Path("output") / "charts" / f"service_requests_{customer_id}_{month}.png"
    chart = ServiceRequestChart(flowchart_data, output_path)
    return chart.generate()

def generate_incident_chart(records: List[IncidentRecord], customer_id: str, month: str) -> Path:
    output_path = Path("output") / "charts" / f"incident_summary_{customer_id}_{month}.png"
    chart = IncidentSummaryChart(records, output_path)
    return chart.generate()
