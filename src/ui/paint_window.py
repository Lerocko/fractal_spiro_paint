"""
paint_window.py
Module for managing the graphical user interface of the Fractal Spiro Paint app.
"""

import tkinter as tk
from tkinter import *
from tkinter import ttk

class PaintWindow:
    """
    Main application window for Fractal Spiro Paint.
    """
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        # Initialize the main application window
        root = tk.Tk()
        root.title("Fractal Spiro Paint")
        root.geometry(f"{self.width}x{self.height}") # Set window size
        root.geometry("+250+60")  # Position the window
        root.configure(bg='grey2')
        root.attributes('-alpha', 0.98)  # Set window transparency

        frame1 = Frame(root, bg='dark slate gray') # Top frame for buttons
        frame1.pack(side=TOP, fill=X) # Fill horizontally at the top of the window
        frame2 = Frame(root, bg='grey2') # Bottom frame for canvas and controls
        frame2.pack(side=TOP, fill=BOTH, expand=True) # Fill remaining space
        canvas = Canvas(frame2, bg='white') # Drawing canvas
        canvas.pack(side=LEFT, fill=BOTH, expand=True) # Fill left side of frame2


        root.mainloop()

    def start(self):
        """Initialize window, buttons, and event loop."""
        self.root.mainloop()

if __name__ == "__main__":
    app = PaintWindow()
    app.start()