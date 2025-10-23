"""
paint_window.py
Main GUI window for Fractal Spiro Paint.
Integrates Toolbar and Canvas widgets modules.
"""

import tkinter as tk
from toolbar import Toolbar
from menubar import Menubar

class PaintWindow:
    """
    Main application window for Fractal Spiro Paint.
    """

    def __init__(self, width=800, height=600):
        """Initialize the main window, toolbar, and drawing canvas."""
        self.width = width
        self.height = height

        # Create main window
        self.root = tk.Tk()
        self.root.title("Fractal Spiro Paint")
        self.root.geometry(f"{self.width}x{self.height}+250+60")
        self.root.configure(bg="#1e1e1e")
        self.root.attributes("-alpha", 1)
        self.current_theme = "dark"  # Default theme

        # Files frame
        self.files_frame = tk.Frame(self.root, bg="#252526", height=40)
        self.files_frame.pack(side=tk.TOP, fill=tk.X)
        self.files_frame.pack_propagate(False)

        # Toolbar frame
        self.toolbar_frame = tk.Frame(self.root, bg="#252526", height=80)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)
        self.toolbar_frame.pack_propagate(False)

        # Create File frame buttons
        self.files_frame_buttons = Menubar(self.files_frame, on_click_callback=self.on_file_action)
        self.files_frame_buttons.pack(fill=tk.X)

        # Create specific tool buttons frames in the toolbar frame
        subframes = ["Fractal", "Spiro", "Drawing", "Edit"]
        for name in subframes:
            self.create_toolbar_subframes(name, on_click_callback=self.on_tool_selected)      
        
        # Canvas frame
        self.canvas_frame = tk.Frame(self.root, bg="#252526")
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.Main_Canvas = tk.Canvas(self.canvas_frame, bg="#1E1E20", highlightthickness=0)
        self.Main_Canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Initialize secondary canvas but do not pack it yet
        self.secondary_canvas_frame = tk.Frame(self.canvas_frame, bg="#252526")    
        self.Secondary_Canvas = tk.Canvas(self.secondary_canvas_frame, bg="#252526", height=2)

    def on_file_action(self, action):
        """Handle clicks from Menubar buttons."""
        if action == "Dark/Light":
            new_theme = "light" if self.current_theme == "dark" else "dark"
            self.toggle_theme(new_theme)

    def on_tool_selected(self, category, tool):
        """Handle clicks from Toolbar buttons."""
        if category == "Fractal":
            self.secondary_canvas_frame.pack(side=tk.BOTTOM, padx=150, pady=50)
            self.Secondary_Canvas.pack(side=tk.BOTTOM, fill=tk.X)
        else:
            self.secondary_canvas_frame.pack_forget()
            self.Secondary_Canvas.pack_forget()
        
    '''def update_secondary_canvas(self, active_fractal_tools):
        """Show or hide the secondary canvas based on selected fractal tools."""
        fractal_tool = "SomeFractalTool"  # Replace with actual tool name to check):
        self.secondary_canvas_frame.pack_forget()
        self.Secondary_Canvas.pack_forget()
        if fractal_tool in active_fractal_tools:
            self.secondary_canvas_frame.pack(side=tk.BOTTOM, padx=150, pady=50)
            self.Secondary_Canvas.pack(side=tk.BOTTOM, fill=tk.X)'''

    # Create toolbar sub-frames
    def create_toolbar_subframes(self, name, bg="#252526", on_click_callback=None):
        """Create sub-frames within the toolbar for different tool categories."""
        # Outer frame for each category
        frame = tk.Frame(self.toolbar_frame, bg=bg)
        frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=0, pady=0)
        setattr(self, f"{name}_frame", frame)

        # Inner frame for buttons
        buttons_frame = tk.Frame(frame, bg=bg)
        buttons_frame.pack(side=tk.TOP, pady=2)  

        # Create Toolbar instance for the category
        buttons = Toolbar(buttons_frame, category=name, on_click_callback=on_click_callback)
        buttons.pack()  
        setattr(self, f"{name}_buttons", buttons)

        # Label for the category
        label = tk.Label(frame, text=f"{name} Tools", bg=bg, fg="white")
        label.pack(side=tk.BOTTOM, pady=2)  
        setattr(self, f"{name}_label", label)

        


    
    def toggle_theme(self, theme):
        # Define color schemes for dark and light themes
        colors = {
        "root": ("#1e1e1e", "#f0f0f0"),
        "files_frame": ("#252526", "#dcdcdc"),
        "toolbar_frame": ("#252526", "#dcdcdc"),
        "canvas_frame": ("#252526", "#e0e0e0"),
        "canvas_main": ("#1E1E20", "#ffffff"),
        "canvas_sec": ("#252526", "#e0e0e0"),
        "labels_bg": ("#252526", "#dcdcdc"),
        "labels_fg": ("white", "black"),
        "button_bg": ("#252526", "#dcdcdc"),
        "button_fg": ("white", "black"),
        }

        index = 0 if theme == "dark" else 1
    
        # Apply colors on root and frames
        for attr in ["root", "files_frame", "toolbar_frame", "canvas_frame"]:
            widget = getattr(self, attr)
            widget.configure(bg=colors[attr][index])

        # Apply colors on canvases
        self.Main_Canvas.configure(bg=colors["canvas_main"][index])
        self.secondary_canvas_frame.configure(bg=colors["canvas_sec"][index])
        self.Secondary_Canvas.configure(bg=colors["canvas_sec"][index])

        # Apply colors on labels
        for label_attr in ["Fractal_label", "Spiro_label", "Drawing_label", "Edit_label"]:
            label = getattr(self, label_attr)
            label.configure(bg=colors["labels_bg"][index], fg=colors["labels_fg"][index])

        # Apply colors on any buttons if they exist
        for btn in self.buttons if hasattr(self, 'buttons') else []:
            btn.configure(bg=colors["button_bg"][index], fg=colors["button_fg"][index])

        self.current_theme = theme
        
        


    def start(self):
        """Start the Tkinter main event loop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = PaintWindow()
    app.start()
