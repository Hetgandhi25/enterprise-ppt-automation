import logging
import os
from pathlib import Path
from backend.services.execution_context import ExecutionContext

logger = logging.getLogger(__name__)

class JobCleaner:
    """Handles cleaning up temporary files generated during a job."""
    
    @staticmethod
    def cleanup(context: ExecutionContext) -> None:
        logger.info(f"[{context.job_id}] Starting cleanup.")
        
        # Cleanup downloads
        for name, path in context.download_paths.items():
            if path.exists():
                try:
                    os.remove(path)
                    logger.debug(f"[{context.job_id}] Deleted temporary download: {path}")
                except Exception as e:
                    logger.warning(f"[{context.job_id}] Failed to delete {path}: {e}")
                    
        # Cleanup charts
        for name, path in context.chart_paths.items():
            if path.exists():
                try:
                    os.remove(path)
                    logger.debug(f"[{context.job_id}] Deleted temporary chart: {path}")
                except Exception as e:
                    logger.warning(f"[{context.job_id}] Failed to delete {path}: {e}")
                    
        logger.info(f"[{context.job_id}] Cleanup complete. Generated PPT is preserved at {context.final_ppt_path}")
