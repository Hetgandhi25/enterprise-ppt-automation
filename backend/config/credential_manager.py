import os
from typing import Optional
from backend.utils.exceptions import ConfigurationError
from dotenv import load_dotenv

class CredentialManager:
    """Manages CRM credentials and validates required values."""
    
    def __init__(self):
        # Ensure .env is loaded
        load_dotenv()
        
        self.crm_url: Optional[str] = os.getenv("CRM_URL")
        self.crm_username: Optional[str] = os.getenv("CRM_USERNAME")
        self.crm_password: Optional[str] = os.getenv("CRM_PASSWORD")
        self.download_path: str = os.getenv("DOWNLOAD_PATH", "output/downloads")
        self.output_path: str = os.getenv("OUTPUT_PATH", "output/presentations")
        
        # Automation Settings
        self.headless: bool = os.getenv("HEADLESS", "true").lower() in ("true", "1", "yes")
        self.timeout: int = int(os.getenv("TIMEOUT", "30000"))
        self.retry_count: int = int(os.getenv("RETRY_COUNT", "3"))
        
    def validate_for_production(self):
        """Validates that all required production credentials are present."""
        missing = []
        if not self.crm_url:
            missing.append("CRM_URL")
        if not self.crm_username:
            missing.append("CRM_USERNAME")
        if not self.crm_password:
            missing.append("CRM_PASSWORD")
            
        if missing:
            raise ConfigurationError(
                f"Missing required production credentials in environment variables: {', '.join(missing)}"
            )
            
    def get_credentials(self) -> dict:
        """Returns credentials as a dictionary."""
        return {
            "username": self.crm_username,
            "password": self.crm_password
        }
