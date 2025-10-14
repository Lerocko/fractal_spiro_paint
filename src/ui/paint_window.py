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
        root.mainloop()

    def start(self):
        """Initialize window, buttons, and event loop."""
        self.root.mainloop()
