import os

# Get the absolute path of the current working directory
cwd = os.getcwd()

# Define the paths using the absolute path of the current working directory
mapimage_paths = [
    os.path.join(cwd, 'src', 'images', 'goblincave1.png'),
    os.path.join(cwd, 'src', 'images', 'crypt1.png'),
    os.path.join(cwd, 'src', 'images', 'crypt2.png'),
    os.path.join(cwd, 'src', 'images', 'crypt3.png'),
    os.path.join(cwd, 'src', 'images', 'crypt4.png'),
    os.path.join(cwd, 'src', 'images', 'crypt5.png'),
    os.path.join(cwd, 'src', 'images', 'crypt6.png'),
]
map_edges_paths = [
    os.path.join(cwd, 'src', 'images', 'edge_goblincave1.png'),
    os.path.join(cwd, 'src', 'images', 'edge_crypt1.png'),
    os.path.join(cwd, 'src', 'images', 'edge_crypt2.png'),
    os.path.join(cwd, 'src', 'images', 'edge_crypt3.png'),
    os.path.join(cwd, 'src', 'images', 'edge_crypt4.png'),
    os.path.join(cwd, 'src', 'images', 'edge_crypt5.png'),
    os.path.join(cwd, 'src', 'images', 'edge_crypt6.png'),
]
minimap_path = os.path.join(cwd, 'src', 'images', 'screenshot.png')
minimap_edges_path = os.path.join(cwd, 'src', 'images', 'minimap_edges.png')
map_edges_path = os.path.join(cwd, 'src', 'images', 'map_edges.png')
