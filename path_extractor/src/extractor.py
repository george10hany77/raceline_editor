from Node import Node
from queue import Queue
from PIL import Image
from state import State
import yaml
import csv
import argparse

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb).lower()

def hex_to_rgb(hex_color):
    """
    Converts a hex color string (e.g. "#00ff00") to an (R, G, B) tuple.
    Accepts optional leading '#' and case-insensitive letters.
    """
    hex_color = hex_color.lstrip('#')  # remove '#' if present
    if len(hex_color) != 6:
        raise ValueError("Hex color must be 6 characters long.")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def extract_pixels(image_path):
    """
    Extracts pixel data from an image and returns it as a list of RGB tuples.
    """
    img = Image.open(image_path).convert("RGB")
    pixels = img.load()
    width, height = img.size
    return pixels, width, height

def find_start_end_positions(pixels, width, height):
    start = end = None
    for y in range(height):
        for x in range(width):
            if rgb_to_hex(pixels[x, y][:3]) == State.START.value:
                start = Node(x, y, state=State.START, parent=None)
            elif rgb_to_hex(pixels[x, y][:3]) == State.END.value:
                end = Node(x, y, state=State.END, parent=None)
    return start, end

def extract_path(start:Node, end:Node, pixels, width, height):
    """
    Extracts the path from start to end using BFS.
    Returns a list of nodes representing the path.
    """
    queue = Queue()
    visited = set()
    visited.add(start)
    start.parent = None
    queue.put(start)
    visited.add(start)
    path_backup_list = []

    while not queue.empty():
        current:Node = queue.get()
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            nx, ny = current.x + dx, current.y + dy
            neighbor = Node(nx, ny)
            if neighbor.x == end.x and neighbor.y == end.y:
                neighbor.parent = current
                path = []
                while neighbor:
                    path.append(neighbor)
                    neighbor = neighbor.parent
                return path[::-1]  # Return reversed path
            if 0 <= nx < width and 0 <= ny < height and neighbor not in visited and rgb_to_hex(pixels[nx, ny][:3]) == State.PATH.value:
                neighbor.parent = current
                queue.put(neighbor)
                visited.add(neighbor)
                path_backup_list.append(neighbor)
    print("No path found, returning []")
    return []  # No path found

# Function to load map metadata from a .yaml file
def load_map_metadata(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        map_data = yaml.safe_load(file)
    resolution = map_data['resolution']
    origin = map_data['origin']  # [x, y, theta]
    return resolution, origin

# Function to convert map pixel coordinates to world coordinates
def pixel_to_world(px, py, resolution, origin):
    origin_x, origin_y, origin_theta = origin
    world_x = px * resolution + origin_x
    world_y = py * resolution + origin_y
    return world_x, world_y

def main():
    """
    Main function to run the path extraction process.
    This function is currently a placeholder and does not perform any operations.
    """

    parser = argparse.ArgumentParser(description="Draw 1-pixel points from CSV onto ROS map image.")
    parser.add_argument("map_png", help="Path to the map PNG file")
    # parser.add_argument("--output", default="output.png", help="Output image path")

    args = parser.parse_args()

    # --- Load image ---
    pixels, width, height = extract_pixels(args.map_png)

    # --- Find start and end positions ---
    start = end = None

    start, end = find_start_end_positions(pixels, width, height)
    if start:
        print(f"Start found at: ({start.x}, {start.y})")
    if end:
        print(f"End found at: ({end.x}, {end.y})")

    if not start or not end:
        raise Exception("Start or end color not found.")
        
    path = extract_path(start, end, pixels, width, height)
    if path:
        print(f"Path found: {len(path)} nodes")
        # discretizing the path
        path = path[::5]  # Example: take every 5th node for simplicity
        print(f"Discretized path: {len(path)} nodes")
        for node in path:
            print(f"Node at ({node.x}, {node.y})")
    else:
        print("No path found from start to end.")

# Example usage
if __name__ == "__main__":
    main()