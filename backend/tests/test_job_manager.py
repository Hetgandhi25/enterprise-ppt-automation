import pytest
from unittest.mock import MagicMock
from backend.services.job_manager import JobManager
from backend.services.pipeline import PPTAutomationPipeline

def test_job_manager():
    pipeline_mock = MagicMock(spec=PPTAutomationPipeline)
    manager = JobManager(pipeline_mock)
    
    job_id = manager.create_job("ASG India", "2026-07")
    assert job_id in manager.jobs
    assert job_id in manager.trackers
    assert job_id in manager.metrics
    
    manager.run_job(job_id)
    pipeline_mock.execute.assert_called_once()
    
    status = manager.get_status(job_id)
    assert status is not None
    assert status.job_id == job_id

def test_job_manager_invalid_job():
    pipeline_mock = MagicMock(spec=PPTAutomationPipeline)
    manager = JobManager(pipeline_mock)
    
    with pytest.raises(ValueError):
        manager.run_job("non-existent-id")
