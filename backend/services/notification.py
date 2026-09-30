from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class NotificationInterface(ABC):
    """Abstract interface for all notification types."""
    
    @abstractmethod
    def send_success(self, job_id: str, ppt_path: str):
        pass
        
    @abstractmethod
    def send_failure(self, job_id: str, error: str):
        pass

class ConsoleNotifier(NotificationInterface):
    """Console-based notification for local runs."""
    
    def send_success(self, job_id: str, ppt_path: str):
        logger.info(f"NOTIFICATION: Job {job_id} succeeded. Output: {ppt_path}")
        print(f"\n[SUCCESS] [JOB {job_id}] Successfully generated {ppt_path}\n")
        
    def send_failure(self, job_id: str, error: str):
        logger.error(f"NOTIFICATION: Job {job_id} failed. Error: {error}")
        print(f"\n[FAILED] [JOB {job_id}] Failed: {error}\n")

class EmailNotifier(NotificationInterface):
    """Future email integration."""
    def send_success(self, job_id: str, ppt_path: str):
        pass
    def send_failure(self, job_id: str, error: str):
        pass

class TeamsNotifier(NotificationInterface):
    """Future Teams integration."""
    def send_success(self, job_id: str, ppt_path: str):
        pass
    def send_failure(self, job_id: str, error: str):
        pass

class SlackNotifier(NotificationInterface):
    """Future Slack integration."""
    def send_success(self, job_id: str, ppt_path: str):
        pass
    def send_failure(self, job_id: str, error: str):
        pass
