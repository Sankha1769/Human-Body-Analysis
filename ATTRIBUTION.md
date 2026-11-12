# Asset credits, sources and licences

Every anatomical asset in this project, where it came from, and under which licence. The CC BY 4.0 legal text is in `licenses/CC-BY-4.0.txt` (copied from the HuBMAP repository's LICENSE file).

## 1. Male model: BodyParts3D 4.0
- Content: adult male reference anatomy, 2,234 meshes (`models/male/`).
- Credit: BodyParts3D, © The Database Center for Life Science (DBCLS), **CC BY 4.0**.
- Licence checked on the DBCLS archive licence page (last updated 2025-02-27): https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html
- Dataset: https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html. Publication: Mitsuhashi et al. (2009), https://doi.org/10.1093/nar/gkn613
- Earlier BodyParts3D releases and derivatives (e.g. Z-Anatomy) were published under CC BY-SA 2.1 Japan; check the licence of the exact release you obtain.
- Obtained via the open-source Human Atlas project (MIT licence, github.com/ashemag/human-atlas), which had converted the OBJ files (mm, Z-up) to metres/Y-up and simplified each mesh (meshoptimizer, 0.2% error limit).
- Changes made here: repacked into seven layer GLB files with quantised normals (`tools/build_glb_male.py`), layer assignment, system grouping, organ mapping, colours; then Meshopt-compressed (`tools/compress.sh`).

## 2. Female model (partial): HuBMAP CCF 3D Reference Object Library v1.0, Visible Human Female
- Content: 284 meshes (`models/female/`): skin, heart (14 parts), lungs/trachea/larynx cartilages/bronchopulmonary segments (65), kidneys (81 parts), spleen (5), thymus (2), large intestine (10), lymph nodes (14), pelvic bones (14) and blood vessels (78).
- Source files (all from `VH_Female/v1.0` in https://github.com/hubmapconsortium/ccf-3d-reference-object-library, also in https://github.com/hubmapconsortium/ccf-releases): `VH_F_Skin`, `VH_F_Heart`, `VH_F_Lung`, `VH_F_Kidney_Left/Right`, `VH_F_Spleen`, `VH_F_Thymus`, `VH_F_Pelvis`, `VH_F_Vasculature`, `SBU_F_Intestine_Large` (Stony Brook University), `NIH_F_Lymph_Node_Left/Right` (NIH 3D, modelled by Yao).
- Licence: **CC BY 4.0**. The repository's LICENSE file is the CC BY 4.0 text, its README carries the CC BY 4.0 badge, and the library page (https://hubmapconsortium.github.io/ccf/pages/ccf-3d-reference-library.html) states that all CCF 3D reference objects are released under CC BY 4.0. A HuBMAP presentation notes the Allen Institute brain as the exception.
- **Excluded on purpose:** `Allen_F_Brain` (different licence, not verified for redistribution), the combined `VH_F_United.glb`, and the `UnderReview` lung.
- Citation requested by the library: Browne K, Cross LE, Herr II BW, Record L, Quardokus E, Bueckle A, Börner K. HuBMAP CCF 3D Reference Object Library. https://hubmapconsortium.github.io/ccf/pages/ccf-3d-reference-library.html. Underlying imaging: U.S. National Library of Medicine, Visible Human Project.
- Changes made here (`tools/build_female.mjs`): node transforms baked into the geometry, whole model shifted up 0.8615 m so the feet sit at y = 0, 37 vessel meshes that were duplicated between the heart and vasculature files merged to one copy (bounds identical within 2 mm), names tidied, normals quantised, one GLB per layer, then Meshopt compression.

## Considered and not used
- **Z-Anatomy** (CC BY-SA 4.0, derived from BodyParts3D; some components are non-commercial, e.g. a kidney and an inner-ear model). Not included. It would need component-by-component licence checks and would impose share-alike terms on anything taken from it.
- Female reproductive organs and later HuBMAP organ releases are hosted on a server that was not reachable from the build environment, so they are not included.
- No HDR environment maps or textures are used; the environment lighting is Three.js's built-in RoomEnvironment (generated, no image asset).

## Software
Three.js r160 (MIT): OrbitControls, GLTFLoader, MeshoptDecoder, RoomEnvironment; loaded from the jsDelivr CDN. gltfpack/meshoptimizer (MIT) used at build time.

## Not clinically validated
Both models are simplified educational reference data. Organ proportions and positions come from the source datasets and were only checked by eye. Do not use for diagnosis or treatment.
