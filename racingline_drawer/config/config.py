from enum import Enum
class drawer_config(Enum):
    MAP_YAML = "/home/george/python_files/racingline_editor/original_maps/map.yaml"
    RACING_CSV = "/home/george/python_files/racingline_editor/original_racinglines/csv_path.csv"
    OUTPUT_MAP = "/home/george/python_files/racingline_editor/mod_maps/mod_map.png"
    FIRST_LAST_POINT_COLOR = "#f6ff00"  # Yellow for the first and last points because they are the same
    OTHER_POINTS_COLOR = "#ff0000"  # Red for other points