import cv2
import pandas as pd
import argparse
import os
import yaml
import numpy as np
from scipy.interpolate import splprep, splev

def load_map_metadata(yaml_path):
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)

    image_path = os.path.join(os.path.dirname(yaml_path), data['image'])
    resolution = data['resolution']
    origin = data['origin']
    return image_path, resolution, origin

def world_to_image_coords(x, y, origin, resolution, image_height):
    origin_x, origin_y = origin[0], origin[1]
    pixel_x = int((x - origin_x) / resolution)
    pixel_y = image_height - int((y - origin_y) / resolution)
    return pixel_x, pixel_y

def draw_spline_on_map(map_yaml_path, csv_path, output_path="output.png", point_color=(0, 0, 255)):
    image_path, resolution, origin = load_map_metadata(map_yaml_path)

    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    height, width = image.shape[:2]

    coords = pd.read_csv(csv_path, header=None).dropna()
    if coords.shape[1] < 2:
        raise ValueError("CSV must have at least two columns")

    x = coords[0].to_numpy()
    y = coords[1].to_numpy()

    if len(x) < 4:
        raise ValueError("Need at least 4 points for cubic spline")

    # Fit spline to points
    tck, _ = splprep([x, y], s=0.0, k=3)
    u_fine = np.linspace(0, 1, num=1000)
    x_fine, y_fine = splev(u_fine, tck)

    # Draw 1-pixel wide line
    for xw, yw in zip(x_fine, y_fine):
        px, py = world_to_image_coords(xw, yw, origin, resolution, height)
        if 0 <= px < width and 0 <= py < height:
            image[py, px] = point_color

    cv2.imwrite(output_path, image)
    print(f"Saved smoothed spline path to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Draw a spline-smoothed racing line on a ROS map image.")
    parser.add_argument("map_yaml", help="Path to the map YAML file")
    parser.add_argument("csv_path", help="CSV file with x,y points in map frame")
    parser.add_argument("--output", default="output.png", help="Output image path")

    args = parser.parse_args()
    draw_spline_on_map(args.map_yaml, args.csv_path, args.output)
