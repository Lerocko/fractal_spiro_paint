"""
fractal_tool.py
Orchestrates Fractal tools by using registered tool classes from tools_manager.
"""

from typing import Optional, Tuple
from ui import tools_manager
import tkinter as tk

# =============================================================
# Fractal tools entry
# =============================================================

def use_tool(tool_name: str, canvas: tk.Canvas, start: Tuple[int, int], end: Tuple[int, int]) -> Optional[str]:
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
    # Obtener la clase de herramienta registrada
    ToolClass = tools_manager.get_tool(tool_name)
    if not ToolClass:
        print(f"Tool '{tool_name}' is not registered.")
        return None
    
    # Crear instancia y pasar canvas
    tool_instance = ToolClass(canvas)
    
    # Ejecutar el método de dibujo
    return tool_instance.draw(start, end)
