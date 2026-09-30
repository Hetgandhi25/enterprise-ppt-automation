import os
import hashlib
import logging
from pathlib import Path
from backend.ppt.ppt_generator import PPTGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def hash_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def run_qa():
    template_path = Path("backend/templates/MBR_Template_v1.pptx")
    manifest_path = Path("backend/templates/template_manifest.yaml")
    
    # 1. Hash Master
    master_hash_before = hash_file(template_path)
    
    generator = PPTGenerator(template_path, manifest_path)
    
    # CASE 1: Empty Data
    logger.info("--- RUNNING EMPTY DATA TEST ---")
    empty_data = {}
    generator.generate(empty_data, Path("backend/generated/QA_Empty_Data.pptx"))
    
    # CASE 2: Overflow Data
    logger.info("--- RUNNING OVERFLOW DATA TEST ---")
    overflow_data = {
        "mom_table": [
            ["1", "Issue A", "Team", "Status", "Date"] for _ in range(15) # Template has ~6 rows
        ],
        "overall_service_status": "Lots of text here " * 50 # Long text
    }
    generator.generate(overflow_data, Path("backend/generated/QA_Overflow_Data.pptx"))
    
    # 3. Hash Master Again
    master_hash_after = hash_file(template_path)
    
    print("\n================ PPT QA REPORT ================\n")
    
    immutability_pass = (master_hash_before == master_hash_after)
    print(f"Master Template Immutability: {'PASS' if immutability_pass else 'FAIL'}")
    if not immutability_pass:
        print(f"  Hash Before: {master_hash_before}")
        print(f"  Hash After:  {master_hash_after}")
        
    print("Visual Overflow Check: Please inspect QA_Overflow_Data.pptx")
    print("Empty Handling Check: Please inspect QA_Empty_Data.pptx")
    
    print("\nRun backend/qa/validate_template.py for manifest structural integrity.")
    print("===============================================\n")

if __name__ == "__main__":
    run_qa()
