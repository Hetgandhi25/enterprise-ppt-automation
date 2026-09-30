import logging
import time
from abc import ABC, abstractmethod
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib

from backend.charts.theme_loader import ThemeLoader
from backend.charts.chart_utils import ensure_directory
from backend.utils.exceptions import ChartGenerationError

# Use non-interactive backend for headless generation
matplotlib.use('Agg')

logger = logging.getLogger(__name__)

class BaseChart(ABC):
    """Abstract base class for all chart generators."""
    
    def __init__(self, output_path: Path, width_inches: float = 8.0, height_inches: float = 4.0):
        self.output_path = output_path
        self.width_inches = width_inches
        self.height_inches = height_inches
        self.theme = ThemeLoader.get_theme()
        self.fig, self.ax = plt.subplots(figsize=(self.width_inches, self.height_inches))
        
    def _apply_theme(self) -> None:
        """Applies consistent branding to the chart axes."""
        # Grid
        self.ax.yaxis.grid(True, linestyle='--', color=ThemeLoader.get_color("grid", "#e0e0e0"), alpha=0.7)
        self.ax.set_axisbelow(True)
        
        # Spines
        for spine in ["top", "right"]:
            self.ax.spines[spine].set_visible(False)
        for spine in ["bottom", "left"]:
            self.ax.spines[spine].set_color(ThemeLoader.get_color("text", "#333333"))
            
        # Ticks & Labels
        self.ax.tick_params(colors=ThemeLoader.get_color("text", "#333333"))
        
        # Font family
        plt.rcParams['font.family'] = ThemeLoader.get_font("main", "Arial")
        
    @abstractmethod
    def validate_data(self) -> None:
        """Validates the input data before rendering."""
        pass

    @abstractmethod
    def render(self) -> None:
        """Core rendering logic to be implemented by subclasses."""
        pass

    def generate(self) -> Path:
        """Executes the complete generation lifecycle."""
        start_time = time.time()
        logger.info(f"[{self.__class__.__name__}] Starting chart generation.")
        
        try:
            self.validate_data()
            logger.info(f"[{self.__class__.__name__}] Data validated successfully.")
            
            self._apply_theme()
            self.render()
            logger.info(f"[{self.__class__.__name__}] Chart rendered successfully.")
            
            ensure_directory(self.output_path)
            
            # Save the figure
            self.fig.tight_layout()
            is_transparent = ThemeLoader.get_color("background", "transparent") == "transparent"
            
            self.fig.savefig(
                self.output_path, 
                dpi=300, 
                transparent=is_transparent,
                bbox_inches='tight'
            )
            plt.close(self.fig)
            
            execution_time = (time.time() - start_time) * 1000
            logger.info(f"[{self.__class__.__name__}] PNG saved to {self.output_path}. Exec time: {execution_time:.2f}ms.")
            
            return self.output_path
            
        except Exception as e:
            plt.close(self.fig)
            logger.error(f"[{self.__class__.__name__}] Failed to generate chart: {e}")
            raise ChartGenerationError(f"Failed to generate chart: {e}")
