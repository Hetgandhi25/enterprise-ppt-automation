import logging
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd

from backend.models.domain import SLARecord
from backend.processors.base_processor import BaseProcessor
from backend.processors.excel_reader import read_excel_file, clean_dataframe
from backend.processors.validators import validate_customer_exists, validate_numeric_columns, validate_required_columns

logger = logging.getLogger(__name__)


class SLAProcessor(BaseProcessor):
    """Processes SLA Report and Location SLA Report."""
    
    def __init__(self, sla_file_path: Path, location_sla_file_path: Path):
        # We initialize with the SLA report for the base class
        super().__init__(sla_file_path)
        self.location_sla_file_path = location_sla_file_path
        self.required_columns = ["Customer Name", "Month", "SLA %", "Tickets Raised"]
        self.location_required_columns = ["Customer Name", "Location", "Link ID", "SLA %", "Downtime Duration", "Reason"]
        
    def process(self, customer_names: List[str], target_months: List[str], sla_threshold: float = 99.5, downtime_threshold: float = 4.0) -> Tuple[List[SLARecord], List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Processes SLA trends, links below SLA, and major downtimes.
        
        Args:
            customer_names: List of acceptable customer names.
            target_months: List of months to include (e.g., ['2026-05', '2026-06', '2026-07']).
            sla_threshold: SLA percentage threshold (default 99.5).
            downtime_threshold: Downtime threshold in hours (default 4.0).
            
        Returns:
            Tuple containing:
            - List of SLARecord models.
            - List of Links below SLA (dicts).
            - List of Major Downtime details (dicts).
        """
        logger.info(f"[{self.__class__.__name__}] Processing SLA for customer: {customer_names[0]}")
        
        # --- Part 1: Overall SLA Trend ---
        self.load_and_validate()
        validate_numeric_columns(self.df, ["SLA %", "Tickets Raised"], self.file_path.name)
        
        # Filter customer
        sla_df = validate_customer_exists(self.df, "Customer Name", customer_names)
        
        # Filter months
        sla_df = sla_df[sla_df["Month"].isin(target_months)]
        
        # Calculate averages/sums per month
        monthly_grouped = sla_df.groupby("Month").agg({"SLA %": "mean", "Tickets Raised": "sum"}).reset_index()
        monthly_grouped = monthly_grouped.sort_values(by="Month")
        
        sla_records = []
        for _, row in monthly_grouped.iterrows():
            sla_records.append(SLARecord(
                month=str(row["Month"]),
                sla_percentage=float(row["SLA %"]),
                ticket_count=int(row["Tickets Raised"])
            ))
            
        # --- Part 2: Location Wise SLA ---
        logger.info(f"[{self.__class__.__name__}] Loading Location SLA report from {self.location_sla_file_path.name}")
        loc_df_raw = read_excel_file(self.location_sla_file_path)
        loc_df = clean_dataframe(loc_df_raw)
        validate_required_columns(loc_df, self.location_required_columns, self.location_sla_file_path.name)
        validate_numeric_columns(loc_df, ["SLA %", "Downtime Duration"], self.location_sla_file_path.name)
        
        loc_df = validate_customer_exists(loc_df, "Customer Name", customer_names)
        
        # Filter links below SLA
        below_sla_df = loc_df[loc_df["SLA %"] < sla_threshold]
        links_below_sla = below_sla_df[["Location", "Link ID", "SLA %"]].to_dict('records')
        
        # Filter major downtime
        major_dt_df = loc_df[loc_df["Downtime Duration"] > downtime_threshold]
        major_downtimes = major_dt_df[["Location", "Downtime Duration", "Reason"]].to_dict('records')
        
        logger.info(f"[{self.__class__.__name__}] Found {len(links_below_sla)} links below SLA and {len(major_downtimes)} major downtimes.")
        
        return sla_records, links_below_sla, major_downtimes
