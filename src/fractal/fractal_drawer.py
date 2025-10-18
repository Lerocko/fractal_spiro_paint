"""
fractal_drawer.py
Module for generating fractal patterns.
"""

from tkinter import Canvas
import numpy as np

class FractalTool:
    """
    Tool for drawing fractals interactively.
    """
    def __init__(self, type="koch", color="black", thickness=2):
        self.type = type
        self.color = color
        self.thickness = thickness

    def draw_line(self, canvas, A, B):
        """Draws a base line on the canvas."""
        canvas.create_line(A[0], A[1], B[0], B[1], fill=self.color, width=self.thickness)

    def generate_fractal(self, canvas, A, B):
        """Generates fractal points based on type and base line."""
        #Calculate distance and normal vector
        d = np.linalg.norm(B - A)
        r = d / 3.0
        n = -np.array([(A[1] - B[1]) / d, (B[0] - A[0]) / d])  # Normal vector
        h = r * np.sqrt(3) / 2.0  # Height of the equilateral triangle

        # Calculate points
        p1 = (2 * A + B) / 3.0
        p3 = (A + 2 * B) / 3.0
        C = (A + B) / 2.0
        p2 = C + h * n

        # Recursive case
        if d > 10:
            # flake #1
            self.generate_fractal(canvas, A, p1)
            # flake #2
            self.generate_fractal(canvas, p1, p2)
            # flake #3
            self.generate_fractal(canvas, p2, p3)
            # flake #4
            self.generate_fractal(canvas, p3, B)
        # Base case
        else:
            # Unpack points for easier access
            xA, yA = A
            xB, yB = B
            xp1, yp1 = p1
            xp2, yp2 = p2
            xp3, yp3 = p3

            # Draw minimal line segment
            canvas.create_line(xA, yA, xp1, yp1, fill=self.color, width=self.thickness)
            canvas.create_line(xp1, yp1, xp2, yp2, fill=self.color, width=self.thickness)
            canvas.create_line(xp2, yp2, xp3, yp3, fill=self.color, width=self.thickness)
            canvas.create_line(xp3, yp3, xB, yB, fill=self.color, width=self.thickness)
            
            

    def draw_fractal(self, canvas, A, B):
        """Draws the fractal on the given canvas."""
        if self.type == "koch":
            self.generate_fractal(canvas, A, B)
        else:
            self.draw_line(canvas, A, B)    
        pass
