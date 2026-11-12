import json,re,struct,numpy as np,collections,os
SRC='/tmp/ha/public/models/'; OUT='/mnt/user-data/outputs/human-body-explorer/models/'
os.makedirs(OUT,exist_ok=True)
a=json.load(open(SRC+'atlas.json')); chunks=[open(SRC+f'body-{i}.bin','rb').read() for i in range(len(a['chunks']))]
for i,c in enumerate(a['chunks']): assert len(chunks[i])==c['bytes'],(i,len(chunks[i]),c['bytes'])
byid={p['id']:p for p in a['parts']}
organ_of={}
for c in a['concepts']:
    k={'FMA7088':'heart','FMA50801':'brain','FMA7197':'liver','FMA7309':'lungs','FMA7310':'lungs','FMA7200':'smallIntestine','FMA7201':'largeIntestine','FMA7203':'kidneys','FMA7647':'spinalCord'}.get(c['id'])
    if k:
        for e in c['elements']: organ_of.setdefault(e,k)
nm=lambda p:p['name']
def organ(p):
    n=p['name']
    if p['id'] in organ_of: return organ_of[p['id']]
    if re.fullmatch(r'Trachea',n): return 'trachea'
    if re.search(r'aorta',n,re.I) and p['system']=='arterial' and not re.search('branch|oesoph',n,re.I): return 'aorta'
    if re.search(r'vena cava',n,re.I): return 'venaCava'
    if n=='Stomach': return 'stomach'
    if re.search('pancreas',n,re.I): return 'pancreas'
    if n=='Urinary bladder': return 'bladder'
    if n=='Spleen': return 'spleen'
    if re.search(r'colon|rectum|appendix|ileocecal',n,re.I): return 'largeIntestine'
    if re.search(r'jejunum|ileum|duodenum',n,re.I): return 'smallIntestine'
    if re.search(r'bronch',n,re.I): return 'lungs'
    return None
def layer_of(p,s):
    if s=='integumentary': return 'skin'
    if s=='skeletal': return 'skeleton'
    if s=='muscular': return 'muscles'
    if s=='connective': return 'skeleton' if re.search('cartilage|ligament|disc|capsule|menisc|labrum|synovial',p['name'],re.I) else 'muscles'
    if s=='arterial': return 'arteries'
    if s=='venous': return 'veins'
    if s=='nervous': return 'nerves'
    return 'organs'
layers=collections.defaultdict(list); meta=[]
for p in a['parts']:
    s=p['system']
    if re.search(r'(third|fourth|lateral) ventricle|interventricular foramen',p['name'],re.I): s='nervous'
    L=layer_of(p,s); layers[L].append(p)
    meta.append(dict(id=p['id'],n=p['name'],s=s,l=L,o=organ(p),b=[[round(x,4) for x in p['bounds'][0]],[round(x,4) for x in p['bounds'][1]]]))
json.dump(meta,open(OUT+'parts.json','w'),separators=(',',':'))
def pad(b,c=b'\0'): return b+c*((-len(b))%4)
for L,parts in layers.items():
    bin_=bytearray(); bvs=[]; acc=[]; meshes=[]; nodes=[]
    def add(data,target):
        global bin_
        off=len(bin_); bin_+=pad(data); bvs.append(dict(buffer=0,byteOffset=off,byteLength=len(data),target=target)); return len(bvs)-1
    for p in parts:
        ch=chunks[p['chunk']]; vc=p['vertexCount']; ic=p['indexCount']
        pos=np.frombuffer(ch,np.float32,vc*3,p['positions']).reshape(-1,3)
        nor=np.frombuffer(ch,np.int16,vc*3,p['normals'])
        idx=np.frombuffer(ch,np.uint32,ic,p['indices'])
        i16=vc<65535
        idxd=idx.astype(np.uint16) if i16 else idx
        a0=len(acc); acc.append(dict(bufferView=add(pos.tobytes(),34962),componentType=5126,count=vc,type='VEC3',min=pos.min(0).tolist(),max=pos.max(0).tolist()))
        acc.append(dict(bufferView=add(nor.tobytes(),34962),componentType=5122,normalized=True,count=vc,type='VEC3'))
        acc.append(dict(bufferView=add(idxd.tobytes(),34963),componentType=5123 if i16 else 5125,count=ic,type='SCALAR'))
        meshes.append(dict(primitives=[dict(attributes=dict(POSITION=a0,NORMAL=a0+1),indices=a0+2,material=0)]))
        nodes.append(dict(name=p['id'],mesh=len(meshes)-1,extras=dict(id=p['id'])))
    g=dict(asset=dict(version='2.0',generator='BodyParts3D 4.0 repack (CC BY 4.0)'),extensionsUsed=['KHR_mesh_quantization'],extensionsRequired=['KHR_mesh_quantization'],
      scene=0,scenes=[dict(nodes=list(range(len(nodes))))],nodes=nodes,meshes=meshes,accessors=acc,bufferViews=bvs,buffers=[dict(byteLength=len(bin_))],
      materials=[dict(name='base',pbrMetallicRoughness=dict(baseColorFactor=[.8,.8,.8,1],metallicFactor=0,roughnessFactor=.6))])
    js=pad(json.dumps(g,separators=(',',':')).encode(),b' ')
    glb=struct.pack('<III',0x46546C67,2,12+8+len(js)+8+len(bin_))+struct.pack('<II',len(js),0x4E4F534A)+js+struct.pack('<II',len(bin_),0x004E4942)+bytes(bin_)
    open(OUT+f'{L}.glb','wb').write(glb); print(L,len(parts),'parts',round(len(glb)/1e6,1),'MB')
