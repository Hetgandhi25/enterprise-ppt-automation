import logging
from typing import Dict, Any, Tuple, List
from datetime import datetime

logger = logging.getLogger(__name__)

class SLACalculator:
    """
    Production-grade SLA Calculation Engine.
    Implements the exact business rules from "Enterprise Links' Downtime Calculation" guidelines.
    """

    # --- Business Rules Constants ---
    VALID_CATEGORIES = ["Complaint"]
    VALID_STATUSES = ["Close", "Closed (Auto)", "Closed with OTP"]

    INCLUDED_SUBJECT_TYPES = [
        "Link Down - MPLS/P2P",
        "Internet Not Working - ILL",
        "Link Flapping"
    ]

    INCLUDED_RFO = [
        "Last Mile Issue",
        "Backhaul Network Issue",
        "TP Issue",
        "Ishan Network Issue",
        "Core Device Configuration Issue" # Added based on Illustration 5
    ]

    EXCLUDED_RFO = [
        "Customer End Issue",
        "Other Issue (Link Was Up)",
        "Planned Maintenance Activity",
        "Service Impacted Due to Planned Maintenance" # Added based on Illustration 6
    ]

    CUSTOMER_BUCKETS = [
        "Waiting for Customer",
        "Access Issue at Customer End",
        "Resolved",
        "Observation",
        "Field Resolved",
        "NOC Resolved",
        "Awaiting for Customer Confirmation",
        "Resolved by Cloud Team",
        "Resolved by Voice Team"
    ]

    @classmethod
    def is_ticket_eligible_for_downtime(cls, category: str, status: str, subject_type: str, rfo: str) -> bool:
        """
        Validates if a raw CRM ticket qualifies for DOWNTIME calculation.
        """
        if category not in cls.VALID_CATEGORIES:
            return False
            
        # The PDF states complaints in any other status than Close are excluded.
        # Handling variations of "Close" like "Closed (Auto)" based on illustrations.
        if not any(s.lower() in status.lower() for s in cls.VALID_STATUSES):
            return False
            
        if subject_type not in cls.INCLUDED_SUBJECT_TYPES:
            return False
            
        # RFO Exclusion supersedes inclusion
        if rfo in cls.EXCLUDED_RFO:
            return False
            
        if rfo not in cls.INCLUDED_RFO:
            logger.warning(f"Ticket RFO '{rfo}' is not explicitly included or excluded. Defaulting to excluded.")
            return False
            
        return True

    @classmethod
    def calculate_total_aging(cls, open_time: str, close_time: str) -> float:
        """Calculates total gross downtime in hours between two timestamps."""
        try:
            fmt = "%Y-%m-%d %H:%M:%S"
            t1 = datetime.strptime(open_time, fmt)
            t2 = datetime.strptime(close_time, fmt)
            diff = (t2 - t1).total_seconds() / 3600.0
            return max(0.0, diff)
        except Exception as e:
            logger.error(f"Error parsing dates for total aging ({open_time} -> {close_time}): {e}")
            return 0.0

    @classmethod
    def calculate_customer_aging(cls, audit_logs: List[Any]) -> float:
        """
        Iterates over ticket audit logs. If the bucket is a known Customer Bucket,
        calculates the hours spent in it and sums it up.
        """
        total_hours = 0.0
        fmt = "%Y-%m-%d %H:%M:%S"
        
        for log in audit_logs:
            # We assume log is an object with bucket_name, entry_time, exit_time
            if log.bucket_name in cls.CUSTOMER_BUCKETS:
                try:
                    t1 = datetime.strptime(log.entry_time, fmt)
                    t2 = datetime.strptime(log.exit_time, fmt)
                    diff = (t2 - t1).total_seconds() / 3600.0
                    total_hours += max(0.0, diff)
                except Exception as e:
                    logger.warning(f"Error parsing dates in audit log {log}: {e}")
        return total_hours

    @classmethod
    def calculate_uptime(
        cls, 
        open_time: str,
        close_time: str,
        audit_logs: List[Any],
        total_days_in_month: int, 
        committed_uptime_pct: float
    ) -> Tuple[float, float, str]:
        """
        Calculates Uptime %, Downtime %, and SLA Adherence by dynamically 
        parsing raw ticket dates and history.
        """
        total_aging_hours = cls.calculate_total_aging(open_time, close_time)
        customer_bucket_aging_hours = cls.calculate_customer_aging(audit_logs)
        
        # Formula: DOWNTIME = Total Aging - All Customer Bucket Aging
        net_downtime_hours = max(0.0, total_aging_hours - customer_bucket_aging_hours)
        
        # Formula: Downtime = DOWNTIME/24/Total Days of the Month
        downtime_pct = (net_downtime_hours / 24.0 / total_days_in_month) * 100.0
        downtime_pct = round(downtime_pct, 2)
        
        # Formula: Uptime = 100% - Downtime (%)
        uptime_pct = round(100.0 - downtime_pct, 2)
        
        # SLA Type Evaluation
        if uptime_pct >= committed_uptime_pct:
            sla_status = "WSLA" # Within SLA
        else:
            sla_status = "BSLA" # Beyond SLA
            
        return downtime_pct, uptime_pct, sla_status

