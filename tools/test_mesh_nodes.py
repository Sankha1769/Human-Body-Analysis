import json, struct

def inspect_nodes_bounds(path):
    with open(path, 'rb') as f:
        magic, ver, length = struct.unpack('<4sII', f.read(12))
        chunk_len, chunk_type = struct.unpack('<I4s', f.read(8))
        data = json.loads(f.read(chunk_len))
        nodes = data.get('nodes', [])
        meshes = data.get('meshes', [])
        accessors = data.get('accessors', [])
        print(f'=== {path} ===')
        for node in nodes:
            name = node.get('name')
            mesh_idx = node.get('mesh')
            if mesh_idx is not None and mesh_idx < len(meshes):
                mesh = meshes[mesh_idx]
                prim = mesh.get('primitives', [{}])[0]
                pos_idx = prim.get('attributes', {}).get('POSITION')
                if pos_idx is not None and pos_idx < len(accessors):
                    acc = accessors[pos_idx]
                    ymin = acc.get('min', [0, 0, 0])[1]
                    ymax = acc.get('max', [0, 0, 0])[1]
                    if 'femur' in name.lower() or 'tibia' in name.lower() or 'skull' in name.lower() or 'parietal' in name.lower() or 'calcaneus' in name.lower() or 'deltoid' in name.lower() or 'gastrocnemius' in name.lower() or 'frontalis' in name.lower() or 'soleus' in name.lower():
                        print(f'  {name:<30}: ymin={ymin:.3f}, ymax={ymax:.3f}')

inspect_nodes_bounds('models/anatomy/skeleton.glb')
inspect_nodes_bounds('models/anatomy/muscles.glb')
