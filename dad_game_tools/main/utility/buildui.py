import os

import cv2
from utility.imageprocessing import find_minimap_location


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
    # Find the location of the minimap in the map image to place on the map
    minimap_x, minimap_y = find_minimap_location(minimap, result)
    image = map_image.copy()
    image = show_map_location(minimap, minimap_x, minimap_y, image)
    
    # Compute the center coordinates of the minimap
    minimap_center_x, minimap_center_y = minimap_x + minimap.shape[1] // 2, minimap_y + minimap.shape[0] // 2

    # Display the map location and player info onto the map image
    image = display_map_info(image, playerName, mapimage_path, minimap_center_x, minimap_center_y, screenshot)
    return image