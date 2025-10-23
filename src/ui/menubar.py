"""
menubar.py
Creation of File buttons modules and catching their events.
"""
import tkinter as tk

class Menubar(tk.Frame):
    """
    Generator of file menu buttons
    """
    def __init__(self, parent, bg="#252526", fg="white", on_click_callback=None):
        super().__init__(parent, bg=bg)
        #self.parent = parent
        self.bg = bg
        self.fg = fg
        self.on_click_callback = on_click_callback
        #self.current_file_action = None
                
        self.file_buttons = ["New", "Open", "Save", "Save As", "Export", "Exit", "Dark/Light"]
        self.generate_file_buttons()

    def generate_file_buttons(self):
        """Generate file menu buttons dynamically."""
        for name in self.file_buttons:
            side = tk.RIGHT if name == "Dark/Light" else tk.LEFT
            button = tk.Button(
                self,
                text=name,
                bg=self.bg,
                fg=self.fg,
                width=10,
                height=2,
                command=lambda n=name: self.on_file_button_click(n)   
            )
            button.pack(side=side, padx=5, pady=5)
            

    def on_file_button_click(self, name):
        """Handle file button click events."""
        if self.on_click_callback:
            self.on_click_callback(name)