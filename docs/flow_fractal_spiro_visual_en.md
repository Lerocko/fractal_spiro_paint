# Visual Flow of Fractal Spiro Paint

```mermaid
graph TD
    App --> PaintWindow
    App --> CanvasController
    App --> ToolsManager
    App --> ThemeService

    PaintWindow --> MainCanvas
    PaintWindow --> SecondaryCanvas

    MainCanvas --> CanvasController
    SecondaryCanvas --> CanvasController

    CanvasController --> App

