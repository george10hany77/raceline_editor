#!/usr/bin/env python3
"""
F1Tenth Raceline Editor GUI Launcher
=====================================

This script launches the GUI application for editing F1Tenth racing lines.

Usage:
    python main.py

Features:
- Interactive point editing with drag and drop
- Real-time 3D cubic spline visualization
- Zoom and pan functionality
- Save/load raceline files
- Visual map overlay

Requirements:
- Python 3.6+
- Required packages: see requirements.txt
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def main():
    try:
        from gui.raceline_editor_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Error importing GUI: {e}")
        print("Please ensure all required packages are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
