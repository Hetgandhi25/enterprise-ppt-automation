import logging
from playwright.sync_api import Page
from backend.utils.exceptions import AutomationError

logger = logging.getLogger(__name__)

class WaitUtils:
    """Reusable wait strategies without time.sleep()."""
    
    @staticmethod
    def wait_visible(page: Page, selector: str, timeout: int = 30000) -> None:
        logger.debug(f"Waiting for '{selector}' to be visible (timeout={timeout}ms)")
        try:
            page.wait_for_selector(selector, state="visible", timeout=timeout)
        except Exception as e:
            raise AutomationError(f"Timeout waiting for {selector} to be visible: {e}")
            
    @staticmethod
    def wait_hidden(page: Page, selector: str, timeout: int = 30000) -> None:
        logger.debug(f"Waiting for '{selector}' to be hidden (timeout={timeout}ms)")
        try:
            page.wait_for_selector(selector, state="hidden", timeout=timeout)
        except Exception as e:
            raise AutomationError(f"Timeout waiting for {selector} to be hidden: {e}")
            
    @staticmethod
    def wait_network_idle(page: Page, timeout: int = 30000) -> None:
        logger.debug("Waiting for network idle.")
        try:
            page.wait_for_load_state("networkidle", timeout=timeout)
        except Exception as e:
            raise AutomationError(f"Timeout waiting for network idle: {e}")
