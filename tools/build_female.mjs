// Repacks HuBMAP CCF 3D Reference Object Library v1.0 (Visible Human Female, CC BY 4.0) into per-layer GLBs + parts.json
import * as THREE from 'three';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import fs from 'fs';
const SRC=process.argv[2]||'/tmp/ccf/v1.0/models/', OUT=process.argv[3]||'/mnt/user-data/outputs/human-body-explorer-v3/models/female/';
const FILES={skin:['VH_F_Skin'],organs:['VH_F_Heart','VH_F_Lung','VH_F_Kidney_Left','VH_F_Kidney_Right','VH_F_Spleen','VH_F_Thymus','SBU_F_Intestine_Large','NIH_F_Lymph_Node_Left','NIH_F_Lymph_Node_Right'],skeleton:['VH_F_Pelvis'],vessels:['VH_F_Vasculature']};
const load=async f=>{const b=fs.readFileSync(SRC+f+'.glb');const g=await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');g.scene.updateMatrixWorld(true);return g.scene};
const bake=scene=>{const out=[];scene.traverse(o=>{if(!o.isMesh)return;const g=o.geometry.clone();g.applyMatrix4(o.matrixWorld);if(!g.attributes.normal)g.computeVertexNormals();out.push({name:o.name,g})});return out};
// 1. skin gives the vertical offset (feet at y=0)
const skinMeshes=bake(await load('VH_F_Skin')); const sb=new THREE.Box3(); skinMeshes.forEach(m=>{m.g.computeBoundingBox();sb.union(m.g.boundingBox)});
const OFF=-sb.min.y; console.log('vertical offset',OFF.toFixed(4));
const pretty=n=>{let s=n.replace(/^(VHF_|Yao_)/,'').replace(/_([LR])(_[a-z]+)?$/,(m,s2)=>' ('+(s2==='L'?'left':'right')+')').replace(/_/g,' ');return s.charAt(0).toUpperCase()+s.slice(1)};
const heartNames=new Set(), parts={skin:[],organs:[],skeleton:[],vessels:[]}, boundsOf=g=>{g.computeBoundingBox();return g.boundingBox};
const classifyVessel=(n,fromHeart)=>{const l=n.toLowerCase();let s=/(vein|vena|sinus)/.test(l)?'venous':'arterial';let o=null;
  if(/aorta|aortic_arch/.test(l))o='aorta';else if(/vena_cava/.test(l))o='venaCava';else if(fromHeart)o='heart';return {s,o}};
const vasScene=bake(await load('VH_F_Vasculature')), vasNames=new Set(vasScene.map(m=>m.name));
const heartScene=bake(await load('VH_F_Heart')); const heartBounds=new Map(heartScene.map(m=>[m.name,m.g]));
const add=(layer,m,s,o,file)=>{m.g.translate(0,OFF,0);m.g.computeBoundingBox();parts[layer].push({id:m.name,n:pretty(m.name),s,o,l:layer,file,g:m.g})};
skinMeshes.forEach(m=>add('skin',m,'integumentary',null,'VH_F_Skin'));
for(const f of FILES.organs){
  const ms=f==='VH_F_Heart'?heartScene:bake(await load(f));
  for(const m of ms){const n=m.name.toLowerCase();
    if(f==='VH_F_Heart'){ if(vasNames.has(m.name)){heartNames.add(m.name);continue} add('organs',m,'cardiac','heart',f); continue}
    if(f==='VH_F_Lung'){ add('organs',m,'respiratory',/^vhf_trachea$/.test(n)?'trachea':/cartilage|carina|epiglot/.test(n)&&!/bronch/.test(n)?null:'lungs',f); continue}
    if(/Kidney/.test(f)) add('organs',m,'urinary','kidneys',f);
    else if(/Spleen/.test(f)) add('organs',m,'lymphatic','spleen',f);
    else if(/Thymus|Lymph/.test(f)) add('organs',m,'lymphatic',null,f);
    else if(/Intestine_Large/.test(f)) add('organs',m,'digestive','largeIntestine',f);
  }
}
for(const m of bake(await load('VH_F_Pelvis'))) add('skeleton',m,'skeletal',null,'VH_F_Pelvis');
let dupOK=0,dupDiff=[];
for(const m of vasScene){const fromHeart=heartNames.has(m.name);
  if(fromHeart){const h=heartBounds.get(m.name);const a=boundsOf(h.clone()),b=boundsOf(m.g.clone());const d=Math.max(...['x','y','z'].map(k=>Math.abs(a.min[k]-b.min[k])+Math.abs(a.max[k]-b.max[k])));d<.002?dupOK++:dupDiff.push([m.name,d.toFixed(4)])}
  const c=classifyVessel(m.name,fromHeart); add('vessels',m,c.s,c.o,'VH_F_Vasculature');}
console.log('heart-file vessels duplicated in vasculature file:',heartNames.size,'| same bounds (<2mm):',dupOK,'| differing:',JSON.stringify(dupDiff));
const ids=new Set(),meta=[];
const pad=(b,c=0)=>{const n=(-b.length%4+4)%4;return n?Buffer.concat([b,Buffer.alloc(n,c)]):b};
for(const [layer,list] of Object.entries(parts)){
  const bufs=[],bvs=[],acc=[],meshes=[],nodes=[];let off=0;
  const addBV=(buf,target)=>{const p=pad(buf);bvs.push({buffer:0,byteOffset:off,byteLength:buf.length,target});bufs.push(p);off+=p.length;return bvs.length-1};
  for(const p of list){ if(ids.has(p.id))throw new Error('duplicate id '+p.id); ids.add(p.id);
    const pos=p.g.attributes.position.array, nor=p.g.attributes.normal.array, idx=p.g.index?p.g.index.array:Uint32Array.from({length:pos.length/3},(_,i)=>i);
    const nrm=new Int16Array(nor.length);for(let i=0;i<nor.length;i+=3){let x=nor[i],y=nor[i+1],z=nor[i+2];const l=Math.hypot(x,y,z)||1;nrm[i]=Math.round(x/l*32767);nrm[i+1]=Math.round(y/l*32767);nrm[i+2]=Math.round(z/l*32767)}
    const vc=pos.length/3,i16=vc<65535,ia=i16?Uint16Array.from(idx):Uint32Array.from(idx);const bb=p.g.boundingBox;
    const a0=acc.length;
    acc.push({bufferView:addBV(Buffer.from(new Float32Array(pos).buffer),34962),componentType:5126,count:vc,type:'VEC3',min:bb.min.toArray(),max:bb.max.toArray()});
    acc.push({bufferView:addBV(Buffer.from(nrm.buffer),34962),componentType:5122,normalized:true,count:vc,type:'VEC3'});
    acc.push({bufferView:addBV(Buffer.from(ia.buffer),34963),componentType:i16?5123:5125,count:idx.length,type:'SCALAR'});
    meshes.push({primitives:[{attributes:{POSITION:a0,NORMAL:a0+1},indices:a0+2,material:0}]});nodes.push({name:p.id,mesh:meshes.length-1,extras:{id:p.id}});
    meta.push({id:p.id,n:p.n,s:p.s,l:layer,o:p.o,b:[bb.min.toArray().map(x=>+x.toFixed(4)),bb.max.toArray().map(x=>+x.toFixed(4))],src:p.file});}
  const bin=Buffer.concat(bufs);
  const g={asset:{version:'2.0',generator:'HuBMAP CCF v1.0 VH Female repack (CC BY 4.0)'},extensionsUsed:['KHR_mesh_quantization'],extensionsRequired:['KHR_mesh_quantization'],scene:0,scenes:[{nodes:nodes.map((_,i)=>i)}],nodes,meshes,accessors:acc,bufferViews:bvs,buffers:[{byteLength:bin.length}],materials:[{name:'base',pbrMetallicRoughness:{baseColorFactor:[.8,.8,.8,1],metallicFactor:0,roughnessFactor:.6}}]};
  const js=pad(Buffer.from(JSON.stringify(g)),32);const h=Buffer.alloc(12);h.writeUInt32LE(0x46546C67,0);h.writeUInt32LE(2,4);h.writeUInt32LE(12+8+js.length+8+bin.length,8);
  const jh=Buffer.alloc(8);jh.writeUInt32LE(js.length,0);jh.writeUInt32LE(0x4E4F534A,4);const bh=Buffer.alloc(8);bh.writeUInt32LE(bin.length,0);bh.writeUInt32LE(0x004E4942,4);
  fs.writeFileSync(OUT+layer+'.glb',Buffer.concat([h,jh,js,bh,bin]));console.log(layer,list.length,'parts',(fs.statSync(OUT+layer+'.glb').size/1e6).toFixed(1),'MB');}
fs.writeFileSync(OUT+'parts.json',JSON.stringify(meta));
const c={};meta.forEach(m=>c[m.o||'-']=(c[m.o||'-']||0)+1);console.log('total',meta.length,'organ keys',JSON.stringify(c));
