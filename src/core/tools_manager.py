# =============================================================
# File: tools_manager.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-10-12
# Refactored: 2025-12-19
# Description:
#     Manages the registration and state of all drawing tools.
#     Properly integrates with ThemeManager and supports both primary and secondary tools.
# =============================================================

import logging
import tkinter as tk
from typing import Dict, Optional, Type, TYPE_CHECKING

from src.core.shape_manager import ShapeManager
from src.tools.base_tool import BaseTool

# Use TYPE_CHECKING to avoid runtime import errors for type hints
if TYPE_CHECKING:
    # This import is only for type checkers like MyPy
    pass

# =============================================================
# Tools Manager Class
# =============================================================
class ToolsManager:
    """
    Manages the registration and state of drawing tools.

    This class is the single source of truth for tool state and acts as a factory
    for tool instances. It handles both primary and secondary tool categories.
    """

    # =============================================================
    # Initialization
    # =============================================================
    def __init__(self) -> None:
        """Initializes the ToolsManager with a clean, encapsulated state."""
        # --- Primary Tool State (e.g., Fractal, Spiro) ---
        self.main_category: Optional[str] = None
        self.main_tool: Optional[str] = None
        self._active_main_tool_class: Optional[Type[BaseTool]] = None

        # --- Secondary Tool State (e.g., Drawing, Edit) ---
        self.secondary_category: Optional[str] = None
        self.secondary_tool: Optional[str] = None
        self._active_secondary_tool_class: Optional[Type[BaseTool]] = None
        
        # --- Drawing State ---
        self.width: int = 2
        self.eraser: bool = False
        self.fill: bool = False
        
        # --- Tool Registry ---
        self._registered_tools: Dict[str, Type[BaseTool]] = {}

    # =============================================================
    # Tool Management Methods
    # =============================================================
    def set_active_tool(self, category: str, tool: str, is_pattern_tool: bool = False) -> None:
        """
        Sets the currently active tool based on its category and name.

        This method is the central point for updating the tool state. It updates
        the appropriate state variables (main or secondary) and retrieves the
        corresponding tool class.

        Args:
            category: The category of the tool (e.g., "Fractal", "Drawing").
            tool: The registered name of the tool.
            is_pattern_tool: True if this is the pattern tool for the secondary canvas.
        """
        tool_class = self.get_tool(tool)
        if not tool_class:
            logging.warning(f"Attempted to set an unregistered tool: {tool}")
            return

        if category == "Selection":
            self.main_category = category
            self.main_tool = tool
            self._active_main_tool_class = tool_class
        elif category in ["Fractal", "Spiro"]:
            self.main_category = category
            self.main_tool = tool
            self._active_main_tool_class = tool_class
        elif category in ["Drawing", "Edit"] or is_pattern_tool:
            self.secondary_category = category
            self.secondary_tool = tool
            self._active_secondary_tool_class = tool_class
        else:
            logging.error(f"Unknown tool category: {category}")

    def get_active_tool_info(self) -> Dict[str, Optional[str]]:
        """
        Returns a dictionary containing information about the currently active tools.

        Returns:
            A dictionary with keys for 'main_category', 'main_tool',
            'secondary_category', and 'secondary_tool'.
        """
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
        Retrieves the current drawing color.

        Delegates to the ThemeManager to get the default color for the current theme.

        Returns:
            The hexadecimal color string.
        """
        # Import here to avoid circular dependency with theme_manager
        from .theme_manager import get_color
        
        # This logic can be expanded to support custom colors later
        return get_color("drawing_default")

    def get_width(self) -> int:
        """Returns the current drawing width."""
        return self.width

    def is_eraser_active(self) -> bool:
        """Returns True if the eraser mode is active."""
        return self.eraser

    def is_fill_active(self) -> bool:
        """Returns True if fill mode is active."""
        return self.fill

    # =============================================================
    # Tool Class Registry (Core functionality)
    # =============================================================
    def register_tool(self, name: str, cls: Type[BaseTool]) -> None:
        """
        Registers a tool class to make it available in the application.

        Args:
            name: The unique name to register the tool under.
            cls: The tool class (not an instance).
        """
        if not name or not cls:
            logging.error("Tool registration requires a valid name and class.")
            return
            
        self._registered_tools[name] = cls
        logging.info(f"Registered tool: {name}")

    def get_tool(self, name: str) -> Optional[Type[BaseTool]]:
        """
        Retrieves a registered tool class by its name.

        Args:
            name: The name of the tool to retrieve.

        Returns:
            The tool class if found, otherwise None.
        """
        return self._registered_tools.get(name)

    def get_active_tool_instance(self, canvas: tk.Canvas, shape_manager: ShapeManager, category: str) -> Optional[BaseTool]:
        """
        Creates and returns an instance of the currently active main tool.

        Args:
            canvas: The Tkinter canvas to pass to the tool.
            shape_manager: The ShapeManager to pass to the tool.
            category: The category of the tool.

        Returns:
            An instance of the active tool, or None if no tool is active.
        """
        if self._active_main_tool_class:
            logging.debug(f"Creating instance of main tool: {self._active_main_tool_class.__name__}")
            return self._active_main_tool_class(canvas, shape_manager, category)
        return None

    def get_active_secondary_tool_instance(self, canvas: tk.Canvas, shape_manager: ShapeManager, category: str, allow_close: bool = False) -> Optional[BaseTool]:
        """
        Creates and returns an instance of the currently active secondary tool.

        Args:
            canvas: The Tkinter canvas to pass to the tool.
            shape_manager: The ShapeManager to pass to the tool.
            category: The category of the tool.
            allow_close: Whether the tool should allow closing (for PolylineTool).

        Returns:
            An instance of the active secondary tool, or None if no tool is active.
        """
        if self._active_secondary_tool_class:
            logging.debug(f"Creating instance of secondary tool: {self._active_secondary_tool_class.__name__}")
            # Check if this is a PolylineTool to pass the allow_close parameter
            if self._active_secondary_tool_class.__name__ == "PolylineTool":
                return self._active_secondary_tool_class(canvas, shape_manager, category, allow_close=allow_close)
            else:
                # For other secondary tools, use default parameters
                return self._active_secondary_tool_class(canvas, shape_manager, category)
        return None