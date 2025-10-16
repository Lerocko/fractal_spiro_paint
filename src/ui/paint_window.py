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
        frame_file.pack_propagate(False) # Prevent the frame from resizing based on its content
        frame_tools = Frame(self.root, bg='#333333', height=60) # Top frame for buttons
        frame_tools.pack(side=TOP, fill=X) # Fill horizontally at the top of the window
        frame_tools.pack_propagate(False)
        frame_canvas = Frame(self.root, bg='#252526') # Bottom frame for canvas and controls
        frame_canvas.pack(side=TOP, fill=BOTH, expand=True) # Fill remaining space
        canvas = Canvas(frame_canvas, bg='#f0f0f0', width=700, height=900, highlightthickness=0) # Canvas for drawing
        canvas.pack(pady=20, anchor="center") # Fill the frame for canvas completely

        # Add buttons to the file frame with padding and styling
        btn_file = Button(frame_file, text="File", bg= "#2b2b2b", fg="#f1f1f1", relief=FLAT, bd=0, padx=5, pady=5, activebackground="#6e6a6a")
        btn_file.pack(side=LEFT) # Pack the button to the left side of the frame
        btn_file.pack_propagate(False) # Prevent the button from resizing based on its content
        btn_edit = Button(frame_file, text="Edit", bg= "#2b2b2b", fg="#f1f1f1", relief=FLAT, bd=0, padx=5, pady=5, activebackground="#6e6a6a")
        btn_edit.pack(side=LEFT) # Pack the button to the left side of the frame
        btn_edit.pack_propagate(False) # Prevent the button from resizing based on its content
        btn_view = Button(frame_file, text="View", bg= "#2b2b2b", fg="#f1f1f1", relief=FLAT, bd=0, padx=5, pady=5, activebackground="#6e6a6a")
        btn_view.pack(side=LEFT) # Pack the button to the left side of the frame
        btn_view.pack_propagate(False) # Prevent the button from resizing based on its content
        btn_save = Button(frame_file, text="Save", bg= "#2b2b2b", fg="#f1f1f1", relief=FLAT, bd=0, padx=5, pady=5, activebackground="#6e6a6a")
        btn_save.pack(side=LEFT) # Pack the button to the right side of the frame
        btn_save.pack_propagate(False) # Prevent the button from resizing based on its content
        btn_undo = Button(frame_file, text="Undo", bg= "#2b2b2b", fg="#f1f1f1", relief=FLAT, bd=0, padx=5, pady=5, activebackground="#6e6a6a")
        btn_undo.pack(side=LEFT) # Pack the button to the left side of the frame
        btn_undo.pack_propagate(False) # Prevent the button from resizing based on its content
        btn_redo = Button(frame_file, text="Redo", bg= "#2b2b2b", fg="#f1f1f1", relief=FLAT, bd=0, padx=5, pady=5, activebackground="#6e6a6a")
        btn_redo.pack(side=LEFT) # Pack the button to the left side of the frame
        btn_redo.pack_propagate(False) # Prevent the button from resizing based on its content
        btn_dark_light_mode = Button(frame_file, text="Dark Mode", bg= "#2b2b2b", fg="#f1f1f1", relief=FLAT, bd=0, padx=5, pady=5, activebackground="#6e6a6a")
        btn_dark_light_mode.pack(side=RIGHT) # Pack the button to the right side of the frame
        btn_dark_light_mode.pack_propagate(False) # Prevent the button from resizing based on its content

        # Add buttons to the tools frame with padding and styling
        btn_fractal = Button(frame_tools, text="Fractal", bg= "#333333", fg="#f1f1f1", relief=FLAT, bd=0, padx=5, pady=10, activebackground="#6e6a6a")
        btn_fractal.pack(side=LEFT) # Pack the button to the left side of the frame
        btn_fractal.pack_propagate(False) # Prevent the button from resizing based on its content
        btn_spiro = Button(frame_tools, text="Spiro", bg= "#333333", fg="#f1f1f1", relief=FLAT, bd=0, padx=5, pady=10, activebackground="#6e6a6a")
        btn_spiro.pack(side=LEFT) # Pack the button to the left side of the frame
        btn_spiro.pack_propagate(False) # Prevent the button from resizing based on its content
        btn_color = Button(frame_tools, text="Color", bg= "#333333", fg="#f1f1f1", relief=FLAT, bd=0, padx=5, pady=10, activebackground="#6e6a6a")
        btn_color.pack(side=LEFT) # Pack the button to the left side of the frame
        btn_color.pack_propagate(False) # Prevent the button from resizing based on its content
        btn_thickness = Button(frame_tools, text="Thickness", bg= "#333333", fg="#f1f1f1", relief=FLAT, bd=0, padx=5, pady=10, activebackground="#6e6a6a")
        btn_thickness.pack(side=LEFT) # Pack the button to the left side of the frame
        btn_thickness.pack_propagate(False) # Prevent the button from resizing based on its content
        btn_line_style = Button(frame_tools, text="Line Style", bg= "#333333", fg="#f1f1f1", relief=FLAT, bd=0, padx=5, pady=10, activebackground="#6e6a6a")
        btn_line_style.pack(side=LEFT) # Pack the button to the left side of the frame
        btn_line_style.pack_propagate(False) # Prevent the button from resizing based on its content
        btn_eraser = Button(frame_tools, text="Eraser", bg= "#333333", fg="#f1f1f1", relief=FLAT, bd=0, padx=5, pady=10, activebackground="#6e6a6a")
        btn_eraser.pack(side=LEFT) # Pack the button to the left side of the frame
        btn_eraser.pack_propagate(False) # Prevent the button from resizing based on its content
        btn_clear = Button(frame_tools, text="Clear", bg= "#333333", fg="#f1f1f1", relief=FLAT, bd=0, padx=5, pady=10, activebackground="#6e6a6a")
        btn_clear.pack(side=LEFT) # Pack the button to the left side of the frame
        btn_clear.pack_propagate(False) # Prevent the button from resizing based on its content

        


    def start(self):
        """Initialize window, buttons, and event loop."""
        self.root.mainloop()

if __name__ == "__main__":
    app = PaintWindow()
    app.start()