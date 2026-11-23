import struct, json

def inspect_min_max(path):
    with open(path, 'rb') as f:
        magic, ver, length = struct.unpack('<4sII', f.read(12))
        chunk_len, chunk_type = struct.unpack('<I4s', f.read(8))
        data = json.loads(f.read(chunk_len))
        accessors = data.get('accessors', [])
        mins = []
        maxs = []
        for a in accessors:
            if a.get('type') == 'VEC3' and 'min' in a and 'max' in a:
                mins.append(a['min'])
                maxs.append(a['max'])
        if mins and maxs:
            bmin = [min(m[i] for m in mins) for i in range(3)]
            bmax = [max(m[i] for m in maxs) for i in range(3)]
            print(f'{path} bmin={bmin}, bmax={bmax}')

inspect_min_max('models/anatomy/skeleton.glb')
inspect_min_max('models/anatomy/muscles.glb')
inspect_min_max('models/anatomy/brain.glb')
inspect_min_max('models/anatomy/heart.glb')
inspect_min_max('models/anatomy/lungs.glb')
inspect_min_max('models/anatomy/liver.glb')
inspect_min_max('models/anatomy/stomach.glb')
inspect_min_max('models/anatomy/kidneys.glb')
inspect_min_max('models/anatomy/spinal-cord.glb')
