"""
toolbar.py
Creation of Tools buttons modules and catching their events.
"""

import tkinter as tk

class Toolbar(tk.Frame):
    """
    Generator of toolbar buttons
    """
    def __init__(self, parent, category, bg="#252526", fg="white", on_click_callback=None):
        super().__init__(parent, bg=bg)
        #self.parent = parent
        self.category = category
        self.bg = bg
        self.fg = fg
        #self.current_tool = None
        #self.current_category = None
        self.on_click_callback = on_click_callback

        self.subframe = tk.Frame(self, bg=self.bg)
        self.subframe.pack()
        self.subframe.pack_propagate(False)

        self.button_frames = tk.Frame(self.subframe, bg=self.bg)
        self.button_frames.pack()
        self.button_frames.pack_propagate(False)

        self.label_subframe = tk.Label(self.subframe, bg=self.bg, fg=self.fg, text=f"{self.category} Tools")
        self.label_subframe.pack(side=tk.BOTTOM)
        
                
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
                self.button_frames,
                text=name,
                bg=self.bg,
                fg=self.fg,
                width=10,
                height=2,
                command=lambda n=name: self.on_click_callback(self.category, n)   
            )
            button.pack(side=tk.LEFT, padx=5, pady=5)

    def update_theme(self, colors, index):
        self.subframe.configure(bg=colors["subframe"][index])
        self.button_frames.configure(bg=colors["buttonsframe"][index])
        self.label_subframe.configure(bg=colors["labels_bg"][index])
        for btn in self.button_frames.winfo_children():
            btn.configure(bg=colors["buttons_bg"][index], fg=colors["buttons_fg"][index])

    def on_button_click(self, name):
        """Handle button click events."""
        if self.on_click_callback:
            self.on_click_callback(self.category, name)

    
        




        


