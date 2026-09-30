from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

@dataclass
class ExecutionContext:
    """Stores all context required and generated during pipeline execution."""
    
    # Inputs
    customer_id: str
    report_month: str
    job_id: str
    
    # State
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    
    # Intermediate Paths
    download_paths: Dict[str, Path] = field(default_factory=dict)
    chart_paths: Dict[str, Path] = field(default_factory=dict)
    
    # Processed Data
    data: Dict[str, Any] = field(default_factory=dict)
    summary: Dict[str, Any] = field(default_factory=dict)
    
    # Output
    final_ppt_path: Optional[Path] = None
    
    def mark_completed(self):
        self.end_time = datetime.now()
        
    @property
    def elapsed_time_seconds(self) -> float:
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds()
