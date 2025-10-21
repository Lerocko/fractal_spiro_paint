"""
toolbar.py
Creation of Tools buttons modules and catching their events.
"""

import tkinter as tk

class Toolbar(tk.Frame):
    """
    Generator of toolbar buttons
    """
    def __init__(self, parent, category, bg="#252526", fg="white"):
        super().__init__(parent, bg=bg)
        self.parent = parent
        self.category = category
        self.bg = bg
        self.fg = fg
        self.current_tool = None
        self.current_category = None
                
        self.buttons_by_category = {
            "Fractal": ["Line", "Path", "Poligon"],
            "Spiro": ["Circle", "Hypotrochoid", "Epitrochoid"],
            "Drawing": ["Color", "Width", "Type", "Eraser", "Fill"],
            "Edit": ["Clear"]
        }
        self.generate_buttons()

    def generate_buttons(self):
        """Generate toolbar buttons dynamically, given a list of button names."""
        for name in self.buttons_by_category.get(self.category, []):
            button = tk.Button(
                self,
                text=name,
                bg=self.bg,
                fg=self.fg,
                width=10,
                height=2,
                command=lambda n=name: self.on_button_click(n)   
            )
            button.pack(side=tk.LEFT, padx=5, pady=5)

    def on_button_click(self, name):
        """Handle button click events."""
        
        self.current_category = self.category
        self.current_tool = name

    
        




        


