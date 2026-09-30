import time
import logging
from typing import List, Dict, Any, Optional
from backend.services.task_status import PipelineStage, TaskStatus
from backend.services.execution_context import ExecutionContext

logger = logging.getLogger(__name__)

class ProgressTracker:
    """Tracks the progress of an active pipeline job."""
    
    def __init__(self, job_id: str, total_stages: int = 8):
        self.job_id = job_id
        self.status = TaskStatus.PENDING
        self.current_stage = PipelineStage.INITIALIZING
        self.total_stages = total_stages
        self.completed_stages = 0
        self.warnings: List[str] = []
        self.errors: List[str] = []
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        
    def start(self):
        self.status = TaskStatus.RUNNING
        self.start_time = time.time()
        
    def update_stage(self, stage: PipelineStage):
        self.current_stage = stage
        self.completed_stages += 1
        logger.info(f"[Job {self.job_id}] Progress: {self.percent_complete}% - {stage.value}")
        
    def add_warning(self, message: str):
        self.warnings.append(message)
        logger.warning(f"[Job {self.job_id}] Warning: {message}")
        
    def fail(self, error: str):
        self.status = TaskStatus.FAILED
        self.current_stage = PipelineStage.FAILED
        self.errors.append(error)
        self.end_time = time.time()
        logger.error(f"[Job {self.job_id}] Failed: {error}")
        
    def complete(self):
        self.status = TaskStatus.COMPLETED
        self.current_stage = PipelineStage.COMPLETED
        self.completed_stages = self.total_stages
        self.end_time = time.time()
        logger.info(f"[Job {self.job_id}] Completed in {self.elapsed_time:.2f}s")
        
    @property
    def percent_complete(self) -> float:
        if self.status == TaskStatus.COMPLETED:
            return 100.0
        return round((self.completed_stages / self.total_stages) * 100.0, 1)
        
    @property
    def elapsed_time(self) -> float:
        if not self.start_time:
            return 0.0
        end = self.end_time or time.time()
        return end - self.start_time
