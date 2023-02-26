import cv2
import mss
import numpy as np


def take_screenshot(monitor):
    with mss.mss() as sct:
        screenshot = sct.grab(monitor)
        screenshot = np.array(screenshot)
        return screenshot


def grab_edges(minimap):
    # Convert image to HSV color space
    hsv = cv2.cvtColor(minimap, cv2.COLOR_BGR2HSV)

    # Define range of black colors to look for
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 30])
    mask = cv2.inRange(hsv, lower_black, upper_black)

    # Find contours of specified color in image
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    output_image = np.zeros_like(minimap)

    # Draw contours on output image
    for cnt in contours:
        cv2.drawContours(output_image, [cnt], 0, (0, 255, 0), 2)

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


def show_map_location(minimap, minimap_x, minimap_y, map_image):
    # Draw a rectangle around the exact area the minimap is at in the map image
    cv2.rectangle(map_image, (minimap_x, minimap_y), (minimap_x + minimap.shape[1], minimap_y + minimap.shape[0]), (0, 0, 255), 2)
    # Overlay the minimap inside the red rectangle
    overlay = map_image.copy()
    overlay[minimap_y:minimap_y+minimap.shape[0], minimap_x:minimap_x+minimap.shape[1]] = minimap
    alpha = 0.6
    cv2.addWeighted(overlay, alpha, map_image, 1 - alpha, 0, map_image)
