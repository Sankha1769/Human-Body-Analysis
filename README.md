# Human Body Explorer v3

Interactive Three.js anatomy atlas with two separate anatomical reference models:

| | Male | Female |
|---|---|---|
| Source | BodyParts3D 4.0 | HuBMAP Visible Human Female v1.0 |
| Structures | 2,234 in 7 layers | 284 in 4 layers (**partial**) |
| Has | skin, organs, skeleton, muscles, arteries, veins, nerves | skin, heart, lungs, kidneys, spleen, thymus, large intestine, lymph nodes, pelvis, vessels |
| Lacks | whole-lung surface, whole liver | brain, skeleton (except pelvis), muscles, nerves, liver, stomach, pancreas, small intestine, bladder, **all reproductive organs** |

The Male/Female switch swaps the complete model (never mixes assets), releases the previous model's geometry, updates counts, search, systems and info, clears selection and keeps the current visualisation mode where the new model supports it. Controls for structures a model does not have are disabled with an explanation.

No primitive or procedural anatomy is drawn anywhere. If a model file is missing the app shows an error naming it (for example, deleting `models/female/` leaves the male model working and shows the missing-file message when Female is chosen).

## Run on Windows (PowerShell)
1. Unzip so you have the `human-body-explorer` folder (keep the `models` folder inside it).
2. Open PowerShell in that folder and run `py -m http.server 8000`
3. Open http://localhost:8000 in Chrome or Edge (not by double-clicking `index.html`). Internet is needed for the Three.js CDN. Stop with Ctrl+C.

Weak GPU or software rendering: http://localhost:8000/?quality=low (no shadow map, pixel ratio 1).

## Project layout
    index.html
    models/male/    parts.json + skin, organs, skeleton, muscles, arteries, veins, nerves .glb
    models/female/  parts.json + skin, organs, skeleton (pelvis), vessels .glb
    tools/          build scripts (male repack, female repack, compression)
    licenses/       CC BY 4.0 text
    ATTRIBUTION.md  sources and licences for every asset (also in-app: Credits & licences)
    ASSET_INVENTORY.md  audit: counts, triangles, what is available/incomplete/missing

Startup requests only `parts.json`, `organs.glb` and `skin.glb` of the male model. Other layers load when switched on and unused heavy layers are unloaded (at most two kept). GLBs are Meshopt-compressed (about 53 MB in total versus 78 MB uncompressed).

## Visualisation modes (bottom toolbar)
External · Transparent skin · Muscles · Skeleton · Organs · Circulatory · Nervous · Overview, plus layer toggles with fade, skin opacity, cross-section (sagittal/coronal/transverse, clipping without cap fill), Explode (radial separation, illustrative), Isolate / Hide / Show all, Front/Back/Left/Right (Left = the patient's left), Inspect organ (isolates an organ with its components and leader-line labels). There is no separate "superficial/deep muscles" mode because the source data does not label muscle depth.

## What was tested (real Chromium, software WebGL, local HTTP server, Three.js served locally)
Male: startup requests (only the 3 expected files), hover tooltip, click selection (stomach), front/back/left/right camera positions, system filter fade, isolate, show all, explode and return, cross-section clipping, skin opacity, lazy loading the skeleton, search, heart inspect. Female: switch requests (only female files), male geometry released, hover and click (spleen), kidney selection, pelvis, disabled controls for missing structures, explode, circulatory step, heart inspect (42 labelled parts), lungs, search, back view, round trip back to male with no mixed assets. No console errors or 4xx responses in these runs. 13/13 male checks and 8 of 9 female checks passed in the scripted run; the one female check failure was a test-timing artefact and passed when rerun with a proper wait.

**Not verified:** performance on a real GPU (the test browser rendered in software; JS heap stayed under about 20 MB and the Male scene holds about 635 geometries), Firefox/Safari, touch gestures, high-DPI rendering, every button on mobile, the Nervous step visually, and behaviour with all seven male layers loaded on a low-memory machine. Visual quality was judged from screenshots only.

## Known limitations
See ASSET_INVENTORY.md. Highlights: no textures or normal/roughness/AO maps exist in the sources, so surfaces are plain physically based colours with shadows and environment lighting (this is not photorealism); male lung surface and liver incomplete; female model is partial; panel text still shows the last selected organ after a mode change clears the selection; info text for 15 organs was written from general knowledge and not clinically reviewed.
