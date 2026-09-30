from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from backend.charts.base_chart import BaseChart
from backend.charts.theme_loader import ThemeLoader

class ServiceRequestChart(BaseChart):
    """Generates a Flowchart/Tree diagram showing Service Requests breakdown."""
    
    def __init__(self, flowchart_data: Dict[str, str], output_path: Path):
        # Match dimensions to make it fit nicely (13.9 x 9.25 inches)
        super().__init__(output_path, width_inches=13.9, height_inches=9.25)
        self.flowchart_data = flowchart_data
        
    def validate_data(self) -> None:
        pass
            
    def _draw_box(self, ax, text, x, y, width=2.4, height=0.7, color="#5B9BD5"):
        # Draw rounded rectangle
        box = patches.FancyBboxPatch(
            (x - width/2, y - height/2), 
            width, height,
            boxstyle="round,pad=0.05",
            edgecolor="none",
            facecolor=color,
            alpha=1.0
        )
        ax.add_patch(box)
        # Add text
        ax.text(x, y, text, ha='center', va='center', color='white', fontsize=12, fontweight='normal', wrap=True)
        return (x - width/2, x + width/2, y - height/2, y + height/2)
        
    def _draw_line(self, ax, x1, y1, x2, y2):
        # Draw a line connecting boxes (Orthogonal/Manhattan routing)
        mid_x = (x1 + x2) / 2
        ax.plot([x1, mid_x, mid_x, x2], [y1, y1, y2, y2], color="#5B9BD5", linewidth=1.5)

    def render(self) -> None:
        # Extract data
        total = self.flowchart_data.get("{{total_requests_count}}", "0")
        
        reqs = self.flowchart_data.get("{{requests_count}}", "0")
        comps = self.flowchart_data.get("{{complaints_count}}", "0")
        proac = self.flowchart_data.get("{{proactive_count}}", "0")
        reac = self.flowchart_data.get("{{reactive_count}}", "0")
        ishan = self.flowchart_data.get("{{ishan_issue_count}}", "0")
        cust = self.flowchart_data.get("{{customer_issue_count}}", "0")
        ishan_rfos = [self.flowchart_data.get(f"{{{{ishan_rfo_{i+1}}}}}") for i in range(4)]
        ishan_rfos = [r for r in ishan_rfos if r]
        cust_rfos = [self.flowchart_data.get(f"{{{{customer_rfo_{i+1}}}}}") for i in range(2)]
        cust_rfos = [r for r in cust_rfos if r]
        
        # Disable axes
        self.ax.axis('off')
        
        # Grid parameters
        # We will use 5 columns (levels) of boxes
        # X coordinates for levels
        L1, L2, L3, L4, L5 = 1.5, 4.5, 7.5, 10.5, 13.5
        box_w = 2.4
        
        # Draw boxes and connect
        # 1. Total Requests
        self._draw_box(self.ax, f"Total Service\nRequests-{total}", L1, 5)
        
        # 2. Requests and Complaints
        self._draw_box(self.ax, f"Requests\n{reqs}", L2, 6.5)
        self._draw_box(self.ax, f"Complaints {comps}", L2, 3.5)
        self._draw_line(self.ax, L1+box_w/2, 5, L2-box_w/2, 6.5)
        self._draw_line(self.ax, L1+box_w/2, 5, L2-box_w/2, 3.5)
        
        # 3. Proactive / Reactive (from Complaints)
        self._draw_box(self.ax, f"Proactive-{proac}", L3, 5)
        self._draw_box(self.ax, f"Reactive-{reac}", L3, 2)
        self._draw_line(self.ax, L2+box_w/2, 3.5, L3-box_w/2, 5)
        self._draw_line(self.ax, L2+box_w/2, 3.5, L3-box_w/2, 2)
        
        # 4. Ishan / Customer end (from Reactive)
        self._draw_box(self.ax, f"Issue at Ishan\nend-{ishan}", L4, 3.5)
        self._draw_box(self.ax, f"Issue at\nCustomer end-{cust}", L4, 0.5)
        self._draw_line(self.ax, L3+box_w/2, 2, L4-box_w/2, 3.5)
        self._draw_line(self.ax, L3+box_w/2, 2, L4-box_w/2, 0.5)
        
        # 5. RFOs
        # Ishan RFOs
        if ishan_rfos:
            start_y = 3.5 + (len(ishan_rfos)-1)/2
            for i, rfo in enumerate(ishan_rfos):
                y = start_y - i
                self._draw_box(self.ax, rfo, L5, y)
                self._draw_line(self.ax, L4+box_w/2, 3.5, L5-box_w/2, y)
                
        # Customer RFOs
        if cust_rfos:
            start_y = 0.5 + (len(cust_rfos)-1)/2
            for i, rfo in enumerate(cust_rfos):
                y = start_y - i
                self._draw_box(self.ax, rfo, L5, y)
                self._draw_line(self.ax, L4+box_w/2, 0.5, L5-box_w/2, y)
                
        # Set bounds for 15 wide grid
        self.ax.set_xlim(0, 15)
        self.ax.set_ylim(-1, 8)
