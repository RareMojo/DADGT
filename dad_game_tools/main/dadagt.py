import concurrent.futures
import threading
import time

import cv2
import mss
import numpy as np
import utility.debug as debug
import utility.paths as paths
from controller.empty_controller import EmptyController
from settings import Settings
from utility.imageprocessing import (crop_compass, crop_health_bar,
                                     crop_killfeed, crop_match_time,
                                     crop_minimap, find_minimap_location,
                                     grab_edges, take_screenshot)


class Dadgt:
    def __init__(self, controller, settings):
        self.settings = settings
        self.controller = controller
        self.log_path = paths.log_path
        self.log_file = open(self.log_path, "a")
        self.clear_log()
        self.log_msg("DADGT-App initialized!")
        self.event_end = threading.Event() # Closing event, ends thread
        self.executor = ""
        self.callback = None
        self.window_name = "Map"
        # # Webtalk stuff
        # self.current_map = ""
        # self.socket = playersocket
        # self.socket.lobby = self.lobbyCode
        #  if self.socket.lobby:
        #      self.socket.start("http://bmbros.sytes.net:5001/lobby")
        self.log_msg("DADGT initialized!")

    def start(self):
        """
        Starts DADGT, usually called from controller through DADGT-App.
        """
        self.event_end.clear()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self.clear_log()
        self.log_msg("Dadgt started!")
        self.get_settings()
        self.main()

    def stop(self):
        """
        Stops DADGT, usually called from controller through DADGT-App.
        """
        if self.executor != "":
            self.log_msg("Dadgt stopped!")
            self.executor.shutdown(wait=False, cancel_futures=True)
            self.executor = ""
        self.log_file.close()
        self.event_end.set()
        self.window_name = self.window_name + " "
    
    def log_msg(self, msg: str, overwrite=False):
        """
        Used to log messages from DADGT to the log file, and to the gui.
        """
        # Create the log message with a timestamp
        log_msg = f"{debug.current_time()}: {msg}"
        # Write the log message to the log file
        with open(self.log_path, "a") as f:
            f.write(log_msg + "\n")
        # Call the update_log method of the gui instance
        self.controller.update_log()

    def clear_log(self):
        """
        Clears the log file
        """
        self.log_file.close()
        self.log_file = open(self.log_path, "w")
        self.log_file.close()
        self.log_file = open(self.log_path, "a")

    def get_settings(self):
        """
        Get settings from the settings class.
        This can be default values or ones set by the user at DADGT-App.
        """
        self.playerName = self.settings.get_player_name()
        self.lobbyCode = self.settings.get_lobby_code()
        self.serverName = self.settings.get_server_name()
        self.monitorNumber = self.settings.get_monitor_number()
        self.timerInterval = self.settings.get_timer_interval()
        self.log_msg(f"Settings updated: {self.playerName}, {self.lobbyCode}, {self.serverName}, {self.monitorNumber}, {self.timerInterval}")

    def main(self):
        """
        Main function of the DADGT, this is where the magic happens.
        Uses Settings class to get the variables necessary to run.
        Launched from the DADGT-App.
        For headless mode, use this file and see last line.
        """
        # Define the monitor to capture
        monitor_number = self.monitorNumber
        monitors = mss.mss().monitors
        if monitor_number < len(monitors):
            monitor = {"top": monitors[monitor_number]["top"], "left": monitors[monitor_number]["left"], "width": monitors[monitor_number]["width"], "height": monitors[monitor_number]["height"]}
        else:
            self.log_msg("Invalid monitor number!")
            exit()
        # Define the timer interval used for refresh rate
        if self.timerInterval < 0:
            self.log_msg("Invalid timer interval!")
            exit()

        # Initialize the timer
        match_found = False
        successCount = 0
        while not self.event_end.is_set():
            try:
                # Capture the monitor and return the screenshot as a numpy array
                self.log_msg(f'Taking screenshot for monitor {monitor_number}...')
                screenshot = take_screenshot(monitor)
                self.log_msg('Screenshot taken.')
            except Exception as e:
                self.log_msg("Screenshot error!")
                self.log_msg(e)

            # Crop out the content from the screenshot, coords are based on 1440p monitor
            self.log_msg('Cropping screenshot...')
            minimap = crop_minimap(screenshot)
            health_bar = crop_health_bar(screenshot) # unused, but working
            compass = crop_compass(screenshot) # unused, but working
            killfeed = crop_killfeed(screenshot) # unused, but working
            match_time = crop_match_time(screenshot) # unused, but working
            self.log_msg('Screenshot cropped.')

            # Save screenshot croppings to set filepaths
            self.log_msg('Saving and setting filepaths...')
            minimap = cv2.imread(paths.minimap_path)
            health_bar = cv2.imread(paths.health_bar_path) # unused, but working
            compass = cv2.imread(paths.compass_path) # unused, but working
            killfeed = cv2.imread(paths.killfeed_path) # unused, but working
            match_time = cv2.imread(paths.match_time_path) # unused, but working
            self.log_msg('Images saved and paths set.')
            
            # Process the minimap into edge detected version
            self.log_msg('Processing minimap...')
            minimap_edges = grab_edges(minimap)
            cv2.imwrite(paths.minimap_edges_path, minimap_edges)
            self.log_msg('Minimap processed.')
            
            # Find the location of the minimap in the map image reference image
            if successCount > 2:
                self.log_msg(f'Player found!')
                result = cv2.matchTemplate(map_edges, minimap_edges, cv2.TM_CCOEFF_NORMED)
                if result.max() < 0.45:
                    self.log_msg(f'Trying to find player location...')
                    successCount = 0
                    continue

                self.log_msg('Showing map...')    
                self.current_map = self.__show_map_location(minimap, map_image, result)
                time.sleep(self.timerInterval)

                if self.executor != "":
                    self.executor.submit(process, self)
                    self.log_msg('Map shown.')

            else:
                # Loop through all map images until a match is found
                self.log_msg(f'Trying to locate player, attempt {successCount}...')
                for mapimage_path, map_edges_path in zip(paths.mapimage_paths, paths.map_edges_paths):
                    # Load the map image
                    map_image = cv2.imread(mapimage_path)
                    map_edges = cv2.imread(map_edges_path)
                    
                    # Check if the map image was loaded successfully
                    if map_edges is None:
                        self.log_msg(f'Error: unable figure out the map...')
                    else:
                        # Find the location of the minimap in the map image
                        result = cv2.matchTemplate(map_edges, minimap_edges, cv2.TM_CCOEFF_NORMED)

                        # Check for errors
                        if result is None:
                            self.log_msg(f'Error: template image is larger than search image in {map_edges_path}...')
                        elif result.max() < 0.45:
                            self.log_msg(f'Player not found...')
                            continue

                        self.current_map = self.__show_map_location(minimap, map_image, result)

                        if self.executor != "":
                            self.executor.submit(process, self)
                            self.log_msg('Map shown.')

                        successCount += 1
                        match_found = True
                        time.sleep(self.timerInterval)
                        break

            if not match_found:
                self.log_msg("No match found in any map image. Trying again...")
                match_found = False
                time.sleep(self.timerInterval)

    def __show_map_location(self, minimap: np, map_image: np, result: np):
        """
        Used to show the player's location on the map, produces the final image to display.
        This is a private method and should not be called directly.
        """
        # Find the location of the minimap in the map image to place on the map
        minimap_x, minimap_y = find_minimap_location(minimap, result)
        image = map_image.copy()
        
        # Compute the center coordinates of the minimap
        minimap_center_x, minimap_center_y = minimap_x + minimap.shape[1] // 2, minimap_y + minimap.shape[0] // 2
        try:
            # Send center coordinates to web api
            self.socket.send_info({"player": self.playerName, "position": [minimap_center_x,minimap_center_y], "map": "test_location"})
        except Exception as e:
            self.log_msg("Disconnected from api.")
            self.log_msg(e)

        # Copy the map image to draw on
        map_image = map_image.copy()

        # Draw a circle around the center of the player's minimap location
        cv2.circle(map_image, (minimap_x + minimap.shape[1]//2, minimap_y + minimap.shape[0]//2), 140, (170, 30, 80), 2)

        # Overlay the minimap inside the circle
        minimap_final = map_image.copy()
        minimap_final[minimap_y:minimap_y+minimap.shape[0], minimap_x:minimap_x+minimap.shape[1]] = minimap
        alpha = 0.65
        cv2.addWeighted(minimap_final, alpha, map_image, 1 - alpha, 0, map_image)
        return map_image

def process(self):
    """
    Seperate process to show the map itself, supoposed to be for testing purposes.
    """
    try:
        cv2.imshow(self.window_name, self.current_map)
        cv2.waitKey(1) 
    except Exception as e:
        self.log_msg(e)


#  For testing purposes, run this file to start the program without UI
if __name__ == '__main__':
    settings = Settings()
    dadgt = Dadgt(controller= EmptyController(), settings=settings)
    dadgt.controller = EmptyController()
    dadgt.start()
