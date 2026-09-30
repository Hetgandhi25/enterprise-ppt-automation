import logging
import yaml
from pathlib import Path
from typing import Dict, Any

from pptx import Presentation
from .shape_resolver import find_shape_by_id
from .text_updater import update_text_preserve_style
from .table_updater import update_table_in_place
from .chart_updater import update_chart_in_place

logger = logging.getLogger(__name__)

class PPTGenerator:
    def __init__(self, template_path: Path, manifest_path: Path):
        self.template_path = template_path
        self.manifest_path = manifest_path
        with open(manifest_path, 'r', encoding='utf-8') as f:
            self.manifest = yaml.safe_load(f)

    def generate(self, data: Dict[str, Any], output_path: Path):
        logger.info(f"Loading template from {self.template_path}")
        prs = Presentation(self.template_path)
        
        # Ensure slide count matches manifest expectations
        # The manifest is written with keys like "slide_1", "slide_2" etc.
        
        slides_manifest = self.manifest.get("slides", {})
        
        for slide_key, element_mappings in slides_manifest.items():
            # Parse slide index (e.g., "slide_1" -> index 0)
            try:
                slide_idx = int(slide_key.split('_')[1]) - 1
            except:
                continue
                
            if slide_idx >= len(prs.slides):
                logger.warning(f"Slide index {slide_idx} out of range.")
                continue
                
            slide = prs.slides[slide_idx]
            
            # Skip if pass: true
            if element_mappings.get("pass"):
                continue
                
            # Process each mapped element
            for logical_name, shape_id_str in element_mappings.items():
                if logical_name == "pass": continue
                
                # The data dict should contain corresponding data for logical_name
                # If not, skip
                if logical_name not in data:
                    logger.debug(f"Missing data for '{logical_name}'. Skipping.")
                    continue
                    
                target_data = data[logical_name]
                
                paragraph_mapping = None
                is_dynamic = True
                
                if isinstance(shape_id_str, dict):
                    clean_id_str = str(shape_id_str.get('shape_id', '')).replace('text_', '').replace('table_', '').replace('chart_', '')
                    paragraph_mapping = shape_id_str.get('fields')
                    is_dynamic = shape_id_str.get('dynamic', True)
                    template_str = shape_id_str.get('template')
                    if template_str and target_data:
                        target_data = template_str.replace('{customer}', str(target_data))
                    elif template_str and not target_data:
                        target_data = ""
                        
                    is_text = 'text' in str(shape_id_str.get('shape_id', ''))
                    is_table = 'table' in str(shape_id_str.get('shape_id', ''))
                    is_chart = 'chart' in str(shape_id_str.get('shape_id', ''))
                else:
                    clean_id_str = str(shape_id_str).replace('text_', '').replace('table_', '').replace('chart_', '')
                    is_text = 'text' in str(shape_id_str)
                    is_table = 'table' in str(shape_id_str)
                    is_chart = 'chart' in str(shape_id_str)
                
                if not is_dynamic:
                    continue
                
                shape = find_shape_by_id(slide, clean_id_str)
                
                if not shape:
                    logger.warning(f"Shape ID '{clean_id_str}' not found on {slide_key}")
                    continue
                    
                # Identify expected action by shape type or logical name
                if is_text or shape.has_text_frame:
                    if paragraph_mapping:
                        update_text_preserve_style(shape, target_data, paragraph_mapping)
                    else:
                        update_text_preserve_style(shape, target_data)
                elif is_table or shape.has_table:
                    update_table_in_place(shape, target_data)
                elif is_chart or shape.has_chart:
                    target_categories = target_data.get('categories', []) if target_data else []
                    target_series = target_data.get('series', {}) if target_data else {}
                    update_chart_in_place(shape, target_categories, target_series)

        logger.info(f"Saving generated PPT to {output_path}")
        prs.save(output_path)
        
        from .validator import PPTValidator
        validator = PPTValidator(expected_slide_count=15)
        validator.validate(output_path)
        
        return output_path
