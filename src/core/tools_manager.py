# =============================================================
# File: tools_manager.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-10-12
# Refactored: 2025-11-23
# Description:
#     Manages the registration and state of all drawing tools.
#     Properly integrates with ThemeManager and supports both primary and secondary tools.
# =============================================================

import tkinter as tk
from typing import Dict, Optional, TYPE_CHECKING
from src.core.shape_manager import ShapeManager

if TYPE_CHECKING:
    from ..tools.base_tool import BaseTool

# =============================================================
# Tools Manager Class
# =============================================================
class ToolsManager:
    """
    Manages the registration and state of drawing tools.
    This class is the single source of truth for tool state and acts as a factory
    for tool instances.
    """

    # =============================================================
    # Initialization
    # =============================================================
    def __init__(self) -> None:
        """Initializes the ToolsManager with a clean, encapsulated state."""
        # --- Primary Tool State (e.g., Fractal, Spiro) ---
        self.main_category: Optional[str] = None
        self.main_tool: Optional[str] = None
        self._active_main_tool_class: Optional[type] = None

        # --- Secondary Tool State (e.g., Drawing, Edit) ---
        self.secondary_category: Optional[str] = None
        self.secondary_tool: Optional[str] = None
        self._active_secondary_tool_class: Optional[type] = None
        
        # --- Drawing State ---
        self.width: int = 2
        self.eraser: bool = False
        self.fill: bool = False
        
        # --- Tool Registry ---
        self._registered_tools: Dict[str, type] = {}

    # =============================================================
    # Tool Management Methods
    # =============================================================
    def set_active_tool(self, category: str, tool: str) -> None:
        """
        Set the currently active tool according to its category.
        This method is the central point for updating tool state.
        """
        if category == "Selection":
            self.main_category = category
            self.main_tool = tool
            self._active_main_tool_class = self.get_tool(tool)
        elif category in ["Fractal", "Spiro"]:
            self.main_category = category
            self.main_tool = tool
            self._active_main_tool_class = self.get_tool(tool)
        elif category in ["Drawing", "Edit"]:
            self.secondary_category = category
            self.secondary_tool = tool
            self._active_secondary_tool_class = self.get_tool(tool)

    def get_active_tool_info(self) -> Dict[str, Optional[str]]:
        """Returns a dictionary of the currently active tool info."""
        return {
            "main_category": self.main_category,
            "main_tool": self.main_tool,
            "secondary_category": self.secondary_category,
            "secondary_tool": self.secondary_tool
        }

    # =============================================================
    # Drawing State Accessors
    # =============================================================
    def get_drawing_color(self) -> str:
        """
        Returns the current drawing color.
        Delegates to ThemeManager to get the default color for the current theme.
        """
        # Import here to avoid circular dependency with theme_manager
        from .theme_manager import get_color
        
        # This logic can be expanded to support custom colors later
        return get_color("drawing_default")

    def get_width(self) -> int:
        return self.width

    def is_eraser_active(self) -> bool:
        return self.eraser

    def is_fill_active(self) -> bool:
        return self.fill

    # =============================================================
    # Tool Class Registry (Core functionality)
    # =============================================================
    def register_tool(self, name: str, cls: type) -> None:
        """
        Register a tool class to make it available in the application.
        """
        self._registered_tools[name] = cls
        print(f"Registered tool: {name}") # Debug

    def get_tool(self, name: str) -> Optional[type]:
        """Retrieve a registered tool class by name."""
        return self._registered_tools.get(name)

    def get_active_tool_instance(self, canvas: tk.Canvas, shape_manager: ShapeManager, category: str) -> Optional["BaseTool"]:
        """
        Creates and returns an instance of the currently active MAIN tool.
        """
        print(f"DEBUG: _active_main_tool_class is {self._active_main_tool_class}") # Debug

        if self._active_main_tool_class:
            if issubclass(self._active_main_tool_class, BaseTool):
                return self._active_main_tool_class(canvas, shape_manager, category)
        return None

    def get_active_secondary_tool_instance(self, canvas: tk.Canvas) -> Optional["BaseTool"]:
        """
        Creates and returns an instance of the currently active SECONDARY tool.
        This method will be useful for tools that modify the behavior of others.
        """
        if self._active_secondary_tool_class:
            from ..tools.base_tool import BaseTool
            if issubclass(self._active_secondary_tool_class, BaseTool):
                return self._active_secondary_tool_class(canvas)
        return None