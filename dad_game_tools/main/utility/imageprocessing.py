import os
import cv2
import mss
import numpy as np
from utility.settings import DadgtPaths as paths

base_resolution = (1440, 900)


def grab_ui(monitor: dict):
    """
    Capture the monitor and return the screenshot as a numpy array

    Args: monitor (dict): The monitor to capture
    """
    with mss.mss() as sct:
        screenshot = sct.grab(monitor)
        screenshot = np.array(screenshot)
        minimap = grab_minimap(screenshot)
        match_time = grab_match_time(screenshot)
        killfeed = grab_killfeed(screenshot)
        health_bar = grab_health_bar(screenshot)
        compass = grab_compass(screenshot)
        return minimap, match_time, killfeed, health_bar, compass
    

def grab_minimap(image: np):
    """
    Crop out the minimap from the image

    Args: image (np.ndarray): The image to crop
    """
    # Crop out the minimap from the screenshot, coords are based on 1440p monitor
    ref = base_resolution
    minimap_x, minimap_y = 2230, 1110
    minimap_width, minimap_height = 285, 285

    # Calculate the ratio of the provided image size to the base resolution
    ratio = image.shape[1] / ref[0]

    # Calculate the new coordinates and dimensions based on the ratio
    minimap_x = int(minimap_x * ratio)
    minimap_y = int(minimap_y * ratio)
    minimap_width = int(minimap_width * ratio)
    minimap_height = int(minimap_height * ratio)

    minimap = image[minimap_y:minimap_y+minimap_height, minimap_x:minimap_x+minimap_width]
    cv2.imwrite(paths.minimap_path, minimap)
    return minimap


def grab_match_time(image: np):
    """
    Crop out the match time from the image

    Args: image (np.ndarray): The image to crop
    """
    # Crop out the match time and zone time from the screenshot, coords are based on 1440p monitor
    ref = base_resolution
    match_time_x, match_time_y = 2217, 1067
    match_time_width, match_time_height = 315, 25

    # Calculate the ratio of the provided image size to the base resolution
    ratio = image.shape[1] / ref[0]

    # Calculate the new coordinates and dimensions based on the ratio
    match_time_x = int(match_time_x * ratio)
    match_time_y = int(match_time_y * ratio)
    match_time_width = int(match_time_width * ratio)
    match_time_height = int(match_time_height * ratio)

    match_time = image[match_time_y:match_time_y+match_time_height, match_time_x:match_time_x+match_time_width]
    cv2.imwrite(paths.match_time_path, match_time)
    return match_time


def grab_killfeed(image: np): # unused, but working
    """
    Crop out the killfeed from the image

    Args: image (np.ndarray): The image to crop
    """
    # Crop out the killfeed from the screenshot, coords are based on 1440p monitor
    ref = base_resolution
    killfeed_x, killfeed_y = 1900, 10
    killfeed_width, killfeed_height = 700, 300

    # Calculate the ratio of the provided image size to the base resolution
    ratio = image.shape[1] / ref[0]

    # Calculate the new coordinates and dimensions based on the ratio
    killfeed_x = int(killfeed_x * ratio)
    killfeed_y = int(killfeed_y * ratio)
    killfeed_width = int(killfeed_width * ratio)
    killfeed_height = int(killfeed_height * ratio)

    killfeed = image[killfeed_y:killfeed_y+killfeed_height, killfeed_x:killfeed_x+killfeed_width]
    cv2.imwrite(paths.killfeed_path, killfeed)
    return killfeed

def grab_health_bar(image: np): # unused, but working
    """
    Crop out the health bar from the image

    Args: image (np.ndarray): The image to crop
    """
    # Crop out the health bar from the screenshot, coords are based on 1440p monitor
    ref = base_resolution
    health_x, health_y = 1090, 1324
    health_width, health_height = 382, 25

    # Calculate the ratio of the provided image size to the base resolution
    ratio = image.shape[1] / ref[0]

    # Calculate the new coordinates and dimensions based on the ratio
    health_x = int(health_x * ratio)
    health_y = int(health_y * ratio)
    health_width = int(health_width * ratio)
    health_height = int(health_height * ratio)

    health_bar = image[health_y:health_y+health_height, health_x:health_x+health_width]
    cv2.imwrite(paths.health_bar_path, health_bar)
    return health_bar

def grab_compass(image: np): # unused, but working
    """
    Crop out the compass from the image
    Args: image (np.ndarray): The image to crop

    """
    # Crop out the compass from the screenshot, coords are based on 1440p monitor
    ref = base_resolution
    compass_x, compass_y = 1255, 15
    compass_width, compass_height = 50, 50

    # Calculate the ratio of the provided image size to the base resolution
    ratio = image.shape[1] / ref[0]

    # Calculate the new coordinates and dimensions based on the ratio
    compass_x = int(compass_x * ratio)
    compass_y = int(compass_y * ratio)
    compass_width = int(compass_width * ratio)
    compass_height = int(compass_height * ratio)

    compass = image[compass_y:compass_y+compass_height, compass_x:compass_x+compass_width]
    cv2.imwrite(paths.compass_path, compass)
    return compass

def grab_edges(image: np):
    """
    Process an image into edge detected version

    Args: image (np.ndarray): The image to process
    """
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detection to extract edges
    edges = cv2.Canny(gray, 250, 350)

    # Dilate the edges to make them more visible
    kernel = np.ones((3, 3), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)

    # Draw the edges on a black background
    edge_image = np.zeros_like(image)
    edge_image[dilated_edges != 0] = (0, 255, 0)
    return edge_image

def find_minimap_location(minimap: np, result: np):
    """
    Finds the location of the minimap in the reference image.

    The minimap is found using template matching to locate the minimap within the reference image.

    Args:
        minimap (np.ndarray): The minimap to find in the reference image.
        result (np.ndarray): The result of the template matching.

    Returns:
        A tuple containing the x and y coordinates of the top-left corner of the minimap in the reference image.
    """
    # Find the location of the minimap in the map image, coords are based on 1440p monitor
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    bottom_right = (top_left[0] + minimap.shape[1] // 2, top_left[1] + minimap.shape[0] // 2)
    # Get the coordinates of the minimap in the map image
    minimap_x, minimap_y = top_left
    minimap_center_x = minimap_x + minimap.shape[1] // 2
    minimap_center_y = minimap_y + minimap.shape[0] // 2
    return minimap_x, minimap_y

def display_map_info(image: np, playerName: str, mapimage_path: str, minimap_center_x: int, minimap_center_y: int):
    """
    Displays the map name and player location on the map image.

    The map name and player location are displayed by adding text onto the map image.

    Args:
        image (np.ndarray): The map image.
        playerName (str): The name of the player, set by user input.
        mapimage_path (str): The path to the map image.
        minimap_center_x (int): The x coordinate of the minimap center.
        minimap_center_y (int): The y coordinate of the minimap center.

    Returns:
        The map image with the player location and map name displayed.
    """
    # get the mapimage_path without the directory path and extension
    filename = os.path.basename(mapimage_path)
    map_found = os.path.splitext(filename)[0].capitalize().replace('_', ' ')
    log = f'{playerName} located in {map_found} at x={minimap_center_x}, y={minimap_center_y}'
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    thickness = 1
    color = (0, 255, 0)
    org = (10, 30)
    image = cv2.putText(image, log, org, font, font_scale, color, thickness, cv2.LINE_AA)
    return image