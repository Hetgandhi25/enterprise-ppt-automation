import logging
from typing import Dict, Any, Type
from backend.automation.portal_client import PortalClient
from backend.automation.crm_adapter import CRMAdapter
from backend.utils.exceptions import AutomationError

logger = logging.getLogger(__name__)

class AutomationRunner:
    """Entry point for executing an automation job."""
    
    def __init__(self, config: Dict[str, Any], adapter_class: Type[CRMAdapter]):
        self.config = config
        self.adapter_class = adapter_class
        
    def run_job(self, customer_id: str, credentials: dict) -> Dict[str, Any]:
        """Runs the entire automation job for a specific customer."""
        logger.info(f"Starting automation job for {customer_id}")
        client = PortalClient(self.config, self.adapter_class)
        
        try:
            client.start(credentials)
            downloader = client.get_downloader()
            reports = downloader.download_all(customer_id)
            logger.info(f"Automation job completed successfully for {customer_id}")
            return reports
        except Exception as e:
            logger.error(f"Automation job failed for {customer_id}: {e}")
            client.browser_manager.take_screenshot(f"error_{customer_id}")
            raise AutomationError(f"Job failed: {e}")
        finally:
            client.close()
