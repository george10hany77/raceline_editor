from path_extractor.src.Node import Node
from queue import Queue
from PIL import Image
import yaml
import csv
import argparse
from config.config import extractor_config, State, drawer_config
from math import hypot
import shutil

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

def find_starts_positions(pixels, width, height):
    starts = []
    for y in range(height):
        for x in range(width):
            if rgb_to_hex(pixels[x, y][:3]) == State.START.value:
                starts.append(Node(x, y, state=State.START, parent=None))
    return starts

def extract_path_dfs(start: Node, end: Node, pixels, width, height):
    """
    Extracts the path from start to end using DFS.
    Returns a list of nodes representing the path.
    """
    stack = [start]
    visited = set()
    visited.add(start)
    start.parent = None

    while stack:
        current: Node = stack.pop()
        if current.x == end.x and current.y == end.y:
            # Reconstruct path
            path = []
            node = current
            while node:
                path.append(node)
                node = node.parent
            return path[::-1]  # Return reversed path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            nx, ny = current.x + dx, current.y + dy
            neighbor = Node(nx, ny)
            if (
                0 <= nx < width and
                0 <= ny < height and
                neighbor not in visited and
                rgb_to_hex(pixels[nx, ny][:3]) == State.PATH.value
            ):
                neighbor.parent = current
                stack.append(neighbor)
                visited.add(neighbor)
    print("No path found, returning []")
    return []  # No path found

def extract_path_bfs(start:Node, pixels, width, height):
    """
    Extracts the path from start to end using BFS.
    Returns a list of nodes representing the path.
    It only uses the start node and the end node will be found after the bfs.
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
            if rgb_to_hex(pixels[nx, ny][:3]) == State.END.value:
                neighbor.parent = current # The neighbor is the end node
                end = neighbor
                print(f"End found at: ({end.x}, {end.y})")
                path = []
                while neighbor:
                    path.append(neighbor)
                    neighbor = neighbor.parent
                return path[::-1], end  # Return reversed path
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


def load_racing_line_pixels(csv_path, origin, resolution, height):
    racing_line_pixels = []
    original_racing_line_world = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                x_world = float(row[0])
                y_world = float(row[1])
                v_world = float(row[2]) if len(row) > 2 else 0.0  # Optional velocity
                px = int((x_world - origin[0]) / resolution)
                py = height - int((y_world - origin[1]) / resolution)
                racing_line_pixels.append((px, py))
                original_racing_line_world.append((x_world, y_world, v_world))  # keep for saving
    return racing_line_pixels, original_racing_line_world

def dist(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

def find_nearest_indices(start, end, racing_line_pixels):
    start_idx = min(range(len(racing_line_pixels)), key=lambda i: dist((start.x, start.y), racing_line_pixels[i]))
    end_idx = min(range(len(racing_line_pixels)), key=lambda i: dist((end.x, end.y), racing_line_pixels[i]))
    return sorted([start_idx, end_idx])

def convert_path_to_world_coordinates(path, resolution, origin, height):
        # Replace segment
    path_pixels = [(node.x, node.y) for node in path]

    # Convert new segment back to world (map) coordinates
    path_world = []
    for px, py in path_pixels:
        wx = px * resolution + origin[0]
        wy = (height - py) * resolution + origin[1]
        path_world.append((round(wx, 7), round(wy, 7), extractor_config.NOT_VELOCITY.value))  # Use NOT_VELOCITY as placeholder for velocity
    return path_world

def save_modified_path_to_csv(modified_path, output_csv_path):
    # Save to CSV
    with open(output_csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        for point in modified_path:
            writer.writerow(point)
    print(f"Saved modified racing line to: {output_csv_path}")

def fix_missing_velocities(new_csv_path, original_csv_path, output_csv_path, distance_threshold=10.0):
    """
    Replace NOT_VELOCITY velocity values in new_csv with values from original_csv by matching (x, y) coordinates.
    """

    # Load original CSV into memory
    original_data = []
    with open(original_csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 3:
                x, y, v = float(row[0]), float(row[1]), float(row[2])
                original_data.append((x, y, v))

    # Process new CSV
    fixed_data = []
    with open(new_csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3:
                continue
            x_new, y_new, v_new = float(row[0]), float(row[1]), float(row[2])
            if v_new == extractor_config.NOT_VELOCITY.value:
                # Find the closest point in original_data
                closest = min(original_data, key=lambda p: hypot(p[0] - x_new, p[1] - y_new))
                if hypot(closest[0] - x_new, closest[1] - y_new) <= distance_threshold:
                    v_new = closest[2]  # Replace missing value
                else:
                    print(f"Warning: No nearby match found for point ({x_new}, {y_new})")
            fixed_data.append((x_new, y_new, v_new))

    # Save to output CSV
    with open(output_csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in fixed_data:
            writer.writerow(row)

    print(f"Fixed CSV saved to {output_csv_path}")

def find_first_point(pixels, width, height):
    """
    Find the first point in the image that matches the START color.
    Returns a Node with the coordinates of the first point found.
    The pixels are from the modified image.
    """
    for y in range(height):
        for x in range(width):
            if rgb_to_hex(pixels[x, y][:3]) == drawer_config.FIRST_LAST_POINT_COLOR.value:
                return Node(x, y, state=State.START, parent=None)
    return None  # No start point found

def find_nearest_index_to_first_point(racingline_pixels, first_point):
    """
    Find the index of the nearest point in racing_line_pixels to the first point.
    """
    return min(range(len(racingline_pixels)), key=lambda i: dist((first_point.x, first_point.y), racingline_pixels[i]))

def rotate_racing_line_to_first_point_and_save_it_in_csv_racingline(original_racing_line_world, nearest_index, output_csv_path):
    """
    Rotates the racing line so it starts from the nearest point and updates the CSV.
    """
    rotated = original_racing_line_world[nearest_index:] + original_racing_line_world[:nearest_index]
    rotated.append(rotated[0])  # Close the loop
    with open(output_csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        for point in rotated:
            writer.writerow(point)
    print(f"Updated racing line CSV with rotated line starting from nearest point: {nearest_index}")


def main():
    # Copy the racingline CSV to the temp path
    shutil.copy(extractor_config.RACING_CSV.value, extractor_config.TEMP_RACING_CSV.value)
    print(f"Copied {extractor_config.RACING_CSV.value} to {extractor_config.TEMP_RACING_CSV.value}")
    
    # Load image and metadata
    pixels, width, height = extract_pixels(extractor_config.MOD_MAP_PATH.value)
    resolution, origin = load_map_metadata(extractor_config.MAP_YAML.value)

    # Convert racing line from map (meters) to image pixels
    racing_line_pixels, original_racing_line_world = load_racing_line_pixels(
        extractor_config.TEMP_RACING_CSV.value, origin, resolution, height
    )

    first_point = find_first_point(pixels, width, height)
    if not first_point:
        raise Exception("First point not found in the image.")
    print(f"First point found at: ({first_point.x}, {first_point.y})")
    # Find the nearest index to the first point in the racing line
    nearest_index = find_nearest_index_to_first_point(racing_line_pixels, first_point)
    print(f"Nearest index to first point in racing line: {nearest_index}")

    # Rotate the original racing line to start from the nearest point
    rotate_racing_line_to_first_point_and_save_it_in_csv_racingline(
        original_racing_line_world,
        nearest_index,
        extractor_config.TEMP_RACING_CSV.value
    )

    # Find start and end positions in the image
    starts = find_starts_positions(pixels, width, height)
    ends = []
    if not starts:
        raise Exception("Start color not found.")
    for start in starts:
        print(f"Start found at: ({start.x}, {start.y})")
    ##############################################
    for start in starts:
    # Generate path using BFS
        path, end = extract_path_bfs(start, pixels, width, height)
        ends.append(end)
        if not path:
            print("No path found.")
            return
        print(f"Generated path length: {len(path)}")
        path = path[::extractor_config.DISCRETIZATION_STEP.value]  # Optional discretization
        print(f"Discretized path length: {len(path)}")

        # Convert racing line from map (meters) to image pixels
        racing_line_pixels, original_racing_line_world = load_racing_line_pixels(
            extractor_config.TEMP_RACING_CSV.value, origin, resolution, height
        )

        # Find nearest racing points to start and end
        i1, i2 = find_nearest_indices(start, end, racing_line_pixels)

        print(f"Replacing CSV segment from index {i1} to {i2} (inclusive)")

        # Convert path to world coordinates
        path_world = convert_path_to_world_coordinates(path, resolution, origin, height)

        if dist(original_racing_line_world[i1], path_world[0]) > dist(original_racing_line_world[i1], path_world[-1]):
            path_world.reverse()
            print("Reversed path to match original racing line direction.")

        for (px, py, v) in path_world:
            print(f"New point: ({px}, {py}, {v} )")

        # Final modified path
        modified_path = original_racing_line_world[:i1] + path_world + original_racing_line_world[i2+1:]
        # Save to CSV
        save_modified_path_to_csv(modified_path, extractor_config.TEMP_RACING_CSV.value)
    ##############################################

    # Fix missing velocities
    fix_missing_velocities(
        extractor_config.TEMP_RACING_CSV.value,
        extractor_config.RACING_CSV.value,
        extractor_config.OUTPUT_CSV.value
    )
# Example usage
if __name__ == "__main__":
    main()