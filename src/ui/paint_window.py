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
        # Set default window dimensions
        self.width = width
        self.height = height

        # Initialize the main application window
        self.root = tk.Tk() # Create the main window
        self.root.title("Fractal Spiro Paint")
        self.root.geometry(f"{self.width}x{self.height}") # Set window size
        self.root.geometry("+250+60")  # Position the window
        self.root.configure(bg='#1e1e1e') # Set background color
        self.root.attributes('-alpha', 1)  # Set window transparency

        # Create frames and canvas
        frame_file = Frame(self.root, bg='#2b2b2b', height=40) # Top frame for file operations
        frame_file.pack(side=TOP, fill=X) # Fill horizontally at the top of the window
        frame_tools = Frame(self.root, bg='#333333', height=60) # Top frame for buttons
        frame_tools.pack(side=TOP, fill=X) # Fill horizontally at the top of the window
        frame_canvas = Frame(self.root, bg='#252526') # Bottom frame for canvas and controls
        frame_canvas.pack(side=TOP, fill=BOTH, expand=True) # Fill remaining space
        canvas = Canvas(frame_canvas, bg='#f0f0f0', width=700, height=900, highlightthickness=0) # Canvas for drawing
        canvas.pack(pady=20, anchor="center") # Fill the frame for canvas completely



    def start(self):
        """Initialize window, buttons, and event loop."""
        self.root.mainloop()

if __name__ == "__main__":
    app = PaintWindow()
    app.start()