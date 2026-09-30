from pathlib import Path
from typing import List
from datetime import datetime
import numpy as np

from backend.charts.base_chart import BaseChart
from backend.charts.theme_loader import ThemeLoader
from backend.models.domain import SLARecord
from backend.utils.exceptions import ChartGenerationError

class SLATrendChart(BaseChart):
    """Generates the SLA Trend Bar Chart."""
    
    def __init__(self, data: List[SLARecord], output_path: Path):
        super().__init__(output_path, width_inches=6.0, height_inches=4.0)
        self.data = data
        
    def validate_data(self) -> None:
        """Validates SLA data constraints."""
        if not self.data:
            raise ChartGenerationError("Empty data provided for SLA chart.")
        if any(r.sla_percentage < 0 or r.sla_percentage > 100 for r in self.data):
            raise ChartGenerationError("Invalid SLA percentage")
        months = [r.month for r in self.data]
        if len(months) != len(set(months)):
            raise ChartGenerationError("Duplicate month in data")
            
    def render(self) -> None:
        """Renders the SLA bars and trend line matching the original PPT exactly."""
        # Convert YYYY-MM to short month name (e.g. 'Apr', 'May')
        months = []
        for r in self.data:
            try:
                months.append(datetime.strptime(r.month, "%Y-%m").strftime("%b"))
            except ValueError:
                months.append(r.month)
                
        sla_values = [record.sla_percentage for record in self.data]
        
        # Standard PPT Blue
        ppt_blue = "#5B9BD5"
        
        # Bars (thinner width like original)
        bars = self.ax.bar(months, sla_values, color=ppt_blue, width=0.3)
        
        # Trend Line (dotted blue)
        # Using numpy polyfit to draw a straight trendline
        x = np.arange(len(months))
        if len(x) > 1:
            z = np.polyfit(x, sla_values, 1)
            p = np.poly1d(z)
            self.ax.plot(x, p(x), color=ppt_blue, linestyle=':', linewidth=1.5)
        
        # Y-axis scaling (zoom in to match the original feel)
        min_sla = min(sla_values) if sla_values else 99.5
        max_sla = max(sla_values) if sla_values else 100.0
        y_min = min_sla - 0.2
        y_max = max(100.0, max_sla + 0.1)
        self.ax.set_ylim(bottom=y_min, top=y_max)
        
        # Format Y-axis as percentage with 1 decimal place
        self.ax.yaxis.set_major_formatter('{x:.1f}%')
        
        # Title
        self.ax.set_title("SLA", pad=15, color=ThemeLoader.get_color("text", "#333333"))
        
        # Add border around plot area
        for spine in self.ax.spines.values():
            spine.set_visible(True)
            spine.set_color('#cccccc')
            spine.set_linewidth(1)
            
        # Optional: No value labels, no target line, no legend to match exactly
