import json
import os
from controller.dadgt_controller import DadgtController


class Settings:
    """
    Settings class for the dadgtapp to save and load settings for dadgt
    """
    def __init__(self):
        # Default settings
        self.monitorNumber = 1
        self.timerInterval = 0.5
        self.playerName = "Player"
        self.lobbyCode = "1234"
        self.serverName = "localhost"
        self.load_config()

# SETTERS
    def set_monitor_number(self, number):
        self.monitorNumber = number

    def set_timer_interval(self, interval):
        self.timerInterval = interval
    
    def set_player_name(self, name):
        self.playerName= name

    def set_lobby_code(self, code):
        self.lobbyCode = code

    def set_server_name(self, name):
        self.serverName = name

# GETTERS
    def get_monitor_number(self):
        return self.monitorNumber
    
    def get_timer_interval(self):
        return self.timerInterval
    
    def get_player_name(self):
        return self.playerName
    
    def get_lobby_code(self):
        return self.lobbyCode
    
    def get_server_name(self):
        return self.serverName

    # LOAD AND SAVE CONFIG
    def save_config(self):
        config= {
            "monitorNumber": self.monitorNumber,
            "timerInterval": self.timerInterval,
            "playerName": self.playerName,
            "lobbyCode": self.lobbyCode,
            "serverName": self.serverName,
        }
        with open(DadgtPaths.config_path, "w") as f:
            f.write(json.dumps(config, indent=4))

    # RESETS CONFIG TO DEFAULT
    def reset_config(self):
        config= {
            "monitorNumber": 1,
            "timerInterval": 0.1,
            "playerName": "Player",
            "lobbyCode": "1234",
            "serverName": "localhost",
        }
        with open(DadgtPaths.config_path, "w") as f:
            f.write(json.dumps(config, indent=4))
    
    # LOADS CONFIG FROM CONFIG.JSON
    def load_config(self):
        try:
            with open(DadgtPaths.config_path, "r") as f:
                config = json.load(f)

            if "monitorNumber" in config:
                self.monitorNumber = config["monitorNumber"]
            if "timerInterval" in config:
                self.timerInterval = config["timerInterval"]
            if "playerName" in config:
                self.playerName = config["playerName"]
            if "lobbyCode" in config:
                self.lobbyCode = config["lobbyCode"]
            if "serverName" in config:
                self.serverName = config["serverName"]
        except FileNotFoundError:
            pass
    

class DadgtPaths:
    """
    File paths for dadgt
    """
    path = os.path.dirname(os.path.abspath(__file__))

    # LOGS PATHS
    #------------------------------------------------------------
    log_path = os.path.join(path, '..', 'utility', 'logs', 'log.txt')
    latest_log_path = os.path.join(path, '..', 'utility', 'logs', 'latest_log.txt')
    debug_log_path = os.path.join(path, '..', 'utility', 'logs', 'debug.log')

    # CONFIG PATHS
    #------------------------------------------------------------
    config_path = os.path.join(path, '..', 'utility', 'config', 'config.json')


    # ASSETS PATHS
    #------------------------------------------------------------
    # CAPTURES
    # Screenshot of game window
    screenshot_path = os.path.join(path, '..', 'assets', 'captures', 'screenshot.png')
    # Cropped images from screenshots
    health_bar_path = os.path.join(path, '..', 'assets', 'captures', 'health_bar.png')
    compass_path = os.path.join(path, '..', 'assets', 'captures', 'compass.png')
    killfeed_path = os.path.join(path, '..', 'assets', 'captures', 'killfeed.png')
    match_time_path = os.path.join(path, '..', 'assets', 'captures', 'match_time.png')
    minimap_path = os.path.join(path, '..', 'assets', 'captures', 'minimap.png')
    # Final image
    current_map_path = os.path.join(path, '..', 'assets', 'captures', 'current_map.png')

    # INTERFACE
    outline_image_path = os.path.join(path, '..', 'assets', 'interface', 'outline.png')
    standby_image_path = os.path.join(path, '..', 'assets', 'interface', 'standby.png')
    icon_png_path = os.path.join(path, '..', 'assets', 'interface', 'dadgt_icon.png')
    icon_ico_path = os.path.join(path, '..', 'assets', 'interface', 'dadgt_icon.ico')
    about_txt_path = os.path.join(path, '..', 'assets', 'interface', 'about.txt')
    credits_txt_path = os.path.join(path, '..', 'assets', 'interface', 'credits.txt')

    # MAPS
    # Normal unprocessed maps
    mapimage_paths = [
        os.path.join(path, '..', 'assets', 'maps', 'normal', 'goblincave1.png'),
        os.path.join(path, '..', 'assets', 'maps', 'normal', 'crypt1.png'),
        os.path.join(path, '..', 'assets', 'maps', 'normal', 'crypt2.png'),
        os.path.join(path, '..', 'assets', 'maps', 'normal', 'crypt3.png'),
        os.path.join(path, '..', 'assets', 'maps', 'normal', 'crypt4.png'),
        os.path.join(path, '..', 'assets', 'maps', 'normal', 'crypt5.png'),
        os.path.join(path, '..', 'assets', 'maps', 'normal', 'crypt6.png'),
    ]
    # Edge detected maps
    map_edges_paths = [
        os.path.join(path, '..', 'assets', 'maps', 'edges', 'edge_goblincave1.png'),
        os.path.join(path, '..', 'assets', 'maps', 'edges', 'edge_crypt1.png'),
        os.path.join(path, '..', 'assets', 'maps', 'edges', 'edge_crypt2.png'),
        os.path.join(path, '..', 'assets', 'maps', 'edges', 'edge_crypt3.png'),
        os.path.join(path, '..', 'assets', 'maps', 'edges', 'edge_crypt4.png'),
        os.path.join(path, '..', 'assets', 'maps', 'edges', 'edge_crypt5.png'),
        os.path.join(path, '..', 'assets', 'maps', 'edges', 'edge_crypt6.png'),
    ]
    minimap_edges_path = os.path.join(path, '..', 'assets', 'maps', 'edges', 'minimap_edges.png')
    map_edges_path = os.path.join(path, '..', 'assets', 'maps', 'edges', 'map_edges.png')


    # TEST IMAGES
    # Controlled images for testing without capture method
    test_minimap_path = os.path.join(path, '..', 'assets', 'test_images', 'test_minimap.png')
    test_minimap2_path = os.path.join(path, '..', 'assets', 'test_images', 'test_minimap2.png')
    test_images_path = os.path.join(path, '..', 'assets', 'test_images')

    #------------------------------------------------------------
    # END OF ASSETS PATHS