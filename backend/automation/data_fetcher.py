import logging
from abc import ABC, abstractmethod
from typing import Dict
from pathlib import Path

class DataFetcher(ABC):
    """
    Abstract interface for fetching CRM data payloads.
    Provides a standardized way to pull Inventory, SLA, Incidents, etc.
    """
    
    @abstractmethod
    def download_all(self, customer_id: str) -> Dict[str, Path]:
        """
        Fetches all necessary data for a given customer.
        Returns a dictionary mapping dataset names to local temporary file paths.
        
        Example Return:
        {
            "inventory": Path("downloads/inventory.xlsx"),
            "raw_tickets": Path("downloads/raw_tickets.xlsx"),
            "invoices": Path("downloads/invoices.xlsx"),
            "retention": Path("downloads/retention.xlsx")
        }
        """
        pass
