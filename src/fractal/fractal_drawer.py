"""
fractal_drawer.py
Module for generating fractal patterns.
"""
class FractalTool:
    """
    Tool for drawing fractals interactively.
    """
    def __init__(self, type="koch", color="black", thickness=2):
        self.type = type
        self.color = color
        self.thickness = thickness

    def draw_line(self, start, end):
        """Draws a base line for the fractal."""
        pass  # luego implementamos con la lógica de dibujo

    def generate_fractal(self, points):
        """Generates fractal points based on type and base line."""
        pass

    def draw_fractal(self, canvas):
        """Draws the fractal on the given canvas."""
        pass
