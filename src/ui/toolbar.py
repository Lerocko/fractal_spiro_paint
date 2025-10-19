"""
toolbar.py
Toolbar module for Fractal Spiro Paint.
Creates collapsible tool sections (Fractal, Spiro, Edit).
"""

import tkinter as tk
from tkinter import Frame, Button, Label

class CollapsibleSection(Frame):
    """
    A collapsible section containing a label and optional buttons.
    Clicking the header toggles the visibility of the inner content.
    """

    def __init__(self, parent, title, buttons, command_map=None, bg="#333333", fg="#f1f1f1"):
        super().__init__(parent, bg=bg)
        self.parent = parent
        self.title = title
        self.buttons = buttons
        self.command_map = command_map or {}

        # Track expanded/collapsed state
        self.expanded = True

        # Header frame with title and toggle arrow
        self.header_frame = Frame(self, bg=bg)
        self.header_frame.pack(fill=tk.X)

        self.arrow = Label(self.header_frame, text="▼", bg=bg, fg=fg, font=("Arial", 10))
        self.arrow.pack(side=tk.LEFT, padx=5)

        self.title_label = Label(self.header_frame, text=title, bg=bg, fg=fg, font=("Arial", 11, "bold"))
        self.title_label.pack(side=tk.LEFT, pady=5)

        # Bind click events to toggle section
        self.header_frame.bind("<Button-1>", self.toggle)
        self.title_label.bind("<Button-1>", self.toggle)
        self.arrow.bind("<Button-1>", self.toggle)

        # Frame for the collapsible content
        self.content_frame = Frame(self, bg=bg)
        self.content_frame.pack(fill=tk.X)

        # Create buttons inside the content frame
        self.create_buttons(self.content_frame)

    def create_buttons(self, parent):
        """Generate buttons dynamically based on the provided list."""
        for name in self.buttons:
            btn = Button(
                parent,
                text=name,
                bg="#3a3a3a",
                fg="#f1f1f1",
                relief=tk.FLAT,
                bd=0,
                padx=5,
                pady=5,
                activebackground="#6e6a6a",
            )
            if name in self.command_map:
                btn.config(command=self.command_map[name])
            btn.pack(fill=tk.X, padx=10, pady=2)

    def toggle(self, event=None):
        """Expand or collapse the section."""
        if self.expanded:
            self.content_frame.forget()
            self.arrow.config(text="►")
        else:
            self.content_frame.pack(fill=tk.X)
            self.arrow.config(text="▼")
        self.expanded = not self.expanded


class Toolbar(Frame):
    """
    Toolbar container for Fractal, Spiro, and Edit sections.
    """

    def __init__(self, parent, command_map=None, bg="#333333"):
        super().__init__(parent, bg=bg)
        self.command_map = command_map or {}

        # Fractal section
        self.fractal_section = CollapsibleSection(
            self, "Fractal Tools",
            ["Line", "Triangle", "Square"],
            command_map=self.command_map,
            bg=bg
        )
        self.fractal_section.pack(fill=tk.X, pady=2)

        # Spiro section
        self.spiro_section = CollapsibleSection(
            self, "Spiro Tools",
            ["Spiro 1", "Spiro 2"],
            command_map=self.command_map,
            bg=bg
        )
        self.spiro_section.pack(fill=tk.X, pady=2)

        # Edit section
        self.edit_section = CollapsibleSection(
            self, "Edit Tools",
            ["Color", "Thickness", "Line Style", "Eraser", "Clear"],
            command_map=self.command_map,
            bg=bg
        )
        self.edit_section.pack(fill=tk.X, pady=2)
