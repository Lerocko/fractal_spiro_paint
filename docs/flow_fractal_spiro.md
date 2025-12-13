# Flujo detallado de Fractal Spiro Paint

Este documento describe el flujo completo de la aplicación **Fractal Spiro Paint**, incluyendo referencias entre objetos, eventos y responsabilidades.

---

## Main
- Se ejecuta `main()`.
- Se instancia `ToolsManager`.
- Se registran todas las herramientas.
- Se crea `App(tools_manager)`.
- Se crea `PaintWindow(app)`.
- Se llama `app.set_ui(paint_window)` estableciendo referencias circulares.

---

## App
- Contiene:
  - `ToolsManager`
  - `ShapeManager`
  - `ThemeService`
- En `set_ui()`:
  - Registra `update_theme` como observer.
  - Crea `CanvasController`.
  - Inyecta referencias a canvases.
  - Establece referencia circular con `CanvasController`.

---

## PaintWindow
- Inicializa:
  - `root`
  - `Menubar`
  - `Toolbar`
  - `MainCanvas`
  - `SecondaryCanvas`
- Los botones llaman callbacks en `App`.

---

## CanvasController
- Recibe eventos de mouse y teclado.
- Decide la lógica de dibujo.
- Gestiona la herramienta activa.
- Se comunica con `App` y `ToolsManager`.

---

## ThemeService
- Implementa patrón Observer.
- Notifica cambios de tema a la UI.

---

## Referencias clave
- `App ↔ CanvasController ↔ PaintWindow`
- Canvases conocen su controlador.
- Herramientas conocen `App`.

---

## Conclusión
El flujo es funcional pero acoplado. Se recomienda desacoplar mediante eventos o signals.
