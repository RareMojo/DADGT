import time

import cv2
import mss
import utility.imageprocessing as impro
import utility.paths as paths
from utility.buildui import build_window
from utility.imageprocessing import (crop_compass, crop_health_bar,
                                     crop_killfeed, crop_match_time,
                                     crop_minimap, grab_edges, take_screenshot)


# DADGT.py
# Currently the main script of the program
"""
This is intended to provide useful information to the player while playing the video game Dark and Darker.
This is not intended to be used for malicious purposes.
It prompts the user to input the monitor number (Game capture), timer interval (Refresh rate of the output), and player name.
First it captures a monitor, crops out specific parts of the screenshot, and processes the minimap to an edge-detected version.
Then it finds the location of the minimap in a set of reference map images that are already edge detected.
If a match is found, the program builds a window with the matching map image (Non-edge detected), a location overlay, and a player info overlay.
It then runs an infinite loop until the user closes the program with ESCAPE or a match is found.
There are some other functions that are not being used at the moment, but they are working.
Thanks to Zero-PAiN, NaakedBushman, kelltom, StuffMadeHereYT, and the DaD developers and community.
This description was last updated on 02/26/2023 by RareMojo. Enjoy!
"""

try:
    # Define the monitor to capture
    monitor_number = int(input("Enter monitor number (0, 1, or 2): "))
    monitors = mss.mss().monitors
    if monitor_number < len(monitors):
        monitor = {"top": monitors[monitor_number]["top"], "left": monitors[monitor_number]["left"], "width": monitors[monitor_number]["width"], "height": monitors[monitor_number]["height"]}
    else:
        print("Invalid monitor number!")
        exit()
    # Define the timer interval used for refresh rate
    timer_interval = int(input("Enter timer interval to output location (in milliseconds): "))
    if timer_interval < 0:
        print("Invalid timer interval!")
        exit()
    # Define player name
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

        # Capture the monitor and return the screenshot as a numpy array
        screenshot = take_screenshot(monitor)

        # Crop out the content from the screenshot, coords are based on 1440p monitor
        minimap = crop_minimap(screenshot)
        health_bar = crop_health_bar(screenshot) # unused, but working
        compass = crop_compass(screenshot) # unused, but working
        killfeed = crop_killfeed(screenshot) # unused, but working
        match_time = crop_match_time(screenshot) # unused, but working

        # Save screenshot croppings to set filepaths
        minimap = cv2.imread(paths.minimap_path)
        health_bar = cv2.imread(paths.health_bar_path) # unused, but working
        compass = cv2.imread(paths.compass_path) # unused, but working
        killfeed = cv2.imread(paths.killfeed_path) # unused, but working
        match_time = cv2.imread(paths.match_time_path) # unused, but working

        # Process the minimap into edge detected version
        minimap_edges = grab_edges(minimap)
        cv2.imwrite(paths.minimap_edges_path, minimap_edges)

         # Find the location of the minimap in the map image reference image
        if successCount > 3:
            result = cv2.matchTemplate(map_edges, minimap_edges, cv2.TM_CCOEFF_NORMED)
            if result.max() < 0.45:
                print(f'Template not found in {map_edges_path}')
                successCount = 0
                continue
                
            # Build a window with the map image, map overlay, and player info overlay
            build_window(minimap, map_image, result, mapimage_path, impro.playerName, "DADGT")
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
                        print(f'Error: template image is larger than search image in {map_edges_path}')
                    elif result.max() < 0.45:
                        print(f'Template not found in {map_edges_path}')
                    else:
                        # Build a window with the map image, map overlay, and player info overlay
                        build_window(minimap, map_image, result, mapimage_path, impro.playerName, "DADGT")
                        successCount += 1
                        match_found = True
                        break

        if not match_found:
            print("No match found in any map image. Trying again...")
        else:
            match_found = False

        #27 is the escape key, when pressed closed program
        if cv2.waitKey(timer_interval) & 0xFF == 27:
            print("User closed the program.")
            break

    cv2.destroyAllWindows()
except Exception as e:
    print (f"Error: {e}")



# LICENSE
"""
Copyright 2023 RareMojo, Zero-PAiN

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""