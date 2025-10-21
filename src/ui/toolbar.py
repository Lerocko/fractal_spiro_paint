"""
toolbar.py
Creation of Tools buttons modules and catching their events.
"""

import tkinter as tk

class Toolbar_button(tk.Frame):
    """
    Generator of toolbar buttons
    """
    def __init__(self, parent, text, width, height, bg_color, fg_color, command=None):
        super().__init__(parent)
        self.text = text
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.command = command

    


    def generate_buttons(self, parent, buttons, bg, fg):
        """Generate toolbar buttons dynamically, given a list of button names."""
        for btn_name in buttons:
            button = tk.Button(
                parent,
                text=btn_name,
                width=10,
                height=2,
                bg=bg,
                fg=fg,
                command=lambda name=btn_name: self.on_button_click(name)   
            )
            button.pack(side=tk.LEFT, padx=5, pady=5)

    
        




        


