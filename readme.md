# F1Tenth Raceline Editor

A comprehensive tool for editing and modifying F1Tenth racing lines with both GUI-based interactive editing and traditional GIMP-based workflow support.

## 🚀 Quick Start

### GUI Editor (Recommended)

```bash
python main.py
```

### Traditional GIMP Workflow

```bash
python -m racingline_drawer.src.drawer
# Edit in GIMP
python -m path_extractor.src.extractor
```

## 📁 Project Structure

```
raceline_editor/
├── assets/                     # Example images and documentation
├── config/                     # Configuration files
│   ├── __init__.py
│   └── config.py              # Path and color configurations
├── gui/                       # GUI application
│   ├── __init__.py
│   └── raceline_editor_gui.py # Main GUI application
├── mod_maps/                  # Generated maps for GIMP editing
├── original_maps/             # Track maps (PNG + YAML metadata)
│   ├── map.png
│   └── map.yaml
├── original_racinglines/      # Input raceline CSV files
│   └── input_racingline.csv
├── output_racinglines/        # Generated output racelines
│   └── output_racingline.csv
├── path_extractor/           # GIMP-based extraction tools
│   ├── src/
│   │   ├── extractor.py      # Extract paths from GIMP images
│   │   └── Node.py           # Path node class
│   └── temp_csvs/           # Temporary processing files
├── racingline_drawer/        # Map generation tools
│   └── src/
│       └── drawer.py         # Generate visual maps
├── main.py                   # GUI application launcher
├── requirements.txt          # Python dependencies
└── README.md
```

## ✨ Features

### 🖥️ GUI Editor

-   **Interactive Point Editing**: Click, drag, and modify raceline points in real-time
-   **Real-time Spline Visualization**: See smooth cubic spline curves as you edit
-   **Velocity Control**: Edit individual point velocities with dedicated controls
-   **Visual Map Overlay**: Work directly on top of track maps
-   **Zoom & Pan**: Navigate large maps with mouse wheel zoom and pan
-   **Undo/Redo Support**: Keyboard shortcuts for common operations
-   **Export/Import**: Save and load raceline CSV files

### 🎨 Traditional GIMP Workflow

-   **Pixel-Perfect Editing**: Use GIMP for precise manual path editing
-   **Color-Coded States**: Visual indicators for start, end, and path pixels
-   **Automatic Extraction**: Convert pixel art back to raceline coordinates

## 🛠️ Installation

### Prerequisites

-   Python 3.7+
-   Required packages (install via pip)

### Setup

1. Clone the repository:

```bash
git clone [repository-url]
cd raceline_editor
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Launch the GUI:

```bash
python main.py
```

## 📖 Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

**Required packages:**

-   `tkinter` (GUI framework)
-   `opencv-python` (Image processing)
-   `numpy` (Numerical computing)
-   `scipy` (Spline interpolation)
-   `pillow` (Image handling)
-   `pyyaml` (YAML file parsing)
-   `pandas` (Data manipulation)
-   `matplotlib` (Optional: plotting)

## 🎮 GUI Usage Guide

### Getting Started

1. **Launch**: Run `python main.py`
2. **Load Data**: The application automatically loads default map and raceline
3. **Start Editing**: Click on points to select and modify them

### Core Features

#### 🎯 Point Selection & Editing

-   **Select Points**: Click near any raceline point to select it
-   **Drag Points**: Click and drag selected points to new positions
-   **Point Information**: View coordinates and velocity in the right panel

#### ⚡ Velocity Editing

-   **Manual Entry**: Type velocity values in the input field
-   **Quick Buttons**: Use preset velocity buttons (0.5, 1.0, 1.5, 2.0, 3.0)
-   **Visual Feedback**: Selected points show velocity labels

#### 📍 Coordinate Editing

-   **Precise Control**: Enter exact X,Y coordinates manually
-   **Real-time Updates**: Changes reflect immediately on the map

#### ➕ Adding/Removing Points

-   **Add Points**: Click "Add Point" button, then click on map
-   **Delete Points**: Select a point and press Delete key or click "Delete Point"
-   **Minimum Points**: Maintains at least 3 points for valid racelines

#### 🎨 Spline Visualization

-   **Real-time Splines**: Green curves show smooth interpolated paths
-   **Adjustable Smoothness**: Control spline smoothness (0.01 - 1.0)
-   **Variable Resolution**: Adjust spline point density (50 - 500 points)

#### 🔍 Navigation

-   **Zoom**: Mouse wheel to zoom in/out
-   **Pan**: Automatic centering and manual offset adjustment
-   **Reset View**: Button to restore default view

#### 💾 File Operations

-   **Save**: Ctrl+S or "Save Raceline" button
-   **Load**: Ctrl+O or "Load Raceline" button
-   **Auto-format**: Saves with proper precision (7 decimal places)

### Keyboard Shortcuts

-   `Ctrl+S` - Save raceline
-   `Ctrl+O` - Load raceline
-   `Delete` - Delete selected point
-   `Enter` - Apply velocity/coordinate changes

## 🎨 Traditional GIMP Workflow

### Configuration

The project uses configuration enums for paths, colors, and processing parameters:

#### Drawer Configuration

| Parameter                | Default Value                               | Description            |
| ------------------------ | ------------------------------------------- | ---------------------- |
| `MAP_YAML`               | `original_maps/map.yaml`                    | Track map metadata     |
| `RACING_CSV`             | `original_racinglines/input_racingline.csv` | Input raceline         |
| `OUTPUT_MAP`             | `mod_maps/mod_map.png`                      | Generated map for GIMP |
| `FIRST_LAST_POINT_COLOR` | `#f6ff00` (Yellow)                          | Start/end point color  |
| `OTHER_POINTS_COLOR`     | `#ff0000` (Red)                             | Regular point color    |

#### Extractor Configuration

| Parameter             | Default Value                              | Description     |
| --------------------- | ------------------------------------------ | --------------- |
| `MOD_MAP_PATH`        | `mod_maps/mod_map.png`                     | GIMP-edited map |
| `OUTPUT_CSV`          | `output_racinglines/output_racingline.csv` | Final output    |
| `DISCRETIZATION_STEP` | `5`                                        | Path resolution |

#### State Configuration (GIMP Colors)

| State   | Color Code | Usage          |
| ------- | ---------- | -------------- |
| `START` | `#11ff00`  | Starting point |
| `END`   | `#0a00ff`  | Ending point   |
| `PATH`  | `#84367b`  | Path pixels    |

### GIMP Workflow Steps

1. **Generate Visual Map**:

```bash
python -m racingline_drawer.src.drawer
```

2. **Edit in GIMP**:

    - Open `mod_maps/mod_map.png`
    - Use exact hex colors for pixel painting
    - Ensure pixel connectivity (8-directional)
    - Mark start (green), path (purple), end (blue)

3. **Extract Modified Path**:

```bash
python -m path_extractor.src.extractor
```

4. **Verify Results**:
    - Check `output_racinglines/output_racingline.csv`
    - Re-run drawer to visualize changes

## 📊 Data Format

### CSV Structure

```csv
x_coordinate,y_coordinate,velocity
-0.2430698,0.2290873,2.0676071
-0.4212379,0.1221564,2.0178379
...
```

### YAML Map Metadata

```yaml
image: map.png
resolution: 0.05
origin: [-7.5, -5.0, 0.0]
occupied_thresh: 0.65
free_thresh: 0.196
negate: 0
```

## 🐛 Troubleshooting

### GUI Issues

-   **Spline not appearing**: Check if you have at least 3 points and try adjusting smoothness
-   **Points not selectable**: Ensure you're clicking within 15 pixels of a point
-   **Performance issues**: Reduce spline resolution or map size

### GIMP Workflow Issues

-   **Path extraction fails**: Verify pixel connectivity and exact hex colors
-   **Yellow pixel conflicts**: Relocate the first/last point marker
-   **File path errors**: Check configuration paths match your system

### Common Solutions

-   **Dependencies**: Ensure all packages are installed: `pip install -r requirements.txt`
-   **File permissions**: Check read/write access to project directories
-   **Path formats**: Use forward slashes in configuration files

## 🔧 Advanced Configuration

### Custom Colors

Modify `config/config.py` to change visualization colors:

```python
class drawer_config(Enum):
    FIRST_LAST_POINT_COLOR = "#your_color"
    OTHER_POINTS_COLOR = "#your_color"
```

### Performance Tuning

-   **Spline Resolution**: Lower values for better performance
-   **Discretization Step**: Higher values for faster processing
-   **Map Size**: Resize large maps for better GUI performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

[Add license information]

## 👥 Authors & Maintainers

**Original Author:**  
George Halim - georgehany064@gmail.com

**Current Maintainer:**  
Fam Shihata - fam@awadlouis.com  
GitHub: FamALouiz

## 🔗 Related Projects

-   [F1Tenth Gym](https://github.com/f1tenth/f1tenth_gym)
-   [F1Tenth System](https://github.com/f1tenth/f1tenth_system)

---

_For detailed technical documentation and API reference, see the inline code documentation._
