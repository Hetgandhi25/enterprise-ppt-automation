import os
import sys
import logging
from pathlib import Path
from PIL import Image, ImageChops

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ppt_to_images(ppt_path: Path, output_dir: Path):
    """
    Uses COM to export PPTX slides to PNG.
    Requires Windows and MS Office PowerPoint installed.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    import comtypes.client
    
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1
    
    # Needs absolute paths for COM
    abs_ppt = str(ppt_path.resolve())
    
    try:
        prs = powerpoint.Presentations.Open(abs_ppt, WithWindow=False)
        # Export each slide
        for i, slide in enumerate(prs.Slides):
            slide_path = str((output_dir / f"slide_{i+1}.png").resolve())
            slide.Export(slide_path, "PNG")
        prs.Close()
    finally:
        powerpoint.Quit()

def compare_images(img1_path: Path, img2_path: Path, diff_path: Path) -> float:
    """
    Compares two images. Returns the percentage of differing pixels.
    Saves a visual diff image.
    """
    img1 = Image.open(img1_path).convert('RGB')
    img2 = Image.open(img2_path).convert('RGB')
    
    diff = ImageChops.difference(img1, img2)
    diff.save(diff_path)
    
    # Calculate difference percentage
    bbox = diff.getbbox()
    if not bbox:
        return 0.0 # Exactly identical
        
    # Naive diff score based on bounding box is not ideal. Let's do pixel counting.
    diff_data = diff.getdata()
    diff_pixels = sum(1 for p in diff_data if p != (0,0,0))
    total_pixels = img1.width * img1.height
    
    return (diff_pixels / total_pixels) * 100

def run_visual_regression():
    master_ppt = Path("backend/templates/Sample MBR PPT_Formatted.pptx") # The reference the user uploaded might be Formatted(1).pptx, let's just use the current one.
    generated_ppt = Path("backend/output/presentations/Regression_Test.pptx")
    
    master_img_dir = Path("backend/qa/regression/master_images")
    gen_img_dir = Path("backend/qa/regression/gen_images")
    diff_dir = Path("backend/qa/regression/diffs")
    
    diff_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("Exporting Master PPT to images...")
    try:
        ppt_to_images(master_ppt, master_img_dir)
    except Exception as e:
        logger.error(f"COM Export failed. Please ensure MS PowerPoint is installed on this Windows host. Error: {e}")
        return
        
    logger.info("Exporting Generated PPT to images...")
    ppt_to_images(generated_ppt, gen_img_dir)
    
    logger.info("Comparing slides...")
    report = []
    
    for i in range(1, 16):
        m_img = master_img_dir / f"slide_{i}.png"
        g_img = gen_img_dir / f"slide_{i}.png"
        d_img = diff_dir / f"slide_{i}_diff.png"
        
        if m_img.exists() and g_img.exists():
            diff_score = compare_images(m_img, g_img, d_img)
            status = "PASS" if diff_score < 5.0 else "FAIL" # 5% tolerance for dynamic text differences
            report.append(f"Slide {i}: {status} ({diff_score:.2f}% difference)")
        else:
            report.append(f"Slide {i}: ERROR (Image missing)")
            
    print("\n" + "="*40)
    print("VISUAL REGRESSION REPORT")
    print("="*40)
    for line in report:
        print(line)
    print("="*40)
    print(f"Diff images saved to: {diff_dir}")

if __name__ == "__main__":
    # In a real run, you'd generate the PPT first here.
    run_visual_regression()
