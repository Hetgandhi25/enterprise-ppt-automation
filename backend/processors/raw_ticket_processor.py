import logging
from typing import List, Dict, Any, Tuple
from collections import defaultdict

from backend.models.domain import RawTicketRecord, SLARecord, IncidentRecord
from backend.processors.sla_calculator import SLACalculator

logger = logging.getLogger(__name__)

class RawTicketProcessor:
    """
    Processes Raw Ticket records to generate mathematically perfect data for Slides 6, 7, 8, and 9.
    Enforces rules from SLACalculator.
    """
    def __init__(self, tickets: List[RawTicketRecord]):
        self.tickets = tickets
        
    def process_all(self, target_months: List[str], sla_threshold: float = 99.5, downtime_threshold: float = 4.0, days_in_month: int = 30) -> Dict[str, Any]:
        """Runs all processors and returns a dictionary of data ready for PPT Generator."""
        
        # We only care about tickets in the target months for most metrics
        filtered_tickets = [t for t in self.tickets if t.month in target_months]
        
        slide6_data = self._generate_slide6_trend(filtered_tickets, days_in_month, target_months)
        below_sla, major_dt, sla_by_location = self._generate_slide7_location_sla(filtered_tickets, sla_threshold, downtime_threshold, days_in_month)
        slide8_data = self._generate_slide8_flowchart(filtered_tickets)
        slide9_data = self._generate_slide9_incident(filtered_tickets)
        
        return {
            "sla_records": slide6_data,
            "below_sla": below_sla,
            "major_dt": major_dt,
            "sla_by_location": sla_by_location,
            "flowchart_data": slide8_data,
            "incident_records": slide9_data
        }

    def _generate_slide6_trend(self, tickets: List[RawTicketRecord], days_in_month: int, target_months: List[str]) -> List[SLARecord]:
        """Calculates overall SLA % and Ticket count per month."""
        monthly_stats = defaultdict(lambda: {"total_tickets": 0, "eligible_tickets": 0, "total_downtime": 0.0, "total_uptime_pct_sum": 0.0})
        
        for t in tickets:
            monthly_stats[t.month]["total_tickets"] += 1
            
            if SLACalculator.is_ticket_eligible_for_downtime(t.category, t.status, t.subject_type, t.rfo):
                _, uptime_pct, _ = SLACalculator.calculate_uptime(
                    open_time=t.open_date,
                    close_time=t.close_date,
                    audit_logs=t.audit_logs,
                    total_days_in_month=days_in_month,
                    committed_uptime_pct=99.5
                )
                monthly_stats[t.month]["eligible_tickets"] += 1
                monthly_stats[t.month]["total_uptime_pct_sum"] += uptime_pct
                
        results = []
        for month, stats in monthly_stats.items():
            # If there are no eligible tickets, SLA is 100%
            if stats["eligible_tickets"] == 0:
                avg_uptime = 100.0
            else:
                avg_uptime = stats["total_uptime_pct_sum"] / stats["eligible_tickets"]
                
            results.append(SLARecord(
                month=month,
                sla_percentage=round(avg_uptime, 2),
                ticket_count=stats["total_tickets"]
            ))
            
        if not results:
            # Fallback to prevent chart crashing if no tickets exist for the target months
            results.append(SLARecord(month=target_months[-1] if target_months else "Current", sla_percentage=100.0, ticket_count=0))
            
        # Sort by month
        results.sort(key=lambda x: x.month)
        return results

    def _generate_slide7_location_sla(self, tickets: List[RawTicketRecord], sla_threshold: float, downtime_threshold: float, days_in_month: int) -> Tuple[List[Dict], List[Dict], Dict[str, float]]:
        """Identifies links below SLA, major downtimes, and computes SLA per location."""
        below_sla = []
        major_dt = []
        loc_uptime_sums = defaultdict(lambda: {"sum": 0.0, "count": 0})
        
        for t in tickets:
            if SLACalculator.is_ticket_eligible_for_downtime(t.category, t.status, t.subject_type, t.rfo):
                downtime_pct, uptime_pct, sla_status = SLACalculator.calculate_uptime(
                    open_time=t.open_date,
                    close_time=t.close_date,
                    audit_logs=t.audit_logs,
                    total_days_in_month=days_in_month,
                    committed_uptime_pct=sla_threshold
                )
                
                if uptime_pct < sla_threshold:
                    below_sla.append({
                        "Location": t.location,
                        "Link ID": t.link_id,
                        "SLA %": uptime_pct
                    })
                    
                total_aging = SLACalculator.calculate_total_aging(t.open_date, t.close_date)
                cust_aging = SLACalculator.calculate_customer_aging(t.audit_logs)
                net_downtime_hours = max(0.0, total_aging - cust_aging)
                if net_downtime_hours > downtime_threshold:
                    major_dt.append({
                        "Location": t.location,
                        "Downtime Duration": f"{net_downtime_hours:.1f} Hours",
                        "Reason": t.rfo
                    })
                    
                loc_uptime_sums[t.location]["sum"] += uptime_pct
                loc_uptime_sums[t.location]["count"] += 1
                
        sla_by_location = {}
        for loc, data in loc_uptime_sums.items():
            sla_by_location[loc] = round(data["sum"] / data["count"], 2)
                    
        return below_sla, major_dt, sla_by_location

    def _generate_slide8_flowchart(self, tickets: List[RawTicketRecord]) -> Dict[str, str]:
        """Calculates precise counts for the Slide 8 Service Requests Flowchart."""
        data = {
            "{{total_requests_count}}": str(len(tickets)),
            "{{requests_count}}": "0",
            "{{complaints_count}}": "0",
            "{{proactive_count}}": "0",
            "{{reactive_count}}": "0",
            "{{ishan_issue_count}}": "0",
            "{{customer_issue_count}}": "0",
        }
        
        requests = 0
        complaints = 0
        proactive = 0
        reactive = 0
        ishan_issue = 0
        customer_issue = 0
        
        ishan_rfos = defaultdict(int)
        customer_rfos = defaultdict(int)
        
        for t in tickets:
            if t.category.lower() == "request":
                requests += 1
            elif t.category.lower() == "complaint":
                complaints += 1
                
                if t.ticket_source.lower() == "proactive":
                    proactive += 1
                else:
                    reactive += 1
                    
                    if t.rfo in SLACalculator.INCLUDED_RFO:
                        ishan_issue += 1
                        ishan_rfos[t.rfo] += 1
                    elif t.rfo in SLACalculator.EXCLUDED_RFO:
                        customer_issue += 1
                        customer_rfos[t.rfo] += 1
                        
        data["{{requests_count}}"] = str(requests)
        data["{{complaints_count}}"] = str(complaints)
        data["{{proactive_count}}"] = str(proactive)
        data["{{reactive_count}}"] = str(reactive)
        data["{{ishan_issue_count}}"] = str(ishan_issue)
        data["{{customer_issue_count}}"] = str(customer_issue)
        
        # Get top RFOs
        sorted_ishan_rfos = sorted(ishan_rfos.items(), key=lambda item: item[1], reverse=True)
        for i in range(4):
            key = f"{{{{ishan_rfo_{i+1}}}}}"
            if i < len(sorted_ishan_rfos):
                data[key] = f"{sorted_ishan_rfos[i][0]} - {sorted_ishan_rfos[i][1]}"
            else:
                data[key] = ""
                
        sorted_cust_rfos = sorted(customer_rfos.items(), key=lambda item: item[1], reverse=True)
        for i in range(2):
            key = f"{{{{customer_rfo_{i+1}}}}}"
            if i < len(sorted_cust_rfos):
                data[key] = f"{sorted_cust_rfos[i][0]} - {sorted_cust_rfos[i][1]}"
            else:
                data[key] = ""
                
        return data

    def _generate_slide9_incident(self, tickets: List[RawTicketRecord]) -> List[IncidentRecord]:
        """Maps Complaint RFOs to Location exactly as Slide 9 requires."""
        # The Slide 9 table needs "Cable issue", "Backhaul Impacted", "Electricity issue"
        loc_stats = defaultdict(lambda: {"cable": 0, "backhaul": 0, "electricity": 0})
        
        for t in tickets:
            if t.category.lower() == "complaint":
                rfo_lower = t.rfo.lower()
                
                # Loose matching based on typical incident types
                if "cable" in rfo_lower or "fiber" in rfo_lower or "last mile" in rfo_lower:
                    loc_stats[t.location]["cable"] += 1
                elif "backhaul" in rfo_lower or "ishan network" in rfo_lower or "core device" in rfo_lower:
                    loc_stats[t.location]["backhaul"] += 1
                elif "power" in rfo_lower or "electricity" in rfo_lower:
                    loc_stats[t.location]["electricity"] += 1
                    
        records = []
        for loc, stats in loc_stats.items():
            records.append(IncidentRecord(
                location=loc,
                cable_issue=stats["cable"],
                backhaul_impacted=stats["backhaul"],
                electricity_issue=stats["electricity"]
            ))
            
        return records
