from pathlib import Path
from backend.ppt.base_ppt import BasePPT
from backend.ppt.placeholder_mapper import find_placeholder, find_shape_by_position
from backend.ppt.image_replacer import replace_image
from backend.utils.exceptions import PPTGenerationError

class Slide6Performance(BasePPT):
    
    def __init__(self, prs):
        # Target Index 5 (Page 6: Service Performance Summary)
        super().__init__(prs, 5)
        
    def populate(self, sla_chart_path: Path, ticket_chart_path: Path) -> None:
        # Find all picture shapes on the slide
        pictures = [s for s in self.slide.shapes if getattr(s, 'shape_type', None) == 13]
        
        if len(pictures) >= 2:
            # Sort by left position to ensure we get left and right charts correctly
            pictures.sort(key=lambda s: s.left)
            
            # Left picture is SLA Chart, Right picture is Ticket Chart
            replace_image(self.slide, pictures[0], sla_chart_path)
            replace_image(self.slide, pictures[1], ticket_chart_path)
        else:
            raise PPTGenerationError(f"Expected 2 picture shapes on Slide 6, found {len(pictures)}")
