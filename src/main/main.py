import cv2
import numpy as np
import mss
import paths as paths
import time
from imageprocessing import *
import os


try:
    # Define the monitor to capture
    monitor_number = int(input("Enter monitor number (0, 1, or 2): "))
    monitors = mss.mss().monitors
    if monitor_number < len(monitors):
        monitor = {"top": monitors[monitor_number]["top"], "left": monitors[monitor_number]["left"], "width": monitors[monitor_number]["width"], "height": monitors[monitor_number]["height"]}
    else:
        print("Invalid monitor number!")
        exit()
    timer_interval = int(input("Enter timer interval to output location (in milliseconds): "))
    if timer_interval < 0:
        print("Invalid timer interval!")
        exit()

    # Initialize the timer
    timer_start = time.time()
    match_found = False
    while True:
        elapsed_time = time.time() - timer_start

        screenshot = take_screenshot(monitor)

        # Crop out the minimap from the screenshot
        minimap_x, minimap_y = 2220, 1100
        minimap_width, minimap_height = 300, 300
        minimap = screenshot[minimap_y:minimap_y+minimap_height, minimap_x:minimap_x+minimap_width]

        cv2.imwrite(paths.minimap_path, minimap)
        minimap = cv2.imread(paths.minimap_path)
        minimap_edges = grab_edges(minimap)
        cv2.imwrite(paths.minimap_edges_path, minimap_edges)

        # Loop through all map images until a match is found
        for mapimage_path, map_edges_path in zip(paths.mapimage_paths, paths.map_edges_paths):
            # Load the map image
            map_image = cv2.imread(mapimage_path)
            map_edges = cv2.imread(map_edges_path)

            # Check if the map image was loaded successfully
            if map_edges is None:
                print(f'Error: could not load {mapimage_path}')
            else:
                # Find the location of the minimap in the map image
                result = cv2.matchTemplate(map_edges, minimap_edges, cv2.TM_CCOEFF_NORMED)

                # Check for errors
                if result is None:
                    print(f'Error: template image is larger than search image in {mapimage_path}')
                elif result.max() < 0.45:
                    print(f'Template not found in {mapimage_path}')
                else:
                    # Find the location of the minimap in the map image
                    minimap_x, minimap_y = find_minimap_location(minimap, result)

                    show_map_location(minimap, minimap_x, minimap_y, map_image)

                    # Compute the center coordinates of the minimap
                    minimap_center_x, minimap_center_y = minimap_x + minimap.shape[1] // 2, minimap_y + minimap.shape[0] // 2
                    # get the mapimage_path without the directory path and extension
                    filename = os.path.basename(mapimage_path)
                    map_found = os.path.splitext(filename)[0].capitalize().replace('_', ' ')
                    log = f'Player located in {map_found} at x={minimap_center_x}, y={minimap_center_y}'
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.5
                    thickness = 1
                    color = (0, 255, 0)
                    org = (10, 30)
                    map_image = cv2.putText(map_image, log, org, font, font_scale, color, thickness, cv2.LINE_AA)
                    cv2.imshow("DaD Minimap Locator", map_image)
                    match_found = True
                    break

        if not match_found:
            print("No match found in any map image. Trying again in 3 seconds...")
            time.sleep(3)
        else:
            match_found = False

        #27 is the escape key
        if cv2.waitKey(timer_interval) & 0xFF == 27:
            print("User closed the program.")
            break

    cv2.destroyAllWindows
except Exception as e:
    print (f"Error: {e}")