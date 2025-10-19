# src/main.py

# Import standard libraries
import sys

# Import our modules
from src.fractal import fractal_drawer
from src.spiro import spiro_drawer
from src.ui import paint_window

def main():
    """
    Entry point for the Fractal Spiro Paint application.
    """
    print("Welcome to Fractal Spiro Paint!")
    # Aquí más adelante iniciaremos la interfaz y lógica
    # por ahora solo prueba que los imports funcionan
    # y que el programa corre sin errores.
    
if __name__ == "__main__":
    main()
    app = paint_window.PaintWindow()
    app.start()
