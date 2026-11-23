import struct, json, glob

def get_bounds(path):
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
            size = [bmax[i] - bmin[i] for i in range(3)]
            center = [(bmax[i] + bmin[i])/2 for i in range(3)]
            return bmin, bmax, size, center
    return None

for p in sorted(glob.glob('models/anatomy/*.glb')):
    res = get_bounds(p)
    if res:
        bmin, bmax, size, center = res
        print(f'{p:<30} size=[{size[0]:.2f}, {size[1]:.2f}, {size[2]:.2f}] center=[{center[0]:.2f}, {center[1]:.2f}, {center[2]:.2f}]')
