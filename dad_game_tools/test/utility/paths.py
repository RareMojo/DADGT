import os

path = os.path.dirname(os.path.abspath(__file__))


# LOGS PATHS
#------------------------------------------------------------
log_path = os.path.join(path, '..', 'utility', 'logs', 'log.txt')
latest_log_path = os.path.join(path, '..', 'utility', 'logs', 'latest_log.txt')


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