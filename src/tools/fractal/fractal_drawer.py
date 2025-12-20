"""
fractal_drawer.py
Module for generating fractal patterns.
"""

import numpy as np
from tkinter import Canvas
from src.core.theme_manager import get_color

class FractalTool:
    """Generates and draws fractals from a base shape and a user-defined pattern."""

    def __init__(self, canvas: Canvas, color="black", thickness=2):
        self.canvas = canvas
        self.color = get_color("drawing_default")
        self.thickness = thickness

    def apply_pattern(self, base_points, pattern_points):
        """
        Applies a fractal pattern to a base shape.
        - base_points: Points from the selected shape in main canvas.
        - pattern_points: Points from the pattern drawn in secondary canvas.
        """
        if len(pattern_points) < 2:
            return
        
        flat_pattern = [coord for point in pattern_points for coord in point]
        self.canvas.create_line(flat_pattern, fill=self.color, width=self.thickness)

