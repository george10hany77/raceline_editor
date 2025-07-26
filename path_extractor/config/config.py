from enum import Enum

class extractor_config(Enum):
    MAP_PATH = "/home/george/python_files/racingline_editor/mod_maps/mod_map.png"
    MAP_YAML = "/home/george/python_files/racingline_editor/original_maps/map.yaml"
    RACING_CSV = "/home/george/python_files/racingline_editor/original_racinglines/csv_path.csv"
    OUTPUT_CSV = "/home/george/python_files/racingline_editor/output_racinglines/oda_kbera_new.csv"
    DISCRETIZATION_STEP = 5  # Optional discretization step for the path

class State(Enum):
    """
    Enum representing the state of a node in a pathfinding algorithm.
    """
    START = "#74367b"  # Example hex color for start
    END = "#94367b"  # Example hex color for end
    PATH = "#84367b"  # Example hex color for path

    def __str__(self):
        return self.name.lower()
