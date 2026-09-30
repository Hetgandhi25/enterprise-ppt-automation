import time
import os
import psutil
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class JobMetrics:
    """Stores performance metrics for a job execution."""
    job_id: str
    download_time_ms: float = 0.0
    excel_processing_time_ms: float = 0.0
    chart_generation_time_ms: float = 0.0
    ppt_generation_time_ms: float = 0.0
    total_runtime_ms: float = 0.0
    peak_memory_mb: float = 0.0
    
class MetricsCollector:
    """Utility to collect and aggregate metrics during execution."""
    
    def __init__(self, job_id: str):
        self.metrics = JobMetrics(job_id=job_id)
        self._start_times: Dict[str, float] = {}
        self.process = psutil.Process(os.getpid())
        
    def start_timer(self, name: str):
        self._start_times[name] = time.time()
        self._record_memory()
        
    def stop_timer(self, name: str, metric_field: str):
        if name in self._start_times:
            elapsed_ms = (time.time() - self._start_times[name]) * 1000.0
            setattr(self.metrics, metric_field, elapsed_ms)
            self._record_memory()
            
    def _record_memory(self):
        mem_mb = self.process.memory_info().rss / (1024 * 1024)
        if mem_mb > self.metrics.peak_memory_mb:
            self.metrics.peak_memory_mb = mem_mb
