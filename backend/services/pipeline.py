import logging
from pathlib import Path
from collections import defaultdict
import pandas as pd

from backend.services.execution_context import ExecutionContext
from backend.services.progress_tracker import ProgressTracker
from backend.services.task_status import PipelineStage
from backend.services.metrics import MetricsCollector
from backend.services.cleanup import JobCleaner
from backend.services.notification import NotificationInterface

# Sub-modules
from backend.automation.data_fetcher import DataFetcher
from backend.processors.process_inventory import InventoryProcessor
from backend.processors.raw_ticket_processor import RawTicketProcessor
from backend.models.domain import RawTicketRecord, TicketAuditLog
from backend.processors.process_invoice import InvoiceProcessor
from backend.processors.process_retention import RetentionProcessor
from backend.charts.chart_generator import generate_sla_chart, generate_ticket_chart, generate_location_sla_chart, generate_sr_chart
from backend.ppt.ppt_generator import PPTGenerator

logger = logging.getLogger(__name__)

class PPTAutomationPipeline:
    """End-to-End Orchestrator Pipeline with Dependency Injection."""
    
    def __init__(self, 
                 data_fetcher: DataFetcher,
                 ppt_template_path: Path,
                 manifest_path: Path,
                 output_dir: Path,
                 notifier: NotificationInterface):
        self.data_fetcher = data_fetcher
        self.ppt_template_path = ppt_template_path
        self.manifest_path = manifest_path
        self.output_dir = output_dir
        self.notifier = notifier
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def execute(self, ctx: ExecutionContext, tracker: ProgressTracker, metrics: MetricsCollector):
        try:
            tracker.start()
            metrics.start_timer("total")
            
            # Stage 1: Download
            tracker.update_stage(PipelineStage.DOWNLOADING)
            metrics.start_timer("download")
            ctx.download_paths = self.data_fetcher.download_all(ctx.customer_id)
            metrics.stop_timer("download", "download_time_ms")
            
            # Stage 2: Processing Inventory
            tracker.update_stage(PipelineStage.PROCESSING_INVENTORY)
            metrics.start_timer("processing")
            inv_proc = InventoryProcessor(ctx.download_paths["inventory"])
            inventory_records, retention_metrics = inv_proc.process([ctx.customer_id])
            ctx.data["inventory_records"] = inventory_records
            ctx.summary.update(retention_metrics)
            
            # Stage 3 & 4: Processing Raw Tickets (SLA, Incidents, Flowchart)
            tracker.update_stage(PipelineStage.PROCESSING_SLA)
            
            raw_df = pd.read_excel(ctx.download_paths["raw_tickets"])
            # Filter for customer
            raw_df = raw_df[raw_df["Customer Name"] == ctx.customer_id]
            
            # Load Audit Logs
            audit_logs_dict = defaultdict(list)
            if "audit_logs" in ctx.download_paths and ctx.download_paths["audit_logs"].exists():
                audit_df = pd.read_excel(ctx.download_paths["audit_logs"])
                for _, row in audit_df.iterrows():
                    tid = str(row["Ticket ID"])
                    audit_logs_dict[tid].append(TicketAuditLog(
                        bucket_name=str(row["Bucket Name"]),
                        entry_time=str(row["Entry Time"]),
                        exit_time=str(row["Exit Time"])
                    ))
            
            raw_tickets = []
            for _, row in raw_df.iterrows():
                tid = str(row["Ticket ID"])
                raw_tickets.append(RawTicketRecord(
                    ticket_id=tid,
                    customer_name=str(row["Customer Name"]),
                    month=str(row["Month"]),
                    location=str(row["Location"]),
                    link_id=str(row["Link ID"]),
                    category=str(row["Category"]),
                    ticket_source=str(row.get("Ticket Source", "Reactive")),
                    status=str(row["Status"]),
                    subject_type=str(row["Subject Type"]),
                    rfo=str(row["RFO"]),
                    open_date=str(row["Open Date"]),
                    close_date=str(row["Close Date"]),
                    audit_logs=audit_logs_dict.get(tid, [])
                ))
                
            raw_proc = RawTicketProcessor(raw_tickets)
            
            # Assuming report_month is like '2026-07'. We will pass a dummy previous months list for demo.
            prev1 = ctx.report_month[:-1] + str(int(ctx.report_month[-1])-2) # crude logic, good for demo
            prev2 = ctx.report_month[:-1] + str(int(ctx.report_month[-1])-1)
            target_months = [prev1, prev2, ctx.report_month]
            
            processed_data = raw_proc.process_all(target_months=target_months)
            
            ctx.data["sla_records"] = processed_data["sla_records"]
            ctx.data["below_sla"] = processed_data["below_sla"]
            ctx.data["major_dt"] = processed_data["major_dt"]
            ctx.data["sla_by_location"] = processed_data.get("sla_by_location", {})
            ctx.data["flowchart_data"] = processed_data["flowchart_data"]
            ctx.data["incident_records"] = processed_data["incident_records"]
            
            # Stage 4b: Processing Finance (Invoices)
            if "invoices" in ctx.download_paths and ctx.download_paths["invoices"].exists():
                invc_proc = InvoiceProcessor(ctx.download_paths["invoices"])
                ctx.data["invoice_records"] = invc_proc.process([ctx.customer_id])
            else:
                ctx.data["invoice_records"] = []
                
            # Stage 4c: Processing Retention
            if "retention" in ctx.download_paths and ctx.download_paths["retention"].exists():
                ret_proc = RetentionProcessor(ctx.download_paths["retention"])
                ctx.data["retention_records"] = ret_proc.process([ctx.customer_id])
            else:
                ctx.data["retention_records"] = []

            metrics.stop_timer("processing", "excel_processing_time_ms")
            
            # Stage 5: Charts
            tracker.update_stage(PipelineStage.GENERATING_CHARTS)
            metrics.start_timer("charts")
            clean_cust = ctx.customer_id.replace(" ", "_").replace("/", "_")
            
            sla_chart = generate_sla_chart(ctx.data["sla_records"], clean_cust, ctx.report_month)
            ticket_chart = generate_ticket_chart(ctx.data["sla_records"], clean_cust, ctx.report_month)
            loc_sla_chart = generate_location_sla_chart(ctx.data["sla_by_location"], clean_cust, ctx.report_month)
            sr_chart = generate_sr_chart(ctx.data["flowchart_data"], clean_cust, ctx.report_month)
            ctx.chart_paths["sla"] = sla_chart
            ctx.chart_paths["ticket"] = ticket_chart
            ctx.chart_paths["loc_sla"] = loc_sla_chart
            ctx.chart_paths["sr"] = sr_chart
            
            ctx.data["sla_chart_path"] = sla_chart
            ctx.data["ticket_chart_path"] = ticket_chart
            ctx.data["loc_sla_chart_path"] = loc_sla_chart
            ctx.data["sr_chart_path"] = sr_chart
            metrics.stop_timer("charts", "chart_generation_time_ms")
            
            # 6. PPT Generation
            tracker.update_stage(PipelineStage.GENERATING_PPT)
            metrics.start_timer("ppt")
            
            # Translate CRM data to Normalized Report Data Object
            # Helper for explicit text conversion
            def fmt(val):
                if val is None or val == "":
                    return ""
                return str(val)

            # Extract metrics
            flow_data = ctx.data.get("flowchart_data", {})
            total_reqs = flow_data.get("{{total_requests_count}}")
            reqs = flow_data.get("{{requests_count}}")
            comps = flow_data.get("{{complaints_count}}")
            proact = flow_data.get("{{proactive_count}}")
            react = flow_data.get("{{reactive_count}}")
            ishan = flow_data.get("{{ishan_issue_count}}")
            cust = flow_data.get("{{customer_issue_count}}")

            complaints_series = []
            if all(v is not None for v in [proact, react, ishan, cust]):
                complaints_series = [float(proact), float(react), float(ishan), float(cust)]

            proactive_reactive = ""
            if proact is not None and react is not None:
                proactive_reactive = f"Proactive {proact}  Reactive {react}"

            normalized_data = {
                "customer_name": ctx.customer_id,
                "csm_block": {
                    "csm_name": fmt(self.data_fetcher.logged_in_user)
                },
                "mom_table": [],
                "overall_service_status": "",
                "service_request_trend": "",
                "customer_sentiment_csat": "",
                "customer_sentiment_nps": "",
                "action_taken": "",
                
                "customer_entities": "",
                "total_links": str(len(ctx.data.get("inventory_records", []))) if ctx.data.get("inventory_records") else "",
                "inventory_table": [ [r.customer_name, r.service_type, r.link_count] for r in ctx.data.get("inventory_records", []) ],
                
                "sla_trend_chart": {
                    "categories": [r.month for r in ctx.data.get("sla_records", [])],
                    "series": {"SLA %": [r.sla_percentage for r in ctx.data.get("sla_records", [])]} if ctx.data.get("sla_records") else {}
                },
                "service_request_chart": {
                    "categories": [r.month for r in ctx.data.get("sla_records", [])],
                    "series": {"Requests": [r.ticket_count for r in ctx.data.get("sla_records", [])]} if ctx.data.get("sla_records") else {}
                },
                "location_sla_chart": {
                    "categories": list(ctx.data.get("sla_by_location", {}).keys()),
                    "series": {"Uptime %": list(ctx.data.get("sla_by_location", {}).values())} if ctx.data.get("sla_by_location") else {}
                },
                
                "total_service_requests": fmt(total_reqs),
                "total_requests": fmt(reqs),
                "total_complaints": fmt(comps),
                "complaints_chart": {
                    "categories": ["Proactive", "Reactive", "Ishan End", "Customer End"] if complaints_series else [],
                    "series": {"Count": complaints_series} if complaints_series else {}
                },
                "proactive_reactive": proactive_reactive,
                "issue_ishan_end_count": fmt(ishan),
                "issue_customer_end_count": fmt(cust),
                
                "incident_table": [ [r.location, r.cable_issue, r.backhaul_impacted, r.electricity_issue] for r in ctx.data.get("incident_records", []) ],
                "projects_table": [],
                "retention_table": [ [r.location, "Pending", r.last_date] for r in ctx.data.get("retention_records", []) ],
                "invoice_table": [ [str(idx + 1), r.service_code, r.invoice_date, fmt(r.opening_balance), r.ageing_bucket] for idx, r in enumerate(ctx.data.get("invoice_records", [])) ],
                "total_outstanding": "", 
                "open_invoices": str(len(ctx.data.get("invoice_records", []))) if ctx.data.get("invoice_records") else "",
                "escalation_table": [],
                "customer_reference": ctx.customer_id
            }
            
            generator = PPTGenerator(self.ppt_template_path, self.manifest_path)
            final_path = self.output_dir / f"{clean_cust}_{ctx.report_month}_{ctx.job_id}.pptx"
            generator.generate(normalized_data, final_path)
            ctx.final_ppt_path = final_path
            metrics.stop_timer("ppt", "ppt_generation_time_ms")
            
            # Stage 7: Cleanup
            tracker.update_stage(PipelineStage.CLEANUP)
            JobCleaner.cleanup(ctx)
            
            # Success
            metrics.stop_timer("total", "total_runtime_ms")
            tracker.complete()
            ctx.mark_completed()
            self.notifier.send_success(ctx.job_id, str(ctx.final_ppt_path))
            
        except Exception as e:
            logger.error(f"Pipeline failed for {ctx.customer_id}: {e}")
            tracker.fail(str(e))
            ctx.mark_completed()
            metrics.stop_timer("total", "total_runtime_ms")
            self.notifier.send_failure(ctx.job_id, str(e))
            # Attempt cleanup on failure but preserve PPT if it was somehow generated
            try:
                JobCleaner.cleanup(ctx)
            except Exception as ce:
                logger.warning(f"Cleanup during failure failed: {ce}")
            raise
