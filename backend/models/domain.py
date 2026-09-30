from typing import List, Optional

from pydantic import BaseModel, Field


class Customer(BaseModel):
    """Represents a customer entity."""
    customer_id: str
    customer_name: str
    alias_list: List[str] = Field(default_factory=list)


class TicketAuditLog(BaseModel):
    """Represents a state transition log for a ticket."""
    bucket_name: str
    entry_time: str
    exit_time: str


class RawTicketRecord(BaseModel):
    """Represents a raw CRM ticket used for SLA calculations."""
    ticket_id: str
    customer_name: str
    month: str
    location: str
    link_id: str
    category: str
    ticket_source: str = "Reactive"
    status: str
    subject_type: str
    rfo: str
    open_date: str
    close_date: str
    audit_logs: List[TicketAuditLog] = Field(default_factory=list)


class InventoryRecord(BaseModel):
    """Represents an inventory record for a customer."""
    customer_name: str
    service_type: str
    link_count: int = Field(ge=0)


class SLARecord(BaseModel):
    """Represents SLA performance for a specific month."""
    month: str
    sla_percentage: float = Field(ge=0.0, le=100.0)
    ticket_count: int = Field(ge=0)


class IncidentRecord(BaseModel):
    """Represents an incident summary for a location."""
    location: str
    cable_issue: int = Field(default=0, ge=0)
    backhaul_impacted: int = Field(default=0, ge=0)
    electricity_issue: int = Field(default=0, ge=0)


class ChartData(BaseModel):
    """Represents data required to generate a chart."""
    labels: List[str]
    values: List[float]
    target_line: Optional[float] = None


class InvoiceRecord(BaseModel):
    """Represents an invoice ageing record for a customer."""
    invoice_number: str
    invoice_date: str
    billing_period: str
    opening_balance: float
    ageing_bucket: str
    service_code: str = ""


class RetentionRecord(BaseModel):
    """Represents a pending retention request for a customer."""
    service_name: str
    client_id: str
    location: str
    bandwidth: str
    disconnection_reason: str
    last_date: str
