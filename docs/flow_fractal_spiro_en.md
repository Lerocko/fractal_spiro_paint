# Detailed Flow of Fractal Spiro Paint

This document describes the complete flow of the **Fractal Spiro Paint** application, including object references, events, and Mermaid diagrams.

---

## 1. Narrative Flow

### Main
- `main()` prints welcome message.
- Core objects instantiated in this order:
  1. `ToolsManager`
  2. Register all tools in `ToolsManager`
  3. `App(tools_manager)`
  4. `PaintWindow(app)`
  5. Circular reference: `app.set_ui(paint_window)`

### App
- Stores `tools_manager` as an attribute.
- Instantiates `ThemeService` and `ShapeManager`.
- `set_ui(main_window)`:
  - Stores `main_window`
  - Registers `update_theme` in `ThemeService`
  - Instantiates `CanvasController(main_canvas, secondary_canvas, tools_manager, shape_manager, root)`
  - `canvas_controller.set_app_reference(self)`
  - `main_canvas.set_controller(canvas_controller)`
  - `secondary_canvas.set_controller(canvas_controller)`

### PaintWindow
- Instantiates `root`, `menubar`, `toolbar`.
- Initializes menubar, toolbar, and canvases:
  - `_init_menubar()` → `Menubar(on_click_callback=self.app.handle_file_action)`
  - `_init_toolbars()` → `Toolbar(on_click_callback=self.app.handle_tool_selection)`
  - `_init_canvases()` → `MainCanvas(root)` and `SecondaryCanvas(main_canvas)`

### Events and Button Flow
- Tool Selection:
  1. User clicks button
  2. Lambda triggers `App.handle_tool_selection`
  3. `ToolsManager.set_active_tool(name, category)`
  4. `CanvasController.on_tool_changed()` → instantiates active tool and stores reference to `App`

### CanvasController
- Constructor stores references to `main_canvas`, `secondary_canvas`, `tools_manager`, `shape_manager`, `root`.
- Mouse events: `handle_click`, `handle_drag`, `handle_release`
- Keyboard events for each canvas
- `set_app_reference(app)` → circular reference to App

### ThemeService and Observer
- `register_observer(observer)` stores method references in `_observers`
- On theme change, calls each observer with `mode` (`"dark"` or `"light"`)

### Key References
- `App` ↔ `CanvasController` ↔ `PaintWindow`
- `MainCanvas` / `SecondaryCanvas` know their controller
- Tools store reference to `App`

---

## 2. Mermaid Diagram (Object Flow)

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
