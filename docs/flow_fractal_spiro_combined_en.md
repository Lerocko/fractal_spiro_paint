# Combined Visual Flow of Fractal Spiro Paint (UI + Logic + Events)

This enhanced Mermaid diagram shows architecture and runtime flow, including events and component interactions.

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

    %% Events - purple
    subgraph Events["Events / Actions"]
        ToolSelect["Tool Selection"]:::event
        MouseClick["Mouse Click / Drag / Release"]:::event
        Keyboard["Keyboard Events"]:::event
        ThemeChange["Theme Change"]:::event
    end

    %% Connections - architecture
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

    %% Connections - events
    TB -->|click| ToolSelect
    ToolSelect -->|updates| TM
    TM -->|notifies| CC
    CC -->|updates tool| MC
    CC -->|updates tool| SC

    MC -->|mouse actions| MouseClick
    SC -->|mouse actions| MouseClick
    MouseClick --> CC
    Keyboard --> CC
    ThemeChange --> TS
    TS -->|applies theme| PW

    %% Styling
    classDef ui fill:#1f77b4,stroke:#000,stroke-width:1px,color:#fff;
    classDef logic fill:#2ca02c,stroke:#000,stroke-width:1px,color:#fff;
    classDef service fill:#ff7f0e,stroke:#000,stroke-width:1px,color:#fff;
    classDef event fill:#9467bd,stroke:#000,stroke-width:1px,color:#fff;

Notes

Blue nodes → UI elements

Green nodes → Controller / App logic

Orange nodes → Managers / Services

Purple nodes → Events / Actions

Interactive Mermaid on GitHub