import logging
from pathlib import Path
from backend.utils.logger import setup_logging
from backend.automation.automation_runner import AutomationRunner
from backend.automation.mock_crm_adapter import MockCRMAdapter

def run_automation_demo():
    setup_logging()
    logger = logging.getLogger("automation_demo")
    
    base_dir = Path(__file__).parent
    
    # Configure framework
    config = {
        "headless": True,
        "downloads_dir": str(base_dir / "output" / "downloads"),
        "screenshots_dir": str(base_dir / "logs" / "screenshots"),
        "auth_file": str(base_dir / "config" / "auth.json"),
        "selectors_file": str(base_dir / "config" / "portal.json")
    }
    
    # Patch the portal.json with absolute path to mock html
    mock_html_path = base_dir / "tests" / "fixtures" / "mock_portal.html"
    mock_url = f"file:///{str(mock_html_path).replace(chr(92), '/')}"
    
    import json
    with open(config["selectors_file"], "r") as f:
        data = json.load(f)
    data["selectors"]["urls"]["login"] = mock_url
    with open(config["selectors_file"], "w") as f:
        json.dump(data, f, indent=4)
        
    logger.info("Starting Automation Framework Demo.")
    runner = AutomationRunner(config, MockCRMAdapter)
    
    credentials = {
        "username": "demo_user",
        "password": "demo_password"
    }
    
    customer_id = "ASG India"
    
    try:
        reports = runner.run_job(customer_id, credentials)
        print("Demo completed successfully!")
        for key, path in reports.items():
            print(f"Downloaded {key}: {path}")
    except Exception as e:
        logger.error(f"Demo failed: {e}")

if __name__ == "__main__":
    run_automation_demo()
