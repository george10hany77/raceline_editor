from Node import Node
from queue import Queue
from PIL import Image
from state import State
import yaml
import csv

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

def extract_path(start, end, pixels, width, height):
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
            if end:
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
    print("No path found, returning backup list of nodes.")
    return path_backup_list  # No path found

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

def path_to_csv(path, yaml_file_path):
    # Replace with your actual list of (px, py) or load from a CSV if needed
    racingline_pixel = path

    # Path to your ROS 2 .yaml map file
    yaml_file = yaml_file_path
    resolution, origin = load_map_metadata(yaml_file)

    # Convert pixel coords to world coords
    racingline_world = []
    for node in racingline_pixel:
        wx, wy = pixel_to_world(node.x, node.y, resolution, origin)
        racingline_world.append((wx, wy))

    # Path to output CSV file
    output_csv = "racingline_world.csv"

    # Save world coordinates to CSV
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x', 'y'])  # Header
        for x, y in racingline_world:
            writer.writerow([x, y])

    print(f"✅ Racing line saved to {output_csv}")

def main():
    """
    Main function to run the path extraction process.
    This function is currently a placeholder and does not perform any operations.
    """
    # --- Load image ---
    pixels, width, height = extract_pixels("/home/george/python_files/path_extractor/map.png")

    # --- Find start and end positions ---
    start = end = None

    start, end = find_start_end_positions(pixels, width, height)
    if start:
        print(f"Start found at: ({start.x}, {start.y})")
    if end:
        print(f"End found at: ({end.x}, {end.y})")

    if not start or not end:
        # raise Exception("Start or end color not found.")
        Warning("Start or end color not found, proceeding with available nodes.")
        
    path = extract_path(start, end, pixels, width, height)
    if path:
        print(f"Path found: {len(path)} nodes")
        for node in path:
            print(f"Node at ({node.x}, {node.y})")
        path_to_csv(path, "/home/george/python_files/path_extractor/map.yaml")
    else:
        print("No path found from start to end.")

# Example usage
if __name__ == "__main__":
    main()