"""
paint_window.py
Module for managing the graphical user interface of the Fractal Spiro Paint app.
"""

import tkinter as tk
from tkinter import *
import numpy as np
from src.fractal import fractal_drawer
#from src.spiro import spiro_drawer

# Main application window class
class PaintWindow:
    """
    Main application window for Fractal Spiro Paint.
    """
    def __init__(self, width=800, height=600):
        '''Initialize the main application window and its components.'''
        
        # Set default window dimensions
        self.width = width
        self.height = height

        # Initialize the main application window
        self.root = tk.Tk() # Create the main window
        self.root.title("Fractal Spiro Paint") # Set window title
        self.root.geometry(f"{self.width}x{self.height}") # Set window size
        self.root.geometry("+250+60")  # Position the window
        self.root.configure(bg='#1e1e1e') # Set background color
        self.root.attributes('-alpha', 1)  # Set window transparency

        ''' Initialize drawing tools and state variables'''
        # Initialize drawing tools
        self.active_tool = None  # Currently selected drawing tool
        self.start_point = None  # Starting point for drawing
        self.fractal_tool = fractal_drawer.FractalTool()  # Fractal drawing tool
        #self.spiro_tool = spiro_drawer.SpiroTool()  # Spirograph drawing tool

        '''Create frames and canvas'''
        # Frame file for file operations
        frame_file = Frame(self.root, bg='#2b2b2b', height=40) # Top frame for file operations
        frame_file.pack(side=TOP, fill=X) # Fill horizontally at the top of the window
        frame_file.pack_propagate(False) # Prevent the frame from resizing based on its content

        #  Frame tools for drawing tools
        frame_tools = Frame(self.root, bg='#333333', height=60) # Top frame for buttons
        frame_tools.pack(side=TOP, fill=X) # Fill horizontally at the top of the window
        frame_tools.pack_propagate(False)

        '''Sub-frames for specific tool categories in the tools frame'''
        # Fractal frame
        frame_fractal = Frame(frame_tools, bg='#333333', width=60) # Sub-frame for fractal tools
        frame_fractal.pack(side=LEFT, fill=Y) # Fill vertically on the left side
        frame_fractal.pack_propagate(False)

        # label for fractal tools
        Label(frame_fractal, text="Fractal Tools", bg='#333333', fg='#f1f1f1').pack(pady=5)

        # Spiro frame
        frame_spiro = Frame(frame_tools, bg='#333333', width=60) # Sub-frame for spiro tools
        frame_spiro.pack(side=LEFT, fill=Y) # Fill vertically on the left side
        frame_spiro.pack_propagate(False)

        # label for spiro tools
        Label(frame_spiro, text="Spiro Tools", bg='#333333', fg='#f1f1f1').pack(pady=5)

        # Frame canvas for drawing area
        frame_canvas = Frame(self.root, bg='#252526') # Bottom frame for canvas and controls
        frame_canvas.pack(side=TOP, fill=BOTH, expand=True) # Fill remaining space
        canvas = Canvas(frame_canvas, bg='#f0f0f0', width=700, height=900, highlightthickness=0) # Canvas for drawing
        canvas.pack(pady=20, anchor="center") # Fill the frame for canvas completely
        canvas.bind("<Button-1>", self.on_canvas_click)  # Bind left mouse click to canvas

    
        ''' Create buttons and assign commands'''
        # Create buttons in the file frame as menu options
        btn_file = self.create_buttons_file_frame(frame_file, "File")
        btn_edit = self.create_buttons_file_frame(frame_file, "Edit")
        btn_view = self.create_buttons_file_frame(frame_file, "View")
        btn_save = self.create_buttons_file_frame(frame_file, "Save")
        btn_undo = self.create_buttons_file_frame(frame_file, "Undo")
        btn_redo = self.create_buttons_file_frame(frame_file, "Redo")
        btn_dark_light_mode = self.create_buttons_file_frame(frame_file, "Dark Mode", side=RIGHT)
        
        # Create buttons in the tools frame as drawing tools
        #btn_fractal = self.create_buttons_tools_frame(frame_tools, "Fractal")
        #btn_spiro = self.create_buttons_tools_frame(frame_tools, "Spiro")
        btn_color = self.create_buttons_tools_frame(frame_tools, "Color")
        btn_thickness = self.create_buttons_tools_frame(frame_tools, "Thickness")
        btn_line_style = self.create_buttons_tools_frame(frame_tools, "Line Style")
        btn_eraser = self.create_buttons_tools_frame(frame_tools, "Eraser")
        btn_clear = self.create_buttons_tools_frame(frame_tools, "Clear")

        # Create specific buttons for fractal and spiro tools
        btn_line = self.create_buttons_tool_options_frame(frame_fractal, "Line")
        btn_triangle = self.create_buttons_tool_options_frame(frame_fractal, "Triangle")
        btn_square = self.create_buttons_tool_options_frame(frame_fractal, "Square")


        '''Assign button commands to their respective functions'''
        
        # Assign button commands in the file frame
        
        
        # Assign button commands in the tools frame
        btn_line.config(command=lambda: self.draw_fractal(canvas))
        btn_triangle.config(command=lambda: self.draw_fractal(canvas))
        btn_square.config(command=lambda: self.draw_fractal(canvas))

        btn_clear.config(command=lambda: self.clear_canvas(canvas))
        

    ''' Create helper functions for button creation and actions'''

    def create_buttons_file_frame(self, parent, texts, bg="#2b2b2b", fg="#f1f1f1", padx=5, pady=5, activebackground="#6e6a6a", side=LEFT):
        # Helper function to create buttons in the file frame
        btn = Button(parent, text=texts, bg=bg, fg=fg, relief=FLAT, bd=0, padx=padx, pady=pady, activebackground=activebackground)
        btn.pack(side=side) # Pack the button to the specified side of the frame
        return btn
    
    def create_buttons_tools_frame(self, parent, texts, bg="#333333", fg="#f1f1f1", padx=5, pady=10, activebackground="#6e6a6a", side=LEFT):
        # Helper function to create buttons in the tools frame
        btn = Button(parent, text=texts, bg=bg, fg=fg, relief=FLAT, bd=0, padx=padx, pady=pady, activebackground=activebackground)
        btn.pack(side=side) # Pack the button to the specified side of the frame
        return btn
    
    def create_buttons_tool_options_frame(self, parent, texts, bg="#444444", fg="#f1f1f1", padx=5, pady=5, activebackground="#6e6a6a", side=TOP):
        # Helper function to create buttons in the tool options frame
        btn = Button(parent, text=texts, bg=bg, fg=fg, relief=FLAT, bd=0, padx=padx, pady=pady, activebackground=activebackground)
        btn.pack(side=side) # Pack the button to the specified side of the frame
        return btn
    
    ''' Define drawing functions for the canvas'''

    # Function to draw a fractal pattern    
    def draw_fractal(self, canvas):
        """Draw a fractal pattern on the canvas."""
        canvas.delete("all")
        canvas.create_text(200, 200, text="Fractal!", fill="blue", font=("Arial", 24))

    # Function to draw a spirograph pattern
    def draw_spiro(self, canvas):
        """Draw a spirograph pattern on the canvas."""
        canvas.delete("all")
        canvas.create_text(200, 200, text="Spiro!", fill="red", font=("Arial", 24))

    # Function to clear the canvas  
    def clear_canvas(self, canvas):
        """Clear the drawing canvas."""
        canvas.delete("all")  # Remove all items from the canvas

    # Function to set the active drawing tool
    def set_active_tool(self, tool_name):
        '''Set the currently active drawing tool'''
        self.active_tool = tool_name
        self.start_point = None  # Reset start point when tool changes

    def on_canvas_click(self, event):
        """Handle canvas click events."""
        if self.active_tool == "Line":
            if self.start_point is None:
                self.start_point = (event.x, event.y)
            else:
                end_point = (event.x, event.y)
                # Draw line using the fractal tool
                self.fractal_tool.draw_fractal(canvas, np.array(self.start_point), np.array(end_point))
                self.start_point = None  # Reset start point after drawing

    '''Method to start the main event loop'''

    def start(self):
        """Initialize window, buttons, and event loop."""
        self.root.mainloop()



if __name__ == "__main__":
    app = PaintWindow()
    app.start()