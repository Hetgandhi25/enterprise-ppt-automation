import uuid
import logging
from typing import Dict, Any, Optional

from backend.services.execution_context import ExecutionContext
from backend.services.progress_tracker import ProgressTracker
from backend.services.metrics import MetricsCollector
from backend.services.pipeline import PPTAutomationPipeline

logger = logging.getLogger(__name__)

class JobManager:
    """Manages the creation and execution tracking of automation jobs."""
    
    def __init__(self, pipeline: PPTAutomationPipeline):
        self.pipeline = pipeline
        self.jobs: Dict[str, ExecutionContext] = {}
        self.trackers: Dict[str, ProgressTracker] = {}
        self.metrics: Dict[str, MetricsCollector] = {}
        
    def create_job(self, customer_id: str, report_month: str) -> str:
        job_id = str(uuid.uuid4())[:8]
        ctx = ExecutionContext(customer_id=customer_id, report_month=report_month, job_id=job_id)
        tracker = ProgressTracker(job_id=job_id)
        metrics = MetricsCollector(job_id=job_id)
        
        self.jobs[job_id] = ctx
        self.trackers[job_id] = tracker
        self.metrics[job_id] = metrics
        
        logger.info(f"Created job {job_id} for {customer_id}")
        return job_id
        
    def run_job(self, job_id: str) -> None:
        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} not found.")
            
        ctx = self.jobs[job_id]
        tracker = self.trackers[job_id]
        metrics = self.metrics[job_id]
        
        logger.info(f"Running job {job_id}")
        self.pipeline.execute(ctx, tracker, metrics)
        
    def get_status(self, job_id: str) -> Optional[ProgressTracker]:
        return self.trackers.get(job_id)
        
    def cancel_job(self, job_id: str) -> None:
        # Currently, cancellation would require threading/async support.
        # This is a stub for future async worker implementation.
        logger.warning(f"Cancellation for {job_id} requested but synchronous runner cannot interrupt.")
