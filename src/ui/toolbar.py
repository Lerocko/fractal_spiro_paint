import tkinter as tk
from tkinter import Frame, Button, Label
from typing import List, Dict, Optional, Callable

# Default colors (can be easily changed or themed)
BG_COLOR = "#333333"
FG_COLOR = "#f1f1f1"
BUTTON_BG = "#3a3a3a"
BUTTON_ACTIVE_BG = "#6e6a6a"


class CollapsibleSection(Frame):
    """
    A collapsible section containing a header with a label and toggle arrow,
    and a content frame that holds buttons or other widgets.
    
    Clicking the header toggles visibility of the content frame.
    """

    def __init__(
        self,
        parent: tk.Widget,
        title: str,
        buttons: List[str],
        command_map: Optional[Dict[str, Callable]] = None,
        bg: str = BG_COLOR,
        fg: str = FG_COLOR
    ):
        """
        Initialize the collapsible section.

        Args:
            parent (tk.Widget): Parent widget.
            title (str): Section title.
            buttons (List[str]): List of button labels.
            command_map (Dict[str, Callable], optional): Mapping from button names to commands.
            bg (str): Background color.
            fg (str): Foreground (text) color.
        """
        super().__init__(parent, bg=bg)
        self.title = title
        self.buttons = buttons
        self.command_map = command_map or {}

        # Track expanded/collapsed state
        self.expanded = True

        # Create header frame with title and arrow
        self.header_frame = Frame(self, bg=bg)
        self.header_frame.pack(fill=tk.X)

        self.arrow = Label(self.header_frame, text="▼", bg=bg, fg=fg, font=("Arial", 10))
        self.arrow.pack(side=tk.LEFT, padx=5)

        self.title_label = Label(self.header_frame, text=title, bg=bg, fg=fg, font=("Arial", 11, "bold"))
        self.title_label.pack(side=tk.LEFT, pady=5)

        # Bind click events to toggle content visibility
        for widget in (self.header_frame, self.title_label, self.arrow):
            widget.bind("<Button-1>", self.toggle)

        # Content frame that will hold the buttons
        self.content_frame = Frame(self, bg=bg)
        self.content_frame.pack(fill=tk.X)

        # Generate buttons
        self.create_buttons()

    def create_buttons(self) -> None:
        """Create and pack buttons dynamically into the content frame."""
        for name in self.buttons:
            btn = Button(
                self.content_frame,
                text=name,
                bg=BUTTON_BG,
                fg=FG_COLOR,
                relief=tk.FLAT,
                bd=0,
                padx=5,
                pady=5,
                activebackground=BUTTON_ACTIVE_BG,
            )
            if name in self.command_map:
                btn.config(command=self.command_map[name])
            btn.pack(fill=tk.X, padx=10, pady=2)

    def toggle(self, event: Optional[tk.Event] = None) -> None:
        """
        Toggle visibility of the content frame.

        Args:
            event (tk.Event, optional): Tkinter event (unused).
        """
        if self.expanded:
            self.content_frame.forget()
            self.arrow.config(text="►")
        else:
            self.content_frame.pack(fill=tk.X)
            self.arrow.config(text="▼")
        self.expanded = not self.expanded


class Toolbar(Frame):
    """
    Toolbar container holding multiple collapsible sections.
    Designed to hold sections like Fractal, Spiro, and Edit tools.
    """

    def __init__(self, parent: tk.Widget, command_map: Optional[Dict[str, Callable]] = None, bg: str = BG_COLOR):
        """
        Initialize the toolbar.

        Args:
            parent (tk.Widget): Parent widget.
            command_map (Dict[str, Callable], optional): Mapping of button names to functions.
            bg (str): Background color.
        """
        super().__init__(parent, bg=bg)
        self.command_map = command_map or {}

        # Define sections with their buttons
        sections = [
            ("Fractal Tools", ["Line", "Triangle", "Square"]),
            ("Spiro Tools", ["Spiro 1", "Spiro 2"]),
            ("Edit Tools", ["Color", "Thickness", "Line Style", "Eraser", "Clear"])
        ]

        # Create CollapsibleSections dynamically
        self.sections: Dict[str, CollapsibleSection] = {}
        for title, buttons in sections:
            section = CollapsibleSection(
                self,
                title=title,
                buttons=buttons,
                command_map=self.command_map,
                bg=bg
            )
            section.pack(fill=tk.X, pady=2)
            self.sections[title] = section
