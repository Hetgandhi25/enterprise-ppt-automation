import pytest
from backend.services.progress_tracker import ProgressTracker
from backend.services.task_status import PipelineStage, TaskStatus

def test_progress_tracker():
    tracker = ProgressTracker("test_job", total_stages=2)
    assert tracker.status == TaskStatus.PENDING
    assert tracker.percent_complete == 0.0
    
    tracker.start()
    assert tracker.status == TaskStatus.RUNNING
    
    tracker.update_stage(PipelineStage.DOWNLOADING)
    assert tracker.completed_stages == 1
    assert tracker.percent_complete == 50.0
    
    tracker.add_warning("Test warning")
    assert "Test warning" in tracker.warnings
    
    tracker.complete()
    assert tracker.status == TaskStatus.COMPLETED
    assert tracker.percent_complete == 100.0

def test_progress_tracker_fail():
    tracker = ProgressTracker("test_job", total_stages=2)
    tracker.start()
    tracker.fail("Failed download")
    
    assert tracker.status == TaskStatus.FAILED
    assert "Failed download" in tracker.errors
