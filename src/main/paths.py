import os
import cv2

path = os.path.dirname(os.path.abspath(__file__))

minimap_path = os.path.join(path, '..', 'images', 'screenshot.png')
minimap_edges_path = os.path.join(path, '..', 'images', 'minimap_edges.png')
map_edges_path = os.path.join(path, '..', 'images', 'map_edges.png')
health_bar_path = os.path.join(path, '..', 'images', 'health_bar.png')
health_bar_edges_path = os.path.join(path, '..', 'images', 'health_bar_edges.png')
compass_path = os.path.join(path, '..', 'images', 'compass.png')

mapimage_paths = [
    os.path.join(path, '..', 'images', 'goblincave1.png'),
    os.path.join(path, '..', 'images', 'crypt1.png'),
    os.path.join(path, '..', 'images', 'crypt2.png'),
    os.path.join(path, '..', 'images', 'crypt3.png'),
    os.path.join(path, '..', 'images', 'crypt4.png'),
    os.path.join(path, '..', 'images', 'crypt5.png'),
    os.path.join(path, '..', 'images', 'crypt6.png'),
]

map_edges_paths = [
    os.path.join(path, '..', 'images', 'edge_goblincave1.png'),
    os.path.join(path, '..', 'images', 'edge_crypt1.png'),
    os.path.join(path, '..', 'images', 'edge_crypt2.png'),
    os.path.join(path, '..', 'images', 'edge_crypt3.png'),
    os.path.join(path, '..', 'images', 'edge_crypt4.png'),
    os.path.join(path, '..', 'images', 'edge_crypt5.png'),
    os.path.join(path, '..', 'images', 'edge_crypt6.png'),
]