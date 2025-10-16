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

        # Add buttons to the file frame with padding and styling
        btn_file = Button(frame_file, text="File", bg= "#3c3c3c", fg="#f1f1f1", relief=RAISED, bd=0, padx=10, pady=5)
        btn_file.pack(side=LEFT, padx=10, pady=5) # Pack the button to the left side of the frame
        btn_edit = Button(frame_file, text="Edit", bg= "#3c3c3c", fg="#f1f1f1", relief=RAISED, bd=0, padx=10, pady=5)
        btn_edit.pack(side=LEFT, padx=10, pady=5) # Pack the button to the left side of the frame
        btn_view = Button(frame_file, text="View", bg= "#3c3c3c", fg="#f1f1f1", relief=RAISED, bd=0, padx=10, pady=5)
        btn_view.pack(side=LEFT, padx=10, pady=5) # Pack the button to the left side of the frame
        btn_save = Button(frame_file, text="Save", bg= "#3c3c3c", fg="#f1f1f1", relief=RAISED, bd=0, padx=10, pady=5)
        btn_save.pack(side=LEFT, padx=10, pady=5) # Pack the button to the right side of the frame
        btn_undo = Button(frame_file, text="Undo", bg= "#4b4b4b", fg="#f1f1f1", relief=RAISED, bd=0, padx=10, pady=5)
        btn_undo.pack(side=LEFT, padx=10, pady=10) # Pack the button to the left side of the frame
        btn_redo = Button(frame_file, text="Redo", bg= "#4b4b4b", fg="#f1f1f1", relief=RAISED, bd=0, padx=10, pady=5)
        btn_redo.pack(side=LEFT, padx=10, pady=10) # Pack the button to the left side of the frame

        # Add buttons to the tools frame with padding and styling
        btn_fractal = Button(frame_tools, text="Fractal", bg= "#3c3c3c", fg="#f1f1f1", relief=RAISED, bd=0, padx=10, pady=5)
        btn_fractal.pack(side=LEFT, padx=10, pady=10) # Pack the button to the left side of the frame
        btn_spiro = Button(frame_tools, text="Spiro", bg= "#3c3c3c", fg="#f1f1f1", relief=RAISED, bd=0, padx=10, pady=5)
        btn_spiro.pack(side=LEFT, padx=10, pady=10) # Pack the button to the left side of the frame
        btn_color = Button(frame_tools, text="Color", bg= "#3c3c3c", fg="#f1f1f1", relief=RAISED, bd=0, padx=10, pady=5)
        btn_color.pack(side=LEFT, padx=10, pady=10) # Pack the button to the left side of the frame
        btn_thickness = Button(frame_tools, text="Thickness", bg= "#3c3c3c", fg="#f1f1f1", relief=RAISED, bd=0, padx=10, pady=5)
        btn_thickness.pack(side=LEFT, padx=10, pady=10) # Pack the button to the left side of the frame
        btn_line_style = Button(frame_tools, text="Line Style", bg= "#3c3c3c", fg="#f1f1f1", relief=RAISED, bd=0, padx=10, pady=5)
        btn_line_style.pack(side=LEFT, padx=10, pady=10) # Pack the button to the left side of the frame
        btn_clear = Button(frame_tools, text="Clear", bg= "#e81123", fg="#f1f1f1", relief=RAISED, bd=0, padx=10, pady=5)
        btn_clear.pack(side=LEFT, padx=10, pady=10) # Pack the button to the left side of the frame


    def start(self):
        """Initialize window, buttons, and event loop."""
        self.root.mainloop()

if __name__ == "__main__":
    app = PaintWindow()
    app.start()