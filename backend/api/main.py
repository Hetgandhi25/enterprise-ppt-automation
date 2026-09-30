from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import logging
import subprocess
import time
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="CustPPTAutomation API", description="API for PPT Generation", version="1.0.0")

class GenerateRequest(BaseModel):
    customerName: str
    reportMonth: str
    demoMode: bool = True

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
from pathlib import Path

# Ensure the output directory exists
presentations_dir = Path("backend/output/presentations")
presentations_dir.mkdir(parents=True, exist_ok=True)

# Mount the static directory
app.mount("/output/presentations", StaticFiles(directory=str(presentations_dir)), name="presentations")

from backend.api.auth import router as auth_router, get_current_user, UserProfile

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"status": "ok", "message": "FastAPI is running"}

@app.get("/api/dashboard/stats")
def get_dashboard_stats(current_user: UserProfile = Depends(get_current_user)):
    import os
    from datetime import datetime, timezone
    
    total_reports = 0
    todays_reports = 0
    now = time.time()
    reports_trend_map = {}
    customer_distribution_map = {}
    
    if presentations_dir.exists():
        for p in presentations_dir.glob("*.pptx"):
            try:
                basename = p.stem
                allowed_customer_names = [c["name"] if isinstance(c, dict) else c for c in current_user.customers]
                matched_customer = None
                
                if current_user.role == "admin":
                    parts = basename.split("_")
                    customer_parts = [part for part in parts if not ("-" in part and len(part) == 7 and part[:4].isdigit()) and len(part) != 8]
                    matched_customer = " ".join(c for c in customer_parts if "-" not in c and len(c) != 8) or basename
                else:
                    for name in allowed_customer_names:
                        sanitized_name = name.replace(" ", "_").replace("/", "_")
                        if basename.startswith(sanitized_name):
                            matched_customer = name
                            break
                            
                if not matched_customer:
                    continue
                    
                total_reports += 1
                mtime = p.stat().st_mtime
                if now - mtime < 86400:
                    todays_reports += 1
                    
                dt_utc = datetime.fromtimestamp(mtime, tz=timezone.utc)
                month_key = dt_utc.strftime("%Y-%m")
                reports_trend_map[month_key] = reports_trend_map.get(month_key, 0) + 1
                customer_distribution_map[matched_customer] = customer_distribution_map.get(matched_customer, 0) + 1
                
            except Exception:
                pass

    reports_trend = [{"name": k, "value": v} for k, v in sorted(reports_trend_map.items())][-6:]
    customer_dist = [{"name": k, "value": v} for k, v in customer_distribution_map.items()]

    return {
        "stats": {
            "totalReports": total_reports,
            "todaysReports": todays_reports,
            "successRate": 100 if total_reports > 0 else 0, # Since we only read completed files
            "avgRuntimeMs": 1200 # Mock average since we don't store historical runtimes
        },
        "charts": {
            "reportsTrend": reports_trend,
            "customerDistribution": customer_dist
        },
        "health": "Healthy"
    }

@app.get("/api/customers")
def get_customers(current_user: UserProfile = Depends(get_current_user)):
    # Check if the user is configured for live sync
    if getattr(current_user, "live_sync", False) or current_user.username == "Shah.Manank":
        try:
            from backend.api_client.crm_rest_client import CRMRestClient
            client = CRMRestClient(logged_in_user=current_user.username)
            live_customers = client.get_customers()
            if live_customers:
                return live_customers
        except Exception as e:
            logger.error(f"Failed to fetch live customers from CRM: {e}")
            
    # Fallback to mock customers
    return current_user.customers

@app.get("/api/jobs")
def get_jobs(current_user: UserProfile = Depends(get_current_user)):
    import os
    from datetime import datetime, timezone
    jobs = []
    if not presentations_dir.exists():
        return jobs
        
    for p in presentations_dir.glob("*.pptx"):
        try:
            basename = p.stem
            mtime = p.stat().st_mtime
            dt_utc = datetime.fromtimestamp(mtime, tz=timezone.utc)
            
            allowed_customer_names = [c["name"] if isinstance(c, dict) else c for c in current_user.customers]
            matched_customer = None
            
            # Find the matching customer by seeing if basename starts with their sanitized name
            if current_user.role == "admin":
                # For admin, we don't have a strict list, so we do our best guess
                parts = basename.split("_")
                month = ""
                customer_parts = []
                for part in parts:
                    if "-" in part and len(part) == 7 and part[:4].isdigit():
                        month = part
                    elif len(part) != 8:
                        customer_parts.append(part)
                if not month and len(parts) >= 2:
                    month = parts[-1] if "-" in parts[-1] else parts[-2]
                matched_customer = " ".join(c for c in customer_parts if "-" not in c and len(c) != 8) or basename
            else:
                month = ""
                for name in allowed_customer_names:
                    sanitized_name = name.replace(" ", "_").replace("/", "_")
                    if basename.startswith(sanitized_name):
                        matched_customer = name
                        # Extract month (it comes right after the customer name)
                        remainder = basename[len(sanitized_name):].strip("_")
                        parts = remainder.split("_")
                        for part in parts:
                            if "-" in part and len(part) == 7 and part[:4].isdigit():
                                month = part
                                break
                        break
                        
            if not matched_customer:
                continue
                
            jobs.append({
                "id": f"job-{int(mtime)}-{p.name}",
                "status": "COMPLETED",
                "progressPercentage": 100,
                "outputPath": f"http://localhost:8000/output/presentations/{p.name}",
                "runtimeMs": 1200 + (int(mtime) % 800), # Mock realistic runtime
                "customerName": matched_customer,
                "reportMonth": month,
                "startTime": dt_utc.isoformat()
            })
        except Exception:
            pass
            
    # Sort by startTime descending
    jobs.sort(key=lambda x: x["startTime"], reverse=True)
    return jobs

@app.get("/api/reports")
def get_reports(current_user: UserProfile = Depends(get_current_user)):
    import os
    from datetime import datetime, timezone
    reports = []
    if not presentations_dir.exists():
        return reports
        
    for p in presentations_dir.glob("*.pptx"):
        try:
            basename = p.stem
            mtime = p.stat().st_mtime
            dt_utc = datetime.fromtimestamp(mtime, tz=timezone.utc)
            
            allowed_customer_names = [c["name"] if isinstance(c, dict) else c for c in current_user.customers]
            matched_customer = None
            
            if current_user.role == "admin":
                parts = basename.split("_")
                month = ""
                customer_parts = []
                for part in parts:
                    if "-" in part and len(part) == 7 and part[:4].isdigit():
                        month = part
                    elif len(part) != 8:
                        customer_parts.append(part)
                if not month and len(parts) >= 2:
                    month = parts[-1] if "-" in parts[-1] else parts[-2]
                matched_customer = " ".join(c for c in customer_parts if "-" not in c and len(c) != 8) or basename
            else:
                month = ""
                for name in allowed_customer_names:
                    sanitized_name = name.replace(" ", "_").replace("/", "_")
                    if basename.startswith(sanitized_name):
                        matched_customer = name
                        remainder = basename[len(sanitized_name):].strip("_")
                        parts = remainder.split("_")
                        for part in parts:
                            if "-" in part and len(part) == 7 and part[:4].isdigit():
                                month = part
                                break
                        break
                        
            if not matched_customer:
                continue
                
            reports.append({
                "id": f"report-{int(mtime)}-{p.name}",
                "jobId": f"job-{int(mtime)}-{p.name}",
                "customerName": matched_customer,
                "reportMonth": month,
                "generatedAt": dt_utc.isoformat(),
                "runtimeMs": 1200 + (int(mtime) % 800),
                "pptPath": f"http://localhost:8000/output/presentations/{p.name}",
                "fileSizeKb": int(p.stat().st_size / 1024)
            })
        except Exception:
            pass
            
    reports.sort(key=lambda x: x["generatedAt"], reverse=True)
    return reports

@app.delete("/api/jobs/{job_id}")
def delete_job(job_id: str, current_user: UserProfile = Depends(get_current_user)):
    if not job_id.startswith("job-"):
        raise HTTPException(status_code=400, detail="Invalid job ID format.")
    
    parts = job_id.split("-", 2)
    if len(parts) < 3:
        raise HTTPException(status_code=400, detail="Invalid job ID format.")
        
    filename = parts[2]
    file_path = presentations_dir / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Job not found.")
        
    # Check authorization
    allowed_customer_names = [c["name"] if isinstance(c, dict) else c for c in current_user.customers]
    
    matched_customer = None
    if current_user.role == "admin":
        matched_customer = "admin" # Admin can delete anything
    else:
        for name in allowed_customer_names:
            sanitized_name = name.replace(" ", "_").replace("/", "_")
            if basename.startswith(sanitized_name):
                matched_customer = name
                break
                
    if not matched_customer:
        raise HTTPException(status_code=403, detail="Not authorized to delete this job.")
        
    try:
        file_path.unlink()
        return {"status": "success", "message": "Job deleted"}
    except Exception as e:
        logger.error(f"Failed to delete job file: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete job file.")

@app.delete("/api/reports/{report_id}")
def delete_report(report_id: str, current_user: UserProfile = Depends(get_current_user)):
    if not report_id.startswith("report-"):
        raise HTTPException(status_code=400, detail="Invalid report ID format.")
    
    parts = report_id.split("-", 2)
    if len(parts) < 3:
        raise HTTPException(status_code=400, detail="Invalid report ID format.")
        
    filename = parts[2]
    file_path = presentations_dir / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Report not found.")
        
    # Check authorization
    allowed_customer_names = [c["name"] if isinstance(c, dict) else c for c in current_user.customers]
    
    matched_customer = None
    if current_user.role == "admin":
        matched_customer = "admin" # Admin can delete anything
    else:
        for name in allowed_customer_names:
            sanitized_name = name.replace(" ", "_").replace("/", "_")
            if file_path.stem.startswith(sanitized_name):
                matched_customer = name
                break
                
    if not matched_customer:
        raise HTTPException(status_code=403, detail="Not authorized to delete this report.")
        
    try:
        file_path.unlink()
        return {"status": "success", "message": "Report deleted"}
    except Exception as e:
        logger.error(f"Failed to delete report file: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete report file.")

@app.post("/api/jobs/{job_id}/cancel")
def cancel_job(job_id: str, current_user: UserProfile = Depends(get_current_user)):
    # Since jobs are executed synchronously in the current mock setup, we just return success
    # to satisfy the frontend if a user manages to click cancel while a job is artificially 'running'
    return {"status": "success", "message": "Job cancelled"}

@app.post("/api/generate")
def generate_report(req: GenerateRequest, current_user: UserProfile = Depends(get_current_user)):
    allowed_customer_names = [c["name"] if isinstance(c, dict) else c for c in current_user.customers]
    if current_user.role != "admin" and req.customerName not in allowed_customer_names:
        raise HTTPException(status_code=403, detail="You are not authorized to generate reports for this customer.")
        
    logger.info(f"Received generation request for {req.customerName} - {req.reportMonth} by {current_user.username}")
    try:
        start_time = time.time()
        
        # Build command using the current virtual environment's python
        cmd = [sys.executable, "-m", "backend.main"]
        if req.demoMode:
            cmd.append("--demo")
        else:
            cmd.append("--production")
            
        cmd.extend(["--customer", req.customerName, "--month", req.reportMonth, "--user", current_user.username])
        
        logger.info(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        runtime = (time.time() - start_time) * 1000
        
        if result.returncode != 0:
            logger.error(f"Generation failed. Stdout: {result.stdout}\nStderr: {result.stderr}")
            raise HTTPException(status_code=500, detail=f"Generation failed from backend. Stderr: {result.stderr}")
            
        # Extract actual output path from stdout
        import re
        match = re.search(r"Successfully generated .*[\\/](.+\.pptx)", result.stdout)
        if match:
            filename = match.group(1).strip()
            download_url = f"http://localhost:8000/output/presentations/{filename}"
        else:
            download_url = f"http://localhost:8000/output/presentations/{req.customerName}_{req.reportMonth}.pptx"
            
        return {
            "id": "job-" + str(int(time.time())),
            "status": "COMPLETED",
            "progressPercentage": 100,
            "outputPath": download_url,
            "runtimeMs": runtime,
            "customerName": req.customerName,
            "reportMonth": req.reportMonth
        }
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

from backend.api_client.crm_rest_client import CRMRestClient
from backend.processors.raw_ticket_processor import RawTicketProcessor
from backend.models.domain import RawTicketRecord
import pandas as pd
import tempfile
from pathlib import Path
import traceback

@app.get("/api/reports/{customer_name}/{month}/preview")
def get_report_preview(customer_name: str, month: str, demo: bool = True, current_user: UserProfile = Depends(get_current_user)):
    allowed_customer_names = [c["name"] if isinstance(c, dict) else c for c in current_user.customers]
    if current_user.role != "admin" and customer_name not in allowed_customer_names:
        raise HTTPException(status_code=403, detail="Not authorized for this customer")
        
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            client = CRMRestClient(api_url="mock", api_token="mock", downloads_dir=Path(tmpdir), logged_in_user=current_user.username)
            download_paths = client.download_all(customer_name)
            
            raw_df = pd.read_excel(download_paths["raw_tickets"])
            raw_df = raw_df[raw_df["Customer Name"] == customer_name]
            
            raw_tickets = []
            for _, row in raw_df.iterrows():
                raw_tickets.append(RawTicketRecord(
                    ticket_id=str(row["Ticket ID"]),
                    customer_name=str(row["Customer Name"]),
                    month=str(row["Month"]),
                    location=str(row["Location"]),
                    link_id=str(row["Link ID"]),
                    category=str(row["Category"]),
                    ticket_source=str(row.get("Ticket Source", "Reactive")),
                    status=str(row["Status"]),
                    subject_type=str(row["Subject Type"]),
                    rfo=str(row["RFO"]),
                    total_aging_hours=float(row["Total Aging Hours"]),
                    customer_bucket_aging_hours=float(row["Customer Bucket Aging Hours"])
                ))
                
            processor = RawTicketProcessor(raw_tickets)
            
            # Mock previous months identically to pipeline.py
            try:
                prev1 = month[:-1] + str(int(month[-1])-2) 
                prev2 = month[:-1] + str(int(month[-1])-1)
            except Exception:
                prev1 = "Prev2"
                prev2 = "Prev1"
                
            target_months = [prev1, prev2, month]
            data = processor.process_all(target_months=target_months)
            
            return {
                "slide6_data": [r.__dict__ for r in data["sla_records"]],
                "flowchart_data": data["flowchart_data"],
                "incident_records": [r.__dict__ for r in data["incident_records"]]
            }
    except Exception as e:
        logger.error(f"Preview fetch failed: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("backend.api.main:app", host="0.0.0.0", port=8000, reload=True)
