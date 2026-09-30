from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt

from backend.charts.base_chart import BaseChart

class LocationSLAChart(BaseChart):
    """Generates a bar chart showing SLA percentage by Location."""
    
    def __init__(self, data: Dict[str, float], output_path: Path):
        # Match exactly the dimensions of the dummy picture (12.34 x 5.47 inches)
        super().__init__(output_path, width_inches=12.34, height_inches=5.47)
        self.data = data
        
    def validate_data(self) -> None:
        if not self.data:
            # Create a placeholder if no data is available
            self.data = {"No Data": 100.0}
            
    def render(self) -> None:
        locations = list(self.data.keys())
        slas = list(self.data.values())
        
        # Standard PPT Blue used in the original template
        ppt_blue = "#5B9BD5"
        
        # Draw bars
        bars = self.ax.bar(locations, slas, color=ppt_blue, width=0.4)
        
        # Title and Labels
        self.ax.set_title("Location Wise SLA", pad=20, fontsize=18, fontweight="bold", color="#2b579a")
        
        # The original chart has no Y-axis label or target line, and has values on top of bars
        for bar in bars:
            height = bar.get_height()
            self.ax.annotate(f'{height:.2f}%',
                             xy=(bar.get_x() + bar.get_width() / 2, height),
                             xytext=(0, 3),  # 3 points vertical offset
                             textcoords="offset points",
                             ha='center', va='bottom',
                             fontsize=9,
                             color="#333333")
                             
        # Auto-scale Y axis dynamically but keep bounds tight like original
        min_sla = min(slas) if slas else 99.0
        max_sla = max(slas) if slas else 100.0
        self.ax.set_ylim(bottom=min(100.0, max(0.0, min_sla - 1.0)), top=max(100.0, max_sla + 0.5))
        
        # Format Y-axis as percentage with 1 decimal place
        self.ax.yaxis.set_major_formatter('{x:.1f}%')
        
        plt.setp(self.ax.get_xticklabels(), rotation=45, ha="right", fontsize=10)
        
        # Add border around plot area
        for spine in self.ax.spines.values():
            spine.set_visible(True)
            spine.set_color('#cccccc')
            spine.set_linewidth(1)
