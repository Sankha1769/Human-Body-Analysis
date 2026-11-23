# Human Anatomy 3D · Professional Medical Atlas (V7.0)

An ultra-realistic, interactive 3D human anatomy visualization and clinical atlas built in **WebGL** using **Three.js** and physically based rendering (PBR).

![Version](https://img.shields.io/badge/version-7.0--PRO-blue.svg)
![Three.js](https://img.shields.io/badge/three.js-r128-black.svg)
![Platform](https://img.shields.io/badge/platform-WebGL2-green.svg)
![License](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey.svg)

---

## 🌟 Key Features

### 1. Photorealistic Scanned Anatomical Models
- **Adult Male & Female Reference Models**: Full-body anatomical scans in natural standing postures with continuous PBR skin envelopes.
- **PBR Dermal Pipeline**: 4K/2K diffuse, high-resolution normal maps, and roughness maps for authentic pore structure, specular response, and subsurface tissue tone.
- **Zero Z-Fighting / Mesh Overlaps**: Subcutaneous polygon offsets and calibrated layer scaling ($0.246\times$ internal systems, $1.022\times$ skin envelope) ensure zero muscle bursting through the skin.

### 2. Anatomically Accurate External Genitalia
- **Male External Genitalia**:
  - Suspended flaccid penile shaft anchored deep within the pubic symphysis crest.
  - Anatomically contoured glans penis with coronal sulcus and urethral meatus.
  - Dependent bilateral scrotal sac with natural physiological asymmetry (left testis lower) and median raphe seam.
  - Seamless pelvic transition cushion with zero gaps or detachments.
- **Female Reproductive System**: Internal pelvic anatomy including uterus, bilateral fallopian tubes, and ovaries.

### 3. Ultra-Realistic 3D Human Eyeball System
- **Anatomical Sclera**: Modeled with an open anterior corneal limbus aperture ($\theta = 0.48\,\text{rad}$ / $27.5^\circ$), eliminating white scleral occlusion over the anterior chamber.
- **High-Resolution Striated Iris**: Procedurally generated iris texture with 720 radial fibrillar striations, collarette crown, and dark limbal ring in warm hazel-amber (male) and oceanic hazel-slate (female).
- **Glistening Corneal Dome**: Clear convex corneal dome ($R \times 1.04$) catching authentic Purkinje specular reflections.
- **Ocular Adnexa & Micro-Saccades**: Lacrimal caruncles (tear ducts), upper eyelashes along the palpebral margins, and subtle physiological ocular drift.

### 4. Conforming 3D Hair System
- **Male Hairstyle**: Sculpted cranial dome with natural frontal hairline, textured crown locks, temporal sideburn fades, and occipital drape.
- **Female Hairstyle**: Layered shoulder-length hairstyle with center parting, voluminous crown, and cascading locks framing the face, neck, and shoulders.
- **Cranial Inspection Toggle**: Dedicated `💇 Hair ON / OFF` control to instantly hide/reveal hair for cranial examination.

### 5. Multi-System Clinical Layers
- **Integumentary** (Skin & Sensory)
- **Muscular System** (Skeletal muscle anatomy)
- **Skeletal System** (Complete bone framework)
- **Visceral Organs** (Brain, heart with 72 BPM cardiac cycle, lungs, liver, stomach, kidneys, intestines)
- **Cardiovascular** (Arterial and venous trees)
- **Nervous System** (Brain, spinal cord, neural trunks)

### 6. Interactive Visualization Controls
- **Shading Modes**:
  - `REAL`: Physically based rendering with PBR textures and soft anatomical studio lighting.
  - `HOLO`: Clean cyan medical holographic visualization.
  - `X-RAY`: Translucent interior visualization revealing deep organ structures.
- **Camera Navigation**:
  - `Free Orbit`: Smooth 360° rotational inspection, panning, and zoom.
  - `First Person`: WASD walk-through navigation, mouse look, and elevation controls.
- **Multi-Planar Cross-Section Slicing**: Interactive Sagittal, Coronal, and Axial clipping planes.
- **Exploded View**: Dynamic radial separation slider to expand anatomical systems for individual part inspection.
- **Trilingual Atlas**: Full internationalization supporting English (`EN`), Hindi (`हिन्दी`), and Bengali (`বাংলা`).

---

## 🚀 Getting Started

### Local Setup (PowerShell / Terminal)
The entire application runs as a single self-contained `index.html` file using standard ES modules and CDN dependencies:

```powershell
# 1. Clone repository
git clone https://github.com/Sankha1769/Human-Body-Analysis.git
cd Human-Body-Analysis

# 2. Start local HTTP server
python -m http.server 8085

# 3. Open in Chrome or Edge
# Navigate to: http://localhost:8085/index.html
```

---

## 📁 Repository Structure

```text
├── index.html          # Complete single-file application (HTML, CSS, Three.js runtime)
├── README.md           # Documentation and feature guide
├── .gitignore          # Git exclusion rules
├── models/             # 3D Anatomical Assets (.glb)
│   ├── male.glb        # Scanned adult male external body
│   ├── female.glb      # Scanned adult female external body
│   └── anatomy/        # Scanned internal systems (skeleton, muscles, heart, brain, etc.)
├── textures/           # High-resolution PBR dermal skin maps
│   ├── skin_diffuse.png
│   ├── skin_normal.png
│   └── skin_roughness.png
└── tools/              # Anatomical measurement & calibration scripts
```

---

## 📜 Attribution & Licenses
- Anatomical meshes and reference geometries derived from BodyParts3D / OrganUI under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- Procedural textures, shader pipelines, and 3D anatomical sculpting developed for Human Anatomy 3D V7.0.
