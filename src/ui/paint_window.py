"""
paint_window.py
Module for managing the graphical user interface of the Fractal Spiro Paint app.
"""

import tkinter as tk
from tkinter import *
from src.fractal import fractal_drawer
from src.spiro import spiro_drawer
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

        '''Create frames and canvas'''
        # Frame file for file operations
        frame_file = Frame(self.root, bg='#2b2b2b', height=40) # Top frame for file operations
        frame_file.pack(side=TOP, fill=X) # Fill horizontally at the top of the window
        frame_file.pack_propagate(False) # Prevent the frame from resizing based on its content

        #  Frame tools for drawing tools
        frame_tools = Frame(self.root, bg='#333333', height=60) # Top frame for buttons
        frame_tools.pack(side=TOP, fill=X) # Fill horizontally at the top of the window
        frame_tools.pack_propagate(False)

        # Frame canvas for drawing area
        frame_canvas = Frame(self.root, bg='#252526') # Bottom frame for canvas and controls
        frame_canvas.pack(side=TOP, fill=BOTH, expand=True) # Fill remaining space
        canvas = Canvas(frame_canvas, bg='#f0f0f0', width=700, height=900, highlightthickness=0) # Canvas for drawing
        canvas.pack(pady=20, anchor="center") # Fill the frame for canvas completely

    
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
        btn_fractal = self.create_buttons_tools_frame(frame_tools, "Fractal")
        btn_spiro = self.create_buttons_tools_frame(frame_tools, "Spiro")
        btn_color = self.create_buttons_tools_frame(frame_tools, "Color")
        btn_thickness = self.create_buttons_tools_frame(frame_tools, "Thickness")
        btn_line_style = self.create_buttons_tools_frame(frame_tools, "Line Style")
        btn_eraser = self.create_buttons_tools_frame(frame_tools, "Eraser")
        btn_clear = self.create_buttons_tools_frame(frame_tools, "Clear")

        
        '''Assign button commands to their respective functions'''
        
        # Assign button commands in the file frame
        
        
        # Assign button commands in the tools frame
        btn_fractal.config(command=lambda: self.draw_fractal(canvas))
        btn_spiro.config(command=lambda: self.draw_spiro(canvas))
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


    '''Method to start the main event loop'''

    def start(self):
        """Initialize window, buttons, and event loop."""
        self.root.mainloop()



if __name__ == "__main__":
    app = PaintWindow()
    app.start()