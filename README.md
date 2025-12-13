# Fractal Spiro Paint

Interactive Python application to draw fractals and spirographs in a user-friendly interface.

## Features

- Draw multiple types of fractals (regular, irregular, customizable divisions)
- Draw spirographs with interactive circles and moving pen
- Save your creations in PNG, JPG, or JPEG
- Multiple patterns can overlap on the same canvas
- Error handling for smooth user experience

## Project Structure

fractal_spiro_paint/
├── src/          
│   ├── fractal/      (Fractal drawing modules)

│   ├── spiro/        (Spirograph drawing modules)

│   └── ui/           (User interface code)

├── tests/            (Test scripts)

├── venv/             (Virtual environment, ignored by Git)

├── .gitignore

├── requirements.txt

└── README.md



## Setup

1. Create virtual environment: `python -m venv venv`
2. Activate environment: `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Run the app: `python src/main.py`


## Documentation

The Fractal Spiro Paint project is documented in detail in the `docs/` folder:

### Narrative Documentation
- **Spanish (personal reference):** [flow_fractal_spiro.md](docs/flow_fractal_spiro.md)
- **English:** [flow_fractal_spiro_en.md](docs/flow_fractal_spiro_en.md)

### Visual Diagrams
- **Simple Visual (English):** [flow_fractal_spiro_visual_en.md](docs/flow_fractal_spiro_visual_en.md)
- **Combined Visual - Architecture + Runtime (English):** [flow_fractal_spiro_combined_en.md](docs/flow_fractal_spiro_combined_en.md)

> **Tip:** The combined visual diagram shows UI components, controllers, managers, and event flow for a full overview of the application.

