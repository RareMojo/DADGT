import os
import time

import cv2
import imageprocessing as impro
import mss
import numpy as np
import paths as paths
from imageprocessing import *

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
    impro.playerName = str(input("Enter player name: "))
    if len(impro.playerName) < 0:
        print("Invalid player name!")
        exit()

    # Initialize the timer
    timer_start = time.time()
    match_found = False
    successCount = 0
    while True:
        elapsed_time = time.time() - timer_start

        screenshot = take_screenshot(monitor)
        health_bar = crop_health_bar(screenshot) # unused, but working
        compass = crop_compass(screenshot) # unused, but working
        minimap = crop_minimap(screenshot)

        # Set file paths
        minimap = cv2.imread(paths.minimap_path)
        health_bar = cv2.imread(paths.health_bar_path) # unused, but working
        compass = cv2.imread(paths.compass_path) # unused, but working
        minimap_edges = grab_edges(minimap)
        health_bar_edges = grab_edges(health_bar)
        cv2.imwrite(paths.minimap_edges_path, minimap_edges)

        if successCount > 3:
            result = cv2.matchTemplate(map_edges, minimap_edges, cv2.TM_CCOEFF_NORMED)
            if result.max() < 0.45:
                print(f'Template not found in {mapimage_path}')
                successCount = 0
                continue
                
            image = build_map(minimap, map_image, result, mapimage_path, screenshot, impro.playerName)
            cv2.imshow("DaD Minimap Locator", image)
            match_found = True

        else:
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
                        image = build_map(minimap, map_image, result, mapimage_path, screenshot, impro.playerName)
                        cv2.imshow("DaD Minimap Locator", image)
                        successCount += 1
                        match_found = True
                        break

        if not match_found:
            print("No match found in any map image. Trying again...")
        else:
            match_found = False

        #27 is the escape key
        if cv2.waitKey(timer_interval) & 0xFF == 27:
            print("User closed the program.")
            break

    cv2.destroyAllWindows()
except Exception as e:
    print (f"Error: {e}")