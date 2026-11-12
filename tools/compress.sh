#!/bin/sh
# Meshopt-compress every layer GLB (requires: npm i gltfpack). Keeps node names, materials and extras; no re-quantisation.
for f in models/male/*.glb models/female/*.glb; do npx gltfpack -i "$f" -o "$f.tmp" -cc -kn -km -ke -noq && mv "$f.tmp" "$f"; done
