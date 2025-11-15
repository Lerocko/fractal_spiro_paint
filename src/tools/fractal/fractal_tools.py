# =============================================================
# File: fractal_tools.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-11-12
# Refactored: 2025-11-15
# Description:
#     Orchestrates fractal tools by retrieving registered tool
#     classes from ToolsManager and executing their draw method.
# =============================================================

from typing import Optional, Tuple, Type
from src.core import tools_manager
import tkinter as tk

# =============================================================
# Public API
# =============================================================

def use_tool(
    tool_name: str,
    canvas: tk.Canvas,
    start: Tuple[int, int],
    end: Tuple[int, int]
) -> Optional[str]:
    """
    Use the tool with the given name on the canvas with start/end coordinates.
    
    Args:
        tool_name (str): Name of the tool (e.g., "Line", "Poligon", "RegPoly")
        canvas (tk.Canvas): The canvas where to draw.
        start (tuple[int,int]): Starting coordinates.
        end (tuple[int,int]): Ending coordinates.
    
    Returns:
        Optional[str]: Optional return value from the tool's draw method.
    """

    # ---------------------------------------------------------
    # Retrieve registered tool class
    # ---------------------------------------------------------
    ToolClass: Optional[Type] = tools_manager.get_tool(tool_name)

    if not ToolClass:
        print(f"Tool '{tool_name}' is not registered.") # Debug
        return None
    
    # ---------------------------------------------------------
    # Create tool instance
    # ---------------------------------------------------------
    tool_instance = ToolClass(canvas)
    
    # ---------------------------------------------------------
    # Execute drawing
    # ---------------------------------------------------------
    return tool_instance.draw(start, end) # type: ignore
