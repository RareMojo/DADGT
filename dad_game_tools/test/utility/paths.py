import os

path = os.path.dirname(os.path.abspath(__file__))


# ASSETS PATHS
#------------------------------------------------------------

# CAPTURES
health_bar_path = os.path.join(path, '..', 'assets', 'captures', 'health_bar.png')
compass_path = os.path.join(path, '..', 'assets', 'captures', 'compass.png')
killfeed_path = os.path.join(path, '..', 'assets', 'captures', 'killfeed.png')
match_time_path = os.path.join(path, '..', 'assets', 'captures', 'match_time.png')
screenshot_path = os.path.join(path, '..', 'assets', 'captures', 'screenshot.png')
minimap_path = os.path.join(path, '..', 'assets', 'captures', 'minimap.png')

# INTERFACE
outline = os.path.join(path, '..', 'assets', 'interface', 'outline.png')

# MAPS
minimap_edges_path = os.path.join(path, '..', 'assets', 'maps', 'minimap_edges.png')
map_edges_path = os.path.join(path, '..', 'assets', 'maps', 'map_edges.png')
mapimage_paths = [
    os.path.join(path, '..', 'assets', 'maps', 'normal', 'goblincave1.png'),
    os.path.join(path, '..', 'assets', 'maps', 'normal', 'crypt1.png'),
    os.path.join(path, '..', 'assets', 'maps', 'normal', 'crypt2.png'),
    os.path.join(path, '..', 'assets', 'maps', 'normal', 'crypt3.png'),
    os.path.join(path, '..', 'assets', 'maps', 'normal', 'crypt4.png'),
    os.path.join(path, '..', 'assets', 'maps', 'normal', 'crypt5.png'),
    os.path.join(path, '..', 'assets', 'maps', 'normal', 'crypt6.png'),
]
map_edges_paths = [
    os.path.join(path, '..', 'assets', 'maps', 'edges', 'edge_goblincave1.png'),
    os.path.join(path, '..', 'assets', 'maps', 'edges', 'edge_crypt1.png'),
    os.path.join(path, '..', 'assets', 'maps', 'edges', 'edge_crypt2.png'),
    os.path.join(path, '..', 'assets', 'maps', 'edges', 'edge_crypt3.png'),
    os.path.join(path, '..', 'assets', 'maps', 'edges', 'edge_crypt4.png'),
    os.path.join(path, '..', 'assets', 'maps', 'edges', 'edge_crypt5.png'),
    os.path.join(path, '..', 'assets', 'maps', 'edges', 'edge_crypt6.png'),
]

# TEST IMAGES
test_minimap_path = os.path.join(path, '..', 'assets', 'test_images', 'test_minimap.png')
test_minimap2_path = os.path.join(path, '..', 'assets', 'test_images', 'test_minimap2.png')
test = os.path.join(path, '..', 'assets', 'test_images', 'test.jpg')

# END OF ASSETS PATHS