from pathlib import Path
from typing import List
import numpy as np

import matplotlib.pyplot as plt

from backend.charts.base_chart import BaseChart
from backend.charts.theme_loader import ThemeLoader
from backend.models.domain import IncidentRecord

class IncidentSummaryChart(BaseChart):
    """Generates a grouped bar chart showing incident types by Location."""
    
    def __init__(self, records: List[IncidentRecord], output_path: Path):
        super().__init__(output_path, width_inches=8.0, height_inches=4.0)
        self.records = records
        
    def validate_data(self) -> None:
        if not self.records:
            # Create a placeholder
            from backend.models.domain import IncidentRecord
            self.records = [IncidentRecord(location="No Data", cable_issue=0, backhaul_impacted=0, electricity_issue=0)]
            
    def render(self) -> None:
        locations = [r.location for r in self.records]
        cable = [r.cable_issue for r in self.records]
        backhaul = [r.backhaul_impacted for r in self.records]
        electricity = [r.electricity_issue for r in self.records]
        
        x = np.arange(len(locations))  # the label locations
        width = 0.25  # the width of the bars
        
        color_cable = ThemeLoader.get_color("primary", "#0047AB")
        color_backhaul = ThemeLoader.get_color("secondary", "#F28C28")
        color_power = ThemeLoader.get_color("accent", "#e74c3c")
        
        bars1 = self.ax.bar(x - width, cable, width, label='Cable', color=color_cable, alpha=0.85)
        bars2 = self.ax.bar(x, backhaul, width, label='Backhaul', color=color_backhaul, alpha=0.85)
        bars3 = self.ax.bar(x + width, electricity, width, label='Electricity', color=color_power, alpha=0.85)
        
        self.ax.set_title("Incident Summary by Location", pad=20, fontsize=14, fontweight="bold", color=ThemeLoader.get_color("text"))
        self.ax.set_ylabel("Incident Count", fontsize=10)
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(locations)
        
        # Max y limit based on data
        max_val = max(max(cable), max(backhaul), max(electricity))
        self.ax.set_ylim(0, max_val + 2)
        
        self.ax.legend(loc="upper right")
        
        plt.setp(self.ax.get_xticklabels(), rotation=45, ha="right")
