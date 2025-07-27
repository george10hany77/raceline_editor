from enum import Enum
class drawer_config(Enum):
    MAP_YAML = "/home/george/python_files/racingline_editor/original_maps/map.yaml"
    RACING_CSV = "/home/george/python_files/racingline_editor/original_racinglines/csv_path.csv"
    OUTPUT_MAP = "/home/george/python_files/racingline_editor/mod_maps/mod_map.png"
    FIRST_LAST_POINT_COLOR = "#f6ff00"  # Yellow for the first and last points because they are the same
    OTHER_POINTS_COLOR = "#ff0000"  # Red for other points

class extractor_config(Enum):
    MOD_MAP_PATH = "/home/george/python_files/racingline_editor/mod_maps/mod_map.png"
    MAP_YAML = "/home/george/python_files/racingline_editor/original_maps/map.yaml"
    RACING_CSV = "/home/george/python_files/racingline_editor/original_racinglines/csv_path.csv"
    OUTPUT_CSV = "/home/george/python_files/racingline_editor/output_racinglines/oda_kbera_new.csv"
    TEMP_RACING_CSV = "/home/george/python_files/racingline_editor/path_extractor/temp_csvs/temp_racingline.csv"
    DISCRETIZATION_STEP = 5  # Optional discretization step for the path
    NOT_VELOCITY = -999  # Placeholder for velocity

class State(Enum):  # Node state for pathfinding algorithm
    """
    Enum representing the state of a node in a pathfinding algorithm.
    """
    START = "#11ff00"  # Example hex color for start
    END = "#0a00ff"  # Example hex color for end
    PATH = "#84367b"  # Example hex color for path

    def __str__(self):
        return self.name.lower()
