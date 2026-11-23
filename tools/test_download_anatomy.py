import urllib.request, os, struct, json

os.makedirs('models/anatomy', exist_ok=True)

test_models = ['heart', 'skeleton', 'stomach', 'kidneys']
for m in test_models:
    path = f'models/anatomy/{m}.glb'
    if not os.path.exists(path):
        url = f'https://raw.githubusercontent.com/organui/{m}-3d/main/public/models/{m}.glb'
        print(f'Downloading {m}...')
        urllib.request.urlretrieve(url, path)
    print(f'Saved {path}, size={os.path.getsize(path)}')

def inspect_glb(path):
    with open(path, 'rb') as f:
        magic, ver, length = struct.unpack('<4sII', f.read(12))
        chunk_len, chunk_type = struct.unpack('<I4s', f.read(8))
        data = json.loads(f.read(chunk_len))
        accessors = data.get('accessors', [])
        # Find min/max of POSITION accessors
        mins = []
        maxs = []
        for a in accessors:
            if a.get('type') == 'VEC3' and 'min' in a and 'max' in a:
                mins.append(a['min'])
                maxs.append(a['max'])
        if mins and maxs:
            overall_min = [min(m[i] for m in mins) for i in range(3)]
            overall_max = [max(m[i] for m in maxs) for i in range(3)]
            print(f'{path} bounds: min={overall_min}, max={overall_max}')
            size = [overall_max[i] - overall_min[i] for i in range(3)]
            print(f'{path} size: {size}')

for m in test_models:
    inspect_glb(f'models/anatomy/{m}.glb')
