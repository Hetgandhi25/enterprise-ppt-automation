import pytest
from backend.processors.sla_calculator import SLACalculator

def test_eligibility_filter():
    # Illustration 6 (Excluded due to Planned Maintenance RFO)
    assert SLACalculator.is_ticket_eligible_for_downtime(
        category="Complaint",
        status="Close",
        subject_type="Link Down - MPLS/P2P",
        rfo="Service Impacted Due to Planned Maintenance"
    ) == False

    # Illustration 5 (Included)
    assert SLACalculator.is_ticket_eligible_for_downtime(
        category="Complaint",
        status="Close",
        subject_type="Link Down - MPLS/P2P",
        rfo="Core Device Configuration Issue"
    ) == True
    
    # Excluded because Request
    assert SLACalculator.is_ticket_eligible_for_downtime(
        category="Request",
        status="Close",
        subject_type="Link Down - MPLS/P2P",
        rfo="Last Mile Issue"
    ) == False

from backend.models.domain import TicketAuditLog

def test_uptime_calculation():
    # Illustration 4 calculation logic: Total aging = 80h, Cust bucket = 51h. Downtime = 29h
    # 80 hours = 2026-06-01 10:00:00 to 2026-06-04 18:00:00
    # Cust bucket = 51 hours = 2026-06-02 10:00:00 to 2026-06-04 13:00:00
    
    mock_log = TicketAuditLog(
        bucket_name="Access Issue at Customer End",
        entry_time="2026-06-02 10:00:00",
        exit_time="2026-06-04 13:00:00"
    )
    
    downtime_pct, uptime_pct, status = SLACalculator.calculate_uptime(
        open_time="2026-06-01 10:00:00",
        close_time="2026-06-04 18:00:00",
        audit_logs=[mock_log],
        total_days_in_month=31,
        committed_uptime_pct=99.5
    )
    
    # Downtime = 29/24/31 = 3.90%
    assert downtime_pct == 3.90
    assert uptime_pct == 96.10
    assert status == "BSLA"
