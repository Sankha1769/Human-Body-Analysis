import struct, json

def get_male_bounds(path):
    with open(path, 'rb') as f:
        magic, ver, length = struct.unpack('<4sII', f.read(12))
        chunk_len, chunk_type = struct.unpack('<I4s', f.read(8))
        data = json.loads(f.read(chunk_len))
        accessors = data.get('accessors', [])
        for a in accessors:
            if a.get('type') == 'VEC3' and 'min' in a and 'max' in a:
                print('Male bounds: min =', a['min'], 'max =', a['max'])
                bmin = a['min']
                bmax = a['max']
                print('Height:', bmax[1] - bmin[1], 'Center Y:', (bmax[1] + bmin[1])/2)

get_male_bounds('models/male.glb')
get_male_bounds('models/female.glb')
