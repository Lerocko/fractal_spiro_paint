# Flujo detallado de Fractal Spiro Paint

Este documento describe el flujo completo de la aplicación **Fractal Spiro Paint**, incluyendo referencias entre objetos, eventos y diagramas Mermaid.

---

## 1. Flujo narrativo

### Main
- `main()` imprime mensaje de bienvenida.
- Se instancian objetos núcleo en este orden:
  1. `ToolsManager`
  2. Registro de todas las herramientas en `ToolsManager`
  3. `App(tools_manager)`
  4. `PaintWindow(app)`
  5. Referencia circular: `app.set_ui(paint_window)`

### App
- Guarda `tools_manager` como atributo.
- Instancia `ThemeService` y `ShapeManager`.
- `set_ui(main_window)`:
  - Guarda `main_window`
  - Registra `update_theme` en `ThemeService`
  - Instancia `CanvasController(main_canvas, secondary_canvas, tools_manager, shape_manager, root)`
  - `canvas_controller.set_app_reference(self)`
  - `main_canvas.set_controller(canvas_controller)`
  - `secondary_canvas.set_controller(canvas_controller)`

### PaintWindow
- Instancia `root`, `menubar`, `toolbar`.
- Inicializa menubar, toolbar y canvases:
  - `_init_menubar()` → `Menubar(on_click_callback=self.app.handle_file_action)`
  - `_init_toolbars()` → `Toolbar(on_click_callback=self.app.handle_tool_selection)`
  - `_init_canvases()` → `MainCanvas(root)` y `SecondaryCanvas(main_canvas)`

### Eventos y flujo de botones
- Tool Selection:
  1. Usuario presiona botón
  2. Lambda activa `App.handle_tool_selection`
  3. `ToolsManager.set_active_tool(name, category)`
  4. `CanvasController.on_tool_changed()` → instancia herramienta activa y guarda referencia a `App`

### CanvasController
- Constructor guarda referencias a `main_canvas`, `secondary_canvas`, `tools_manager`, `shape_manager`, `root`.
- Eventos: `handle_click`, `handle_drag`, `handle_release`
- Métodos de teclado para cada canvas
- `set_app_reference(app)` → referencia circular a App

### ThemeService y Observer
- `register_observer(observer)` guarda referencias en `_observers`
- Al cambiar tema, llama cada observer con `mode` (`"dark"` o `"light"`)

### Referencias clave
- `App` ↔ `CanvasController` ↔ `PaintWindow`
- `MainCanvas` / `SecondaryCanvas` conocen su controlador
- Herramientas guardan referencia a `App`

---

## 2. Diagrama Mermaid (flujo de objetos)

```mermaid
graph TD
    Main["main()"]
    ToolsManager["ToolsManager"]
    AppObj["App"]
    PaintWindowObj["PaintWindow"]
    MainCanvasObj["MainCanvas"]
    SecondaryCanvasObj["SecondaryCanvas"]
    CanvasControllerObj["CanvasController"]
    ThemeServiceObj["ThemeService"]

    Main --> ToolsManager
    Main --> AppObj
    Main --> PaintWindowObj
    AppObj --> ToolsManager
    AppObj --> ThemeServiceObj
    AppObj --> CanvasControllerObj
    PaintWindowObj --> MainCanvasObj
    PaintWindowObj --> SecondaryCanvasObj
    MainCanvasObj --> CanvasControllerObj
    SecondaryCanvasObj --> CanvasControllerObj
    CanvasControllerObj --> AppObj
    ThemeServiceObj --> PaintWindowObj
