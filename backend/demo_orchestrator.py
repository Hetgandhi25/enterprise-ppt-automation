import logging
import time
import psutil
import os
import json
from pathlib import Path
from backend.utils.logger import setup_logging
from backend.services.pipeline import PPTAutomationPipeline
from backend.services.job_manager import JobManager
from backend.services.notification import ConsoleNotifier
from backend.automation.portal_client import PortalClient
from backend.automation.mock_crm_adapter import MockCRMAdapter

def generate_reports(num_reports: int) -> dict:
    setup_logging()
    logger = logging.getLogger("orchestrator_demo")
    base_dir = Path(__file__).parent
    
    config = {
        "headless": True,
        "downloads_dir": str(base_dir / "output" / "downloads"),
        "screenshots_dir": str(base_dir / "logs" / "screenshots"),
        "auth_file": str(base_dir / "config" / "auth.json"),
        "selectors_file": str(base_dir / "config" / "portal.json")
    }
    
    # We clear auth json to ensure a clean start if we wanted, but let's keep it to test session resume speed
    
    # Initialize Core Components
    client = PortalClient(config, MockCRMAdapter)
    
    # Ensure mock URL is set
    mock_html_path = base_dir / "tests" / "fixtures" / "mock_portal.html"
    mock_url = f"file:///{str(mock_html_path).replace(chr(92), '/')}"
    with open(config["selectors_file"], "r") as f:
        data = json.load(f)
    data["selectors"]["urls"]["login"] = mock_url
    with open(config["selectors_file"], "w") as f:
        json.dump(data, f, indent=4)
        
    client.start({"username": "demo", "password": "pwd"})
    
    notifier = ConsoleNotifier()
    template_path = base_dir / "templates" / "ServiceReview.pptx"
    out_dir = base_dir / "output" / "presentations"
    
    pipeline = PPTAutomationPipeline(client, template_path, out_dir, notifier)
    
    import shutil
    def fake_download_all(customer_id):
        paths = {}
        file_map = {
            "inventory": "Customer_Service_Report.xlsx",
            "sla": "SLA_Report.xlsx",
            "location_sla": "Location_SLA_Report.xlsx",
            "incidents": "Incident_Report.xlsx"
        }
        dst_dir = out_dir.parent / "downloads"
        dst_dir.mkdir(parents=True, exist_ok=True)
        for rtype, fname in file_map.items():
            src = base_dir / "tests" / "fixtures" / fname
            dst = dst_dir / f"{rtype}_{customer_id}.xlsx"
            if src.exists():
                shutil.copy(src, dst)
            paths[rtype] = dst
        return paths
        
    job_manager = JobManager(pipeline)
    
    customers = ["ASG India"]
    
    logger.info(f"Starting performance test for {num_reports} reports.")
    start_total = time.time()
    
    for i in range(num_reports):
        cust = customers[i % len(customers)]
        job_id = job_manager.create_job(cust, f"2026-07")
        
        # Monkeypatch the pipeline downloader for this job to use fixtures
        # since mock_portal.html only downloads plain text which breaks pandas
        original_downloader = pipeline.portal_client.get_downloader
        class FakeDownloader:
            def download_all(self, cid):
                return fake_download_all(cid)
        pipeline.portal_client.get_downloader = lambda: FakeDownloader()
        
        try:
            job_manager.run_job(job_id)
        except Exception as e:
            logger.error(f"Job {job_id} failed: {e}")
            
    client.close()
    
    end_total = time.time()
    
    # Analyze metrics
    runtimes = []
    memories = []
    failures = 0
    for jid, metric in job_manager.metrics.items():
        if job_manager.trackers[jid].status.value == "FAILED":
            failures += 1
        else:
            runtimes.append(metric.metrics.total_runtime_ms)
            memories.append(metric.metrics.peak_memory_mb)
            
    avg_runtime = sum(runtimes) / len(runtimes) if runtimes else 0
    fastest = min(runtimes) if runtimes else 0
    slowest = max(runtimes) if runtimes else 0
    avg_mem = sum(memories) / len(memories) if memories else 0
    
    process = psutil.Process(os.getpid())
    peak_mem_overall = process.memory_info().rss / (1024 * 1024)
    
    return {
        "count": num_reports,
        "total_time_s": end_total - start_total,
        "avg_runtime_ms": avg_runtime,
        "fastest_ms": fastest,
        "slowest_ms": slowest,
        "avg_mem_mb": avg_mem,
        "peak_mem_overall_mb": peak_mem_overall,
        "failures": failures
    }

if __name__ == "__main__":
    print("Running 10 reports...")
    res_10 = generate_reports(10)
    print("Running 25 reports...")
    res_25 = generate_reports(25)
    print("Running 50 reports...")
    res_50 = generate_reports(50)
    
    print("\n--- RESULTS ---")
    print(res_10)
    print(res_25)
    print(res_50)
    
    # Save results to a file for artifact generation
    with open("perf_results.json", "w") as f:
        json.dump([res_10, res_25, res_50], f, indent=4)
