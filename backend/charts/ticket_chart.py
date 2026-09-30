from pathlib import Path
from typing import List
from datetime import datetime
import numpy as np

from backend.charts.base_chart import BaseChart
from backend.charts.theme_loader import ThemeLoader
from backend.models.domain import SLARecord
from backend.utils.exceptions import ChartGenerationError

class TicketTrendChart(BaseChart):
    """Generates the Ticket Request Trend Chart."""
    
    def __init__(self, data: List[SLARecord], output_path: Path):
        super().__init__(output_path, width_inches=6.0, height_inches=4.0)
        self.data = data
        
    def validate_data(self) -> None:
        """Validates ticket data constraints."""
        if not self.data:
            raise ChartGenerationError("Empty data provided for Ticket chart.")
        if any(r.ticket_count < 0 for r in self.data):
            raise ChartGenerationError("Negative ticket count")
            
    def render(self) -> None:
        """Renders the ticket bars and trend line matching the original PPT exactly."""
        # Convert YYYY-MM to short month name (e.g. 'Apr', 'May')
        months = []
        for r in self.data:
            try:
                months.append(datetime.strptime(r.month, "%Y-%m").strftime("%b"))
            except ValueError:
                months.append(r.month)
                
        tickets = [record.ticket_count for record in self.data]
        
        # Standard PPT Blue
        ppt_blue = "#5B9BD5"
        
        # Bars (thinner width like original)
        bars = self.ax.bar(months, tickets, color=ppt_blue, width=0.3)
        
        # Auto-scale Y axis dynamically but keep bounds tight like original
        min_tickets = min(tickets) if tickets else 0
        max_tickets = max(tickets) if tickets else 10
        self.ax.set_ylim(bottom=max(0, min_tickets - 2), top=max_tickets + 1)
        
        # Trend Line (dotted blue)
        # Using numpy polyfit to draw a straight trendline
        x = np.arange(len(months))
        if len(x) > 1:
            z = np.polyfit(x, tickets, 1)
            p = np.poly1d(z)
            self.ax.plot(x, p(x), color=ppt_blue, linestyle=':', linewidth=1.5)
        
        # Title
        self.ax.set_title("Service Requests", pad=15, color=ThemeLoader.get_color("text", "#333333"))
        
        # Add border around plot area
        for spine in self.ax.spines.values():
            spine.set_visible(True)
            spine.set_color('#cccccc')
            spine.set_linewidth(1)
            
        # No value labels or legends needed
