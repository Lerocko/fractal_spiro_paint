# Visual Flow of Fractal Spiro Paint (Enhanced)

This Mermaid diagram highlights the application structure with colors for UI, logic, and services.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#1f77b4","secondaryColor": "#ff7f0e","tertiaryColor": "#2ca02c","edgeLabelBackground":"#ffffff"}}}%%
graph TD
    %% UI components - blue
    subgraph UI["User Interface"]
        PW[/"PaintWindow"/]:::ui
        MC[/"MainCanvas"/]:::ui
        SC[/"SecondaryCanvas"/]:::ui
        TB[/"Toolbar"/]:::ui
        MB[/"Menubar"/]:::ui
    end

    %% Logic / Controller - green
    subgraph Logic["Controller & App"]
        AppObj["App"]:::logic
        CC["CanvasController"]:::logic
    end

    %% Services / Managers - orange
    subgraph Services["Managers / Services"]
        TM["ToolsManager"]:::service
        SM["ShapeManager"]:::service
        TS["ThemeService"]:::service
    end

    %% Connections
    AppObj -->|manages| TM
    AppObj -->|manages| SM
    AppObj -->|observes| TS
    AppObj -->|sets UI| PW

    PW --> MC
    PW --> SC
    PW --> TB
    PW --> MB

    MC -->|events| CC
    SC -->|events| CC
    CC -->|callback| AppObj

    TS -->|notifies| PW

    %% Styling
    classDef ui fill:#1f77b4,stroke:#000,stroke-width:1px,color:#fff;
    classDef logic fill:#2ca02c,stroke:#000,stroke-width:1px,color:#fff;
    classDef service fill:#ff7f0e,stroke:#000,stroke-width:1px,color:#fff;

Notes

Blue nodes → UI elements

Green nodes → Controller / App logic

Orange nodes → Managers / Services

This diagram is interactive on GitHub with Mermaid support.