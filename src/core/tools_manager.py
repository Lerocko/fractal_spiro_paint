"""
tools_manager.py
Control and managing activeted tools and theyre staites
"""
import tkinter as tk
from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..tools.base_tool import BaseTool
# =============================================================
# Global tool state
# =============================================================
main_category: Optional[str] = None
main_tool: Optional[str] = None
secondary_category: Optional[str] = None
secondary_tool: Optional[str] = None
current_theme: str = "dark"
color: str = "white"
width: int = 2
eraser: bool = False
fill: bool = False
_active_tool_class: Optional[type] = None

# =============================================================
# Tools management functions
# =============================================================
def set_tools(category: str, tool: str) -> None:
    """Set the currently active tool according to its category.
    Now also sets the active tool class.
    """
    global main_category, main_tool, secondary_category, secondary_tool,  _active_tool_class

    if category in ["Fractal", "Spiro"]:
        main_category = category
        main_tool = tool
        _active_tool_class = get_tool(tool)
    elif category in ["Drawing", "Edit"]:
        secondary_category = category
        secondary_tool = tool

def get_active_tools() -> Dict[str, Optional[str]]:
    return {
        "main_category": main_category,
        "main_tool": main_tool,
        "secondary_category": secondary_category,
        "secondary_tool": secondary_tool
    }

# =============================================================
# Individual state accessors
# =============================================================
def current_main_category() -> Optional[str]:
    return main_category

def current_main_tool() -> Optional[str]:
    return main_tool

def current_secondary_tool() -> Optional[str]:
    return secondary_tool

def current_color() -> str:
    global current_theme, color
    if color is None:
        return "white" if current_theme == "dark" else "black"
    return color

def current_width() -> str:
    return width

def is_eraser_active() -> bool:
    return eraser

def is_fill_active() -> bool:
    return fill

# =============================================================
# Tool class registry
# =============================================================

_registered_tools: Dict[str, type] = {}

def register_tool(name: str, cls: type) -> None:
    """
    Register a tool class to make it available in the application.
    This should be called once at application startup.
    """
    _registered_tools[name] = cls
    print(f"Registered tool: {name}") #Debug

def get_tool(name: str) -> Optional[type]:
    """Retrieve a registered tool class by name."""
    return _registered_tools.get(name)

def get_active_tool_instance(canvas: tk.Canvas) -> Optional["BaseTool"]:
    """
    Creates and returns an instance of the currently active tool.
    """
    if _active_tool_class:
        from ..tools.base_tool import BaseTool
        if issubclass(_active_tool_class, BaseTool):
            return _active_tool_class(canvas)
    return None