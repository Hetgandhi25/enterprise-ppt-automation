from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from backend.models.domain import Customer


class GenerationStatus(str, Enum):
    """Enum representing the status of a generation task."""
    QUEUED = "QUEUED"
    DOWNLOADING = "DOWNLOADING"
    PROCESSING = "PROCESSING"
    GENERATING_CHARTS = "GENERATING_CHARTS"
    UPDATING_PPT = "UPDATING_PPT"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class GenerateRequest(BaseModel):
    """Request model for triggering PPT generation."""
    customer_id: str
    month: str = Field(..., pattern=r"^\d{4}-\d{2}$")
    force_refresh: bool = False


class GenerateResponse(BaseModel):
    """Response model for a successful generate request."""
    task_id: UUID
    status: GenerationStatus
    message: str


class TaskStatusResponse(BaseModel):
    """Response model for checking task status."""
    task_id: UUID
    status: GenerationStatus
    progress_percent: int = Field(ge=0, le=100)
    current_step: str
    download_url: Optional[str] = None
    error_message: Optional[str] = None


class CustomersListResponse(BaseModel):
    """Response model for listing available customers."""
    customers: List[Customer]


class ErrorResponse(BaseModel):
    """Standardized error response model."""
    error_code: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
