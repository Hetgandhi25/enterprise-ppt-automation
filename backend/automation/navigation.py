import logging
from playwright.sync_api import Page
from backend.automation.wait_utils import WaitUtils
from backend.utils.exceptions import AutomationError

logger = logging.getLogger(__name__)

class Navigation:
    """Reusable helpers for DOM navigation and interaction."""
    
    @staticmethod
    def click(page: Page, selector: str, timeout: int = 30000) -> None:
        logger.debug(f"Clicking '{selector}'")
        try:
            page.click(selector, timeout=timeout)
        except Exception as e:
            raise AutomationError(f"Failed to click {selector}: {e}")
            
    @staticmethod
    def safe_click(page: Page, selector: str, timeout: int = 30000) -> None:
        """Waits for element to be visible before clicking."""
        WaitUtils.wait_visible(page, selector, timeout)
        Navigation.click(page, selector, timeout)
        
    @staticmethod
    def fill(page: Page, selector: str, value: str, timeout: int = 30000) -> None:
        logger.debug(f"Filling '{selector}' with secure data.")
        try:
            page.fill(selector, value, timeout=timeout)
        except Exception as e:
            raise AutomationError(f"Failed to fill {selector}: {e}")
            
    @staticmethod
    def safe_fill(page: Page, selector: str, value: str, timeout: int = 30000) -> None:
        WaitUtils.wait_visible(page, selector, timeout)
        Navigation.fill(page, selector, value, timeout)
