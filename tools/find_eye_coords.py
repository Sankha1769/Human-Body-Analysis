import json, struct

with open('models/male.glb', 'rb') as f:
    magic, ver, length = struct.unpack('<4sII', f.read(12))
    chunk_len, chunk_type = struct.unpack('<I4s', f.read(8))
    data = json.loads(f.read(chunk_len))
    # read binary buffer
    buf_len, buf_type = struct.unpack('<I4s', f.read(8))
    bin_data = f.read(buf_len)
    
    pos_acc = data['accessors'][0]
    pos_view = data['bufferViews'][pos_acc['bufferView']]
    count = pos_acc['count']
    offset = pos_view.get('byteOffset', 0)
    
    # find eye socket vertices (around Y in [1.55, 1.70], Z > 0.05)
    eye_vertices = []
    for i in range(count):
        x, y, z = struct.unpack_from('<fff', bin_data, offset + i * 12)
        if 1.60 <= y <= 1.68 and z > 0.06:
            eye_vertices.append((x, y, z))
    
    print(f'Found {len(eye_vertices)} head front vertices')
    # find min and max of X around eye region
    left_eye = [v for v in eye_vertices if v[0] < -0.015 and v[0] > -0.06]
    right_eye = [v for v in eye_vertices if v[0] > 0.015 and v[0] < 0.06]
    if left_eye and right_eye:
        avg_ly = sum(v[1] for v in left_eye)/len(left_eye)
        avg_lz = sum(v[2] for v in left_eye)/len(left_eye)
        avg_lx = sum(v[0] for v in left_eye)/len(left_eye)
        avg_ry = sum(v[1] for v in right_eye)/len(right_eye)
        avg_rz = sum(v[2] for v in right_eye)/len(right_eye)
        avg_rx = sum(v[0] for v in right_eye)/len(right_eye)
        print(f'Left eye socket center: x={avg_lx:.4f}, y={avg_ly:.4f}, z={avg_lz:.4f}')
        print(f'Right eye socket center: x={avg_rx:.4f}, y={avg_ry:.4f}, z={avg_rz:.4f}')
