"""
spiro_drawer.py
Module for generating spirograph patterns.
"""
class SpiroTool:
    """
    Tool for drawing spirographs interactively.
    """
    def __init__(self, R=100, r=50, d=50, color="black", thickness=2):
        self.R = R
        self.r = r
        self.d = d
        self.color = color
        self.thickness = thickness

    def draw_base_circle(self, canvas):
        """Draws the fixed transparent circle."""
        pass

    def draw_moving_circle(self, canvas):
        """Draws the inner circle that rotates."""
        pass

    def draw_spiro(self, canvas):
        """Draws the spirograph line."""
        pass
