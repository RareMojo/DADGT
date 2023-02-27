import cv2
import mss
import numpy as np
import utility.paths as paths


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


def crop_minimap(screenshot):
    # Crop out the minimap from the screenshot
    minimap_x, minimap_y = 2220, 1100
    minimap_width, minimap_height = 300, 300
    minimap = screenshot[minimap_y:minimap_y+minimap_height, minimap_x:minimap_x+minimap_width]
    cv2.imwrite(paths.minimap_path, minimap)
    return minimap


def crop_match_time(screenshot):
    # Crop out the match time and zone time from the screenshot
    match_time_x, match_time_y = 2217, 1067
    match_time_width, match_time_height = 315, 25
    match_time = screenshot[match_time_y:match_time_y+match_time_height, match_time_x:match_time_x+match_time_width]
    cv2.imwrite(paths.match_time_path, match_time)
    return match_time


def crop_killfeed(screenshot): # unused, but working
    # Crop out the killfeed from the screenshot
    killfeed_x, killfeed_y = 1900, 10
    killfeed_width, killfeed_height = 700, 300
    killfeed = screenshot[killfeed_y:killfeed_y+killfeed_height, killfeed_x:killfeed_x+killfeed_width]
    cv2.imwrite(paths.killfeed_path, killfeed)
    return killfeed


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