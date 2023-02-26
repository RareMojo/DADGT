import os

import cv2
import mss
import numpy as np
import paths as paths


def take_screenshot(monitor):
    with mss.mss() as sct:
        screenshot = sct.grab(monitor)
        screenshot = np.array(screenshot)
        return screenshot


def grab_edges(minimap):
    # Convert image to grayscale
    gray = cv2.cvtColor(minimap, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detection to extract edges
    edges = cv2.Canny(gray, 250, 350)

    # Dilate the edges to make them more visible
    kernel = np.ones((3, 3), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)

    # Draw the edges on a black background
    output_image = np.zeros_like(minimap)
    output_image[dilated_edges != 0] = (0, 255, 0)

    return output_image


def find_minimap_location(minimap, result):
    # Find the location of the minimap in the map image
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    bottom_right = (top_left[0] + minimap.shape[1] // 2, top_left[1] + minimap.shape[0] // 2)
    # Get the coordinates of the minimap in the map image
    minimap_x, minimap_y = top_left
    minimap_center_x = minimap_x + minimap.shape[1] // 2
    minimap_center_y = minimap_y + minimap.shape[0] // 2
    return minimap_x, minimap_y


def crop_minimap(screenshot):
    # Crop out the minimap from the screenshot
    minimap_x, minimap_y = 2220, 1100
    minimap_width, minimap_height = 300, 300
    minimap = screenshot[minimap_y:minimap_y+minimap_height, minimap_x:minimap_x+minimap_width]
    cv2.imwrite(paths.minimap_path, minimap)
    return minimap


def crop_health_bar(screenshot): # unused, but working
    # Crop out the health bar from the screenshot
    health_x, health_y = 1090, 1324
    health_width, health_height = 382, 25
    health_bar = screenshot[health_y:health_y+health_height, health_x:health_x+health_width]
    cv2.imwrite(paths.health_bar_path, health_bar)
    return health_bar


def crop_compass(screenshot): # unused, but working
    # Crop out the compass from the screenshot
    compass_x, compass_y = 1255, 15
    compass_width, compass_height = 50, 50
    compass = screenshot[compass_y:compass_y+compass_height, compass_x:compass_x+compass_width]
    cv2.imwrite(paths.compass_path, compass)
    return compass


def show_map_location(minimap, minimap_x, minimap_y, map_image):
    # Draw a rectangle around the exact area the minimap is at in the map image
    map_image = map_image.copy()
    cv2.rectangle(map_image, (minimap_x, minimap_y), (minimap_x + minimap.shape[1], minimap_y + minimap.shape[0]), (0, 0, 255), 2)
    # Overlay the minimap inside the red rectangle
    overlay = map_image.copy()
    overlay[minimap_y:minimap_y+minimap.shape[0], minimap_x:minimap_x+minimap.shape[1]] = minimap
    alpha = 0.8
    cv2.addWeighted(overlay, alpha, map_image, 1 - alpha, 0, map_image)
    return map_image


def display_map_info(image, playerName, mapimage_path, minimap_center_x, minimap_center_y, screenshot):
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


def build_map(minimap, map_image, result, mapimage_path, screenshot, playerName):
    # Find the location of the minimap in the map image
    minimap_x, minimap_y = find_minimap_location(minimap, result)
    image = map_image.copy()
    image = show_map_location(minimap, minimap_x, minimap_y, image)
    
    # Compute the center coordinates of the minimap
    minimap_center_x, minimap_center_y = minimap_x + minimap.shape[1] // 2, minimap_y + minimap.shape[0] // 2

    # Display the map location and player info in the screenshot
    image = display_map_info(image, playerName, mapimage_path, minimap_center_x, minimap_center_y, screenshot)
    
    return image