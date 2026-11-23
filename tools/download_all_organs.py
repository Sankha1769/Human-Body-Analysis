import urllib.request, os
from inspect_skeleton_nodes import inspect_nodes

models = ['brain', 'lungs', 'liver', 'muscles', 'spinal-cord']
for m in models:
    path = f'models/anatomy/{m}.glb'
    if not os.path.exists(path):
        url = f'https://raw.githubusercontent.com/organui/{m}-3d/main/public/models/{m}.glb'
        print(f'Downloading {m}...')
        urllib.request.urlretrieve(url, path)
    inspect_nodes(path)
