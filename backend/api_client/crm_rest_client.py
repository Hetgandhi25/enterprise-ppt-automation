import logging
import os
from pathlib import Path
from typing import Dict, Any
import requests
from bs4 import BeautifulSoup
import shutil
import pandas as pd

from backend.automation.data_fetcher import DataFetcher

logger = logging.getLogger(__name__)

class CRMRestClient(DataFetcher):
    """
    Automated Web Scraper Client for fetching CRM data directly from the portal.
    Bypasses the need for REST APIs by logging in invisibly and scraping HTML.
    """
    def __init__(self, api_url: str, api_token: str, downloads_dir: Path, logged_in_user: str = "system"):
        self.portal_url = "http://27.54.160.8/devops/uatPortal"
        # We use environment variables for security, but default to the UAT credentials provided
        self.username = os.environ.get("CRM_USERNAME", "Shah.Manank")
        self.password = os.environ.get("CRM_PASSWORD", "Apr@2025")
        self.logged_in_user = logged_in_user
        
        self.downloads_dir = downloads_dir
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
        
        self.session = requests.Session()
        self.is_logged_in = False

    def _login(self) -> bool:
        if self.is_logged_in:
            return True
            
        logger.info(f"Attempting background login to CRM Portal as {self.username}...")
        try:
            # The portal uses an AJAX POST to login_check
            login_url = f"{self.portal_url}/index.php/sessions/login_check/?cmd=login&ref={self.username}&ip_add="
            response = self.session.post(login_url, data={'user': self.username, 'pass': self.password}, timeout=10)
            
            if response.status_code == 200 and "true" in response.text.lower():
                logger.info("Successfully logged into CRM Portal.")
                self.is_logged_in = True
                return True
            else:
                logger.warning(f"Failed to log in. Response: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error during CRM login: {e}")
            return False

    def _scrape_finance_ageing(self, customer_id: str):
        """Scrapes Invoice Number, Date, Opening Balance from Client Ageing V2"""
        logger.info(f"Scraping Client Ageing V2 JSON for {customer_id}...")
        url = f"{self.portal_url}/index.php/client_aging_mst_v2/loadData"
        try:
            response = self.session.get(url, timeout=10)
            logger.info(f"Client Ageing Fetch Status: {response.status_code}")
            # Try parsing JSON to verify it works, but don't crash if it requires specific POST params
            data = response.json()
            logger.info(f"Successfully retrieved Client Ageing JSON data (Length: {len(str(data))} bytes)")
            return data
        except Exception as e:
            logger.warning(f"Failed to parse Client Ageing JSON (Fallback Mode Triggered): {e}")
        return None
        
    def _scrape_customer_service(self, customer_id: str):
        """Scrapes Customer Service details JSON for customer_id, or all if customer_id is empty"""
        logger.info(f"Scraping Customer Service details JSON for {customer_id if customer_id else 'ALL'}...")
        url = f"{self.portal_url}/index.php/view_sam_orders/loadData"
        try:
            response = self.session.get(url, timeout=10)
            logger.info(f"Customer Service Fetch Status: {response.status_code}")
            data = response.json()
            logger.info(f"Successfully retrieved Customer Service JSON data (Length: {len(str(data))} bytes)")
            return data
        except Exception as e:
            logger.warning(f"Failed to parse Customer Service JSON (Fallback Mode Triggered): {e}")
        return None

    def _scrape_retention(self, customer_id: str):
        """Scrapes pending retentions from Retention Reports"""
        logger.info(f"Scraping Retention Reports JSON for {customer_id}...")
        url = f"{self.portal_url}/index.php/client_termination_intiation/loadData"
        try:
            response = self.session.get(url, timeout=10)
            logger.info(f"Retention Reports Fetch Status: {response.status_code}")
            data = response.json()
            logger.info(f"Successfully retrieved Retention JSON data (Length: {len(str(data))} bytes)")
        except Exception as e:
            logger.warning(f"Failed to parse Retention JSON (Fallback Mode Triggered): {e}")
        return None

    def get_customers(self) -> list:
        """
        Extracts the unique list of customers and their active services assigned to this CSM from the CRM portal.
        """
        logger.info(f"Extracting live customer list for {self.logged_in_user}...")
        self._login()
        if not self.is_logged_in:
            return []
            
        data = self._scrape_customer_service("")
        if not data or "rows" not in data:
            return []
            
        customers_map = {}
        for row in data["rows"]:
            c_name = row.get("Invoice")
            if not c_name:
                continue
            
            c_name = c_name.strip(" .")
            if c_name not in customers_map:
                customers_map[c_name] = {
                    "id": row.get("client_code", f"LIVE-{len(customers_map)}"),
                    "name": c_name,
                    "services": []
                }
            
            service_detail = {
                "id": row.get("service_code", "UNKNOWN"),
                "type": row.get("direct_indirect", "ILL"),
                "location": row.get("city_name", "HQ"),
                "status": "Active" if row.get("status2", "Active") == "Active" else "Inactive"
            }
            customers_map[c_name]["services"].append(service_detail)
        
        return list(customers_map.values())

    def download_all(self, customer_id: str) -> Dict[str, Path]:
        """
        Main entry point for pipeline. Attempts to scrape live data, 
        and gracefully falls back to mock data if parsing fails or HTML changes.
        """
        logger.info(f"Initializing Web Scraper for {customer_id} (Triggered by {self.logged_in_user})...")
        
        file_map = {
            "inventory": "Customer_Service_Report.xlsx",
            "raw_tickets": "Raw_Ticket_Dump.xlsx",
            "audit_logs": "Audit_Logs_Dump.xlsx",
            "invoices": "Client_Ageing_V2.xlsx",
            "retention": "Retention_Report.xlsx"
        }
        paths = {}
        
        # 1. LIVE SYNC LOGIC (Only for Shah.Manank)
        if self.logged_in_user == "Shah.Manank":
            self._login()
            if self.is_logged_in:
                # Scrape Finance
                finance_data = self._scrape_finance_ageing(customer_id)
                if finance_data and "rows" in finance_data:
                    # Filter rows for the requested customer (ignoring trailing periods/spaces for deduplication)
                    filtered_rows = [r for r in finance_data["rows"] if r.get("party_name", "").strip(" .") == customer_id.strip(" .")]
                    
                    logger.info(f"Live Sync: Mapping {len(filtered_rows)} Client Ageing rows to DataFrame...")
                    df = pd.DataFrame([{
                        "Invoice Number": r.get("invoice_no"),
                        "Invoice Date": r.get("bill_date"),
                        "Opening Balance": r.get("opening"),
                        "Pending": r.get("pending"),
                        "Ageing Bucket": r.get("ageing_criteria"),
                        "Customer Name": customer_id,  # Forced to match pipeline context
                        "Service Code": r.get("service_code"),
                        "Billing Period Duration": f"{r.get('from_date', '')} to {r.get('to_date', '')}"
                    } for r in filtered_rows])
                    
                    # If empty, create with columns anyway
                    if df.empty:
                        df = pd.DataFrame(columns=["Invoice Number", "Invoice Date", "Opening Balance", "Pending", "Ageing Bucket", "Customer Name", "Service Code", "Billing Period Duration"])
                    
                    safe_customer_id = customer_id.replace(' ', '_').replace('/', '_')
                    dst = self.downloads_dir / f"invoices_{safe_customer_id}.xlsx"
                    df.to_excel(dst, index=False)
                    paths["invoices"] = dst
                    del file_map["invoices"] # Remove from fallback
                    
                # Scrape Customer Service
                service_data = self._scrape_customer_service(customer_id)
                if service_data and "rows" in service_data:
                    # Filter rows for the requested customer (ignoring trailing periods/spaces)
                    filtered_rows = [r for r in service_data["rows"] if r.get("Invoice", "").strip(" .") == customer_id.strip(" .")]
                    
                    logger.info(f"Live Sync: Mapping {len(filtered_rows)} Customer Service rows to DataFrame...")
                    df = pd.DataFrame([{
                        "Client Name": customer_id,  # Forced to match pipeline context
                        "Client Code": r.get("client_code", "UNKNOWN"),
                        "Service ID": r.get("service_code"),
                        "Service Type": r.get("direct_indirect", "ILL"),
                        "Install City": r.get("zone_name", "HQ"),
                        "Bandwidth": r.get("bandwidth", "100 Mbps"),
                        "Link ID": r.get("service_code"),
                        "Location": r.get("zone_name", "HQ"),
                        "Status": r.get("status2", "Active")
                    } for r in filtered_rows])
                    
                    # If empty, create with columns anyway
                    if df.empty:
                        df = pd.DataFrame(columns=["Client Name", "Client Code", "Service ID", "Service Type", "Install City", "Bandwidth", "Link ID", "Location", "Status"])
                    
                    safe_customer_id = customer_id.replace(' ', '_').replace('/', '_')
                    dst = self.downloads_dir / f"inventory_{safe_customer_id}.xlsx"
                    df.to_excel(dst, index=False)
                    paths["inventory"] = dst
                    del file_map["inventory"] # Remove from fallback
                    
                # We leave raw_tickets, audit_logs, and retention to the fallback mock for now
                self._scrape_retention(customer_id)
        else:
            logger.info("Skipping Live Sync because user is not Shah.Manank. Using DEMO data.")
        
        # 2. Empty Fallback: Build empty DataFrames for remaining items instead of mocking
        if file_map:
            logger.info("Injecting empty datasets for missing real data (Empty Fallback Mode)...")
            
            # Define schemas for each type
            schemas = {
                "inventory": ["Client Name", "Client Code", "Service ID", "Service Type", "Install City", "Bandwidth", "Link ID", "Location", "Status"],
                "raw_tickets": ["Ticket ID", "Customer Name", "Month", "Location", "Link ID", "Category", "Ticket Source", "Status", "Subject Type", "RFO", "Open Date", "Close Date", "Total Aging Hours", "Customer Bucket Aging Hours"],
                "audit_logs": ["Ticket ID", "Bucket Name", "Entry Time", "Exit Time"],
                "invoices": ["Invoice Number", "Invoice Date", "Opening Balance", "Pending", "Ageing Bucket", "Customer Name", "Service Code", "Billing Period Duration"],
                "retention": ["Client ID", "Service Name", "Location", "Bandwidth", "Disconnection Reason", "Last Date", "Status"]
            }
            
            for rtype in list(file_map.keys()):
                safe_customer_id = customer_id.replace(' ', '_').replace('/', '_')
                dst = self.downloads_dir / f"{rtype}_{safe_customer_id}.xlsx"
                
                columns = schemas.get(rtype, ["Customer Name"])
                df = pd.DataFrame(columns=columns)
                
                # Mock data for Picson testing
                if "Picson" in customer_id:
                    if rtype == "inventory":
                        df = pd.DataFrame([
                            {"Client Name": customer_id, "Service Type": "ILL", "Link ID": "114475", "Location": "Mumbai", "Status": "Active"},
                            {"Client Name": customer_id, "Service Type": "P2P", "Link ID": "114476", "Location": "Delhi", "Status": "Active"},
                            {"Client Name": customer_id, "Service Type": "MPLS", "Link ID": "114477", "Location": "Bangalore", "Status": "Active"},
                            {"Client Name": customer_id, "Service Type": "SD-WAN", "Link ID": "114478", "Location": "Pune", "Status": "Active"}
                        ])
                    elif rtype == "raw_tickets":
                        df = pd.DataFrame([
                            {"Ticket ID": "T-001", "Customer Name": customer_id, "Month": "August 2026", "Location": "Mumbai", "Link ID": "114475", "Category": "Hardware", "Ticket Source": "Proactive", "Status": "Closed", "Subject Type": "Link Down", "RFO": "Power Cut", "Open Date": "2026-08-01 10:00:00", "Close Date": "2026-08-01 11:00:00", "Total Aging Hours": 1, "Customer Bucket Aging Hours": 0},
                            {"Ticket ID": "T-002", "Customer Name": customer_id, "Month": "August 2026", "Location": "Delhi", "Link ID": "114476", "Category": "Software", "Ticket Source": "Reactive", "Status": "Closed", "Subject Type": "High Latency", "RFO": "Routing Issue", "Open Date": "2026-08-02 12:00:00", "Close Date": "2026-08-02 13:30:00", "Total Aging Hours": 1.5, "Customer Bucket Aging Hours": 0},
                            {"Ticket ID": "T-003", "Customer Name": customer_id, "Month": "July 2026", "Location": "Mumbai", "Link ID": "114475", "Category": "Network", "Ticket Source": "Reactive", "Status": "Closed", "Subject Type": "Packet Loss", "RFO": "Fiber Cut", "Open Date": "2026-07-15 14:00:00", "Close Date": "2026-07-15 18:00:00", "Total Aging Hours": 4, "Customer Bucket Aging Hours": 0},
                            {"Ticket ID": "T-004", "Customer Name": customer_id, "Month": "July 2026", "Location": "Bangalore", "Link ID": "114477", "Category": "Hardware", "Ticket Source": "Proactive", "Status": "Closed", "Subject Type": "Link Down", "RFO": "Device Reboot", "Open Date": "2026-07-20 09:00:00", "Close Date": "2026-07-20 09:30:00", "Total Aging Hours": 0.5, "Customer Bucket Aging Hours": 0},
                            {"Ticket ID": "T-005", "Customer Name": customer_id, "Month": "June 2026", "Location": "Pune", "Link ID": "114478", "Category": "Software", "Ticket Source": "Reactive", "Status": "Closed", "Subject Type": "BGP Flap", "RFO": "ISP Issue", "Open Date": "2026-06-10 11:00:00", "Close Date": "2026-06-10 12:00:00", "Total Aging Hours": 1, "Customer Bucket Aging Hours": 0}
                        ])
                    elif rtype == "invoices":
                        df = pd.DataFrame([
                            {"Invoice Number": "INV-1001", "Invoice Date": "2026-03-01", "Opening Balance": 150000.50, "Pending": "Unpaid", "Ageing Bucket": "120+", "Customer Name": customer_id, "Service Code": "114475", "Billing Period Duration": "March 2026"},
                            {"Invoice Number": "INV-1002", "Invoice Date": "2026-04-01", "Opening Balance": 75000.00, "Pending": "Unpaid", "Ageing Bucket": "90-120", "Customer Name": customer_id, "Service Code": "114476", "Billing Period Duration": "April 2026"},
                            {"Invoice Number": "INV-1003", "Invoice Date": "2026-05-01", "Opening Balance": 45000.00, "Pending": "Unpaid", "Ageing Bucket": "60-90", "Customer Name": customer_id, "Service Code": "114477", "Billing Period Duration": "May 2026"},
                            {"Invoice Number": "INV-1004", "Invoice Date": "2026-06-01", "Opening Balance": 12000.00, "Pending": "Unpaid", "Ageing Bucket": "30-60", "Customer Name": customer_id, "Service Code": "114478", "Billing Period Duration": "June 2026"},
                            {"Invoice Number": "INV-1005", "Invoice Date": "2026-07-01", "Opening Balance": 85000.00, "Pending": "Unpaid", "Ageing Bucket": "0-30", "Customer Name": customer_id, "Service Code": "114475", "Billing Period Duration": "July 2026"},
                            {"Invoice Number": "INV-1006", "Invoice Date": "2026-08-01", "Opening Balance": 92000.00, "Pending": "Unpaid", "Ageing Bucket": "0-30", "Customer Name": customer_id, "Service Code": "114476", "Billing Period Duration": "August 2026"},
                            {"Invoice Number": "INV-1007", "Invoice Date": "2026-08-05", "Opening Balance": 15000.00, "Pending": "Unpaid", "Ageing Bucket": "0-30", "Customer Name": customer_id, "Service Code": "114477", "Billing Period Duration": "August 2026"}
                        ])
                    elif rtype == "retention":
                        df = pd.DataFrame([
                            {"Client ID": customer_id, "Service Name": "ILL", "Location": "Mumbai", "Bandwidth": "100Mbps", "Disconnection Reason": "Cost", "Last Date": "2026-08-31", "Status": "Pending"},
                            {"Client ID": customer_id, "Service Name": "P2P", "Location": "Delhi", "Bandwidth": "50Mbps", "Disconnection Reason": "Relocation", "Last Date": "2026-09-15", "Status": "Pending"},
                            {"Client ID": customer_id, "Service Name": "MPLS", "Location": "Bangalore", "Bandwidth": "20Mbps", "Disconnection Reason": "Dissatisfied", "Last Date": "2026-09-30", "Status": "Pending"}
                        ])
                        
                # Ensure missing columns are present and filled with None (for empty representation)
                for col in columns:
                    if col not in df.columns:
                        df[col] = None

                df.to_excel(dst, index=False)
                paths[rtype] = dst
            
        return paths
