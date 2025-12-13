# Detailed Flow of Fractal Spiro Paint

This document describes the full flow of the **Fractal Spiro Paint** application.

---

## Main
- `main()` is executed.
- `ToolsManager` is created.
- All tools are registered.
- `App(tools_manager)` is instantiated.
- `PaintWindow(app)` is created.
- `app.set_ui(paint_window)` establishes circular references.

---

## App
- Holds:
  - `ToolsManager`
  - `ShapeManager`
  - `ThemeService`
- In `set_ui()`:
  - Registers `update_theme` as observer.
  - Creates `CanvasController`.
  - Injects canvas references.
  - Sets circular reference with controller.

---

## PaintWindow
- Initializes:
  - `root`
  - `Menubar`
  - `Toolbar`
  - `MainCanvas`
  - `SecondaryCanvas`
- UI buttons trigger callbacks in `App`.

---

## CanvasController
- Handles mouse and keyboard events.
- Controls drawing logic.
- Manages active tool.
- Communicates with `App` and managers.

---

## ThemeService
- Implements Observer pattern.
- Notifies UI when theme changes.

---

## Conclusion
The architecture works but is tightly coupled and could benefit from better decoupling.
