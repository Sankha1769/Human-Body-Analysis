import struct, json

def inspect_nodes(path):
    with open(path, 'rb') as f:
        magic, ver, length = struct.unpack('<4sII', f.read(12))
        chunk_len, chunk_type = struct.unpack('<I4s', f.read(8))
        data = json.loads(f.read(chunk_len))
        print('Path:', path)
        print('Nodes count:', len(data.get('nodes', [])))
        for i, n in enumerate(data.get('nodes', [])):
            if i < 20:
                print('Node:', n.get('name'))
        print('Meshes count:', len(data.get('meshes', [])))
        for i, m in enumerate(data.get('meshes', [])):
            if i < 20:
                print('Mesh:', m.get('name'))

inspect_nodes('models/anatomy/skeleton.glb')
