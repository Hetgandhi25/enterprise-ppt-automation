import argparse
import sys
import os
import logging
from pathlib import Path
import traceback

# Import configs
from backend.config.mode import AppMode
from backend.config.app_config import AppConfig

from backend.api_client.crm_rest_client import CRMRestClient
from backend.services.pipeline import PPTAutomationPipeline
from backend.services.job_manager import JobManager
from backend.services.notification import ConsoleNotifier
from backend.utils.logger import setup_logging

def main():
    parser = argparse.ArgumentParser(description="CustPPTAutomation - Enterprise Service Review PPT Generator")
    parser.add_argument("--demo", action="store_true", help="Run the application in DEMO mode with mock portal.")
    parser.add_argument("--production", action="store_true", help="Run the application in PRODUCTION mode with real CRM.")
    parser.add_argument("--customer", type=str, required=True, help="Customer Name to generate PPT for.")
    parser.add_argument("--month", type=str, required=True, help="Report Month (e.g., 'July 2026' or '2026-07').")
    parser.add_argument("--user", type=str, default="system", help="Logged in username")
    parser.add_argument("--output", type=str, help="Override output directory.")
    
    args = parser.parse_args()
    
    if args.production:
        mode = AppMode.PRODUCTION
    elif args.demo:
        mode = AppMode.DEMO
    else:
        print("Error: You must specify either --demo or --production.")
        sys.exit(1)
        
    # 1. Configuration & Validation
    setup_logging()
    logger = logging.getLogger("main")
    
    try:
        app_config = AppConfig(mode)
        app_config.validate_startup()
    except Exception as e:
        logger.error(f"Startup validation failed: {e}")
        sys.exit(1)
        
    output_dir = Path(args.output) if args.output else app_config.dirs["outputs"]
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 2. Dependency Injection
    # For now, we use a placeholder API URL and Token.
    api_url = os.getenv("CRM_API_URL", "https://api.crm.internal/v1")
    api_token = os.getenv("CRM_API_TOKEN", "REPLACE_ME_WHEN_READY")
    
    data_fetcher = CRMRestClient(api_url=api_url, api_token=api_token, downloads_dir=app_config.dirs["downloads"], logged_in_user=args.user)
    
    try:
        # 3. Pipeline Initialization
        notifier = ConsoleNotifier()
        pipeline = PPTAutomationPipeline(
            data_fetcher=data_fetcher,
            ppt_template_path=app_config.template_path,
            manifest_path=app_config.manifest_path,
            output_dir=output_dir,
            notifier=notifier
        )
        
        job_manager = JobManager(pipeline)
        
        # 5. Execution
        job_id = job_manager.create_job(args.customer, args.month)
        job_manager.run_job(job_id)
        
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
