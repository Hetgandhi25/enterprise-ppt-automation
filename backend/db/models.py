from datetime import datetime
import uuid

from sqlalchemy import Column, String, Float, Integer, ForeignKey, Text, DateTime, Date, Numeric, Enum
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    aliases = relationship("CustomerAlias", back_populates="customer", cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="customer")
    reports = relationship("Report", back_populates="customer")
    inventory_records = relationship("DBInventoryRecord", back_populates="customer")
    sla_metrics = relationship("DBSLAMetric", back_populates="customer")
    incidents = relationship("DBIncident", back_populates="customer")
    invoices = relationship("DBInvoice", back_populates="customer")
    retention_requests = relationship("DBRetentionRequest", back_populates="customer")


class CustomerAlias(Base):
    __tablename__ = "customer_aliases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    alias = Column(String, nullable=False)

    customer = relationship("Customer", back_populates="aliases")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    target_month = Column(String, nullable=False) # e.g., '2026-07'
    status = Column(String, nullable=False) # PENDING, RUNNING, COMPLETED, FAILED
    progress_percentage = Column(Float, default=0.0)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)

    customer = relationship("Customer", back_populates="jobs")
    reports = relationship("Report", back_populates="job")


class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    target_month = Column(String, nullable=False)
    ppt_path = Column(String, nullable=False)
    file_size_kb = Column(Float, nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="reports")
    customer = relationship("Customer", back_populates="reports")


class DBInventoryRecord(Base):
    __tablename__ = "inventory_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    service_type = Column(String, nullable=False)
    service_code = Column(String, nullable=False)
    location = Column(String, nullable=False)
    status = Column(String, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="inventory_records")


class DBSLAMetric(Base):
    __tablename__ = "sla_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    service_code = Column(String, nullable=True)
    location = Column(String, nullable=False)
    month = Column(String, nullable=False)
    sla_percentage = Column(Float, nullable=False)
    downtime_duration = Column(Float, nullable=False)
    downtime_reason = Column(String, nullable=True)
    tickets_raised = Column(Integer, nullable=False, default=0)

    customer = relationship("Customer", back_populates="sla_metrics")


class DBIncident(Base):
    __tablename__ = "incidents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    location = Column(String, nullable=False)
    issue_category = Column(String, nullable=False)
    month = Column(String, nullable=False)

    customer = relationship("Customer", back_populates="incidents")


class DBInvoice(Base):
    __tablename__ = "invoices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    invoice_number = Column(String, unique=True, nullable=False)
    invoice_date = Column(Date, nullable=False)
    billing_period = Column(String, nullable=False)
    opening_balance = Column(Numeric, nullable=False)
    net_amount = Column(Numeric, nullable=True)
    ageing_bucket = Column(String, nullable=False)
    status = Column(String, nullable=True)

    customer = relationship("Customer", back_populates="invoices")


class DBRetentionRequest(Base):
    __tablename__ = "retention_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    service_code = Column(String, nullable=True)
    location = Column(String, nullable=False)
    bandwidth = Column(String, nullable=True)
    disconnection_reason = Column(Text, nullable=True)
    last_date = Column(Date, nullable=True)
    status = Column(String, nullable=False)

    customer = relationship("Customer", back_populates="retention_requests")
