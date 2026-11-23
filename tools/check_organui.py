import urllib.request

targets = ['skeleton', 'muscles', 'heart', 'brain', 'lungs', 'liver', 'stomach', 'kidneys', 'spinal-cord']
for t in targets:
    url = f'https://raw.githubusercontent.com/organui/{t}-3d/main/public/models/{t}.glb'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            cl = resp.headers.get('content-length')
            print(f'{t}.glb: {resp.status}, size={cl} bytes')
    except Exception as e:
        print(f'{t}.glb: ERR: {e}')
