"""
toolbar.py
Creation of Tools buttons modules and catching their events.
"""

import tkinter as tk

CATEGORIES = ["Fractal", "Spiro", "Drawing", "Edit"]

BUTTONS_BY_CATEGORY = {
            "Fractal": ["Line", "Path", "Poligon"],
            "Spiro": ["Circle", "Hypotrochoid", "Epitrochoid"],
            "Drawing": ["Color", "Width", "Type", "Eraser", "Fill"],
            "Edit": ["Clear"]
        }

class Toolbar(tk.Frame):
    """
    Generator of toolbar buttons
    """
    def __init__(self, parent, bg="#252526", fg="white", on_click_callback=None):
        super().__init__(parent, bg=bg)
        self.bg = bg
        self.fg = fg
        self.on_click_callback = on_click_callback
    
    def generate_tools(self):
        self.subframes_dic= {}
        self.buttons_dic = {}
        for subfr in CATEGORIES:
            subframe = tk.Frame(self, bg=self.bg)
            subframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.subframes_dic[subfr] = subframe

            buttons = BUTTONS_BY_CATEGORY[subfr]
            self.buttons_dic[subfr] = []
            for i, name in enumerate(buttons):
                row, col = i // 2, i % 2
                btn = tk.Button(subframe, text=name, bg=self.bg, fg=self.fg,
                        command=lambda n=name: self.on_click_callback(subfr, n))
                btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                self.buttons_dic[subfr].append(btn)

            label_row = (len(buttons)+1)//2
            label = tk.Label(subframe, text=f"{subfr} Tools", bg=self.bg, fg=self.fg)
            label.grid(row=label_row, column=0, columnspan=2)
            self.buttons_dic[subfr].append(label)

    def update_theme(self, colors, index):
        for subfr_name, subframe in self.subframes_dic.items():
            subframe.configure(bg=colors["subframe"][index])
            for widget in subframe.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.configure(bg=colors["buttons_bg"][index], fg=colors["buttons_fg"][index])
                elif isinstance(widget, tk.Label):
                    widget.configure(bg=colors["labels_bg"][index], fg=colors["labels_fg"][index])

    def on_button_click(self, name):
        """Handle button click events."""
        if self.on_click_callback:
            self.on_click_callback(self.category, name)