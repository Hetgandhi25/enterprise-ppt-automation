from pathlib import Path
from backend.ppt.base_ppt import BasePPT
from backend.ppt.image_replacer import replace_image
from backend.utils.exceptions import PPTGenerationError

class Slide7LocationSLA(BasePPT):
    
    def __init__(self, prs):
        # Target Index 6 (Page 7: Location Wise SLA)
        super().__init__(prs, 6)
        
    def populate(self, loc_sla_chart_path: Path) -> None:
        # The Location SLA chart is Picture 1 according to our python-pptx analysis
        try:
            target_shape = self.slide.shapes[1] # Slide 7 -> Shape 1 is Picture 1
            if getattr(target_shape, 'shape_type', None) == 13: # MSO_SHAPE_TYPE.PICTURE
                replace_image(self.slide, target_shape, loc_sla_chart_path)
            else:
                # Search for it if indices shifted
                for shape in self.slide.shapes:
                    if getattr(shape, 'shape_type', None) == 13:
                        replace_image(self.slide, shape, loc_sla_chart_path)
                        break
        except Exception as e:
            raise PPTGenerationError(f"Failed to replace location SLA chart: {e}")
