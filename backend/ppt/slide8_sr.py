from pathlib import Path
from backend.ppt.base_ppt import BasePPT
from backend.ppt.image_replacer import replace_image
from backend.utils.exceptions import PPTGenerationError

class Slide8ServiceRequests(BasePPT):
    
    def __init__(self, prs):
        # Target Index 7 (Page 8: Service Requests Snapshot)
        super().__init__(prs, 7)
        
    def populate(self, sr_chart_path: Path) -> None:
        try:
            target_shape = self.slide.shapes[1] # Slide 8 -> Shape 1 is Picture 1
            if getattr(target_shape, 'shape_type', None) == 13:
                replace_image(self.slide, target_shape, sr_chart_path)
            else:
                for shape in self.slide.shapes:
                    if getattr(shape, 'shape_type', None) == 13:
                        replace_image(self.slide, shape, sr_chart_path)
                        break
        except Exception as e:
            raise PPTGenerationError(f"Failed to replace SR chart: {e}")
