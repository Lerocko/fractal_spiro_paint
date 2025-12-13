
---

## 4️⃣ `docs/flow_fractal_spiro_combined_en.md` (VISUAL PROFESIONAL COMBINADO)

```markdown
# Combined Visual Flow of Fractal Spiro Paint

```mermaid
%%{init: {"theme": "base"}}%%
graph TD
    subgraph UI["User Interface"]
        PW["PaintWindow"]
        MC["MainCanvas"]
        SC["SecondaryCanvas"]
        TB["Toolbar"]
        MB["Menubar"]
    end

    subgraph Logic["Logic / Controllers"]
        App["App"]
        CC["CanvasController"]
    end

    subgraph Services["Services"]
        TM["ToolsManager"]
        SM["ShapeManager"]
        TS["ThemeService"]
    end

    App --> TM
    App --> SM
    App --> TS
    App --> PW

    PW --> MC
    PW --> SC
    PW --> TB
    PW --> MB

    MC --> CC
    SC --> CC
    CC --> App
