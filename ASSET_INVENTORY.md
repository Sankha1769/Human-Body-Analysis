# Asset inventory (audit)

Generated from `models/*/parts.json` and the shipped GLB files. Counts are named meshes; "missing" means no mesh with a matching name exists in the data (name matching, so a different spelling could hide a part; spot checks were done by hand for the organs).

## Totals

| Model | Source | Structures | Layers (meshes · triangles · file size) |
|---|---|---|---|
| Male | BodyParts3D 4.0 (CC BY 4.0) via Human Atlas repack | 2234 | arteries: 639 · 333,798 tris · 4.6 MB; muscles: 426 · 681,140 tris · 13.6 MB; nerves: 144 · 213,436 tris · 2.7 MB; organs: 304 · 337,622 tris · 5.2 MB; skeleton: 312 · 358,560 tris · 5 MB; skin: 5 · 60,362 tris · 0.9 MB; veins: 404 · 303,350 tris · 3.8 MB |
| Female | HuBMAP CCF 3D Reference Object Library v1.0, Visible Human Female (CC BY 4.0) | 284 | organs: 191 · 1,208,422 tris · 12.1 MB; skeleton: 14 · 87,448 tris · 0.9 MB; skin: 1 · 124,348 tris · 3.3 MB; vessels: 78 · 218,216 tris · 2.3 MB |

Male total 2,234 structures, about 2.29 M triangles. Female 284 structures, about 1.64 M triangles (509 k of these are two small lymph nodes modelled in great detail).

## Availability by structure

Counts are meshes whose name matches (vessel and nerve layers are excluded from organ/bone rows so that, for example, a pancreatic artery is not counted as pancreas). Name matching can over- or under-count, so treat these as indicative and see Findings for hand-checked statements.

| Requested structure | Male | Female |
|---|---|---|
| Brain (incl. sub-structures) | 53 | **missing** |
| Heart (chambers, septum, valves, papillary muscles) | 23 | 15 |
| Lung surface / lobes / bronchopulmonary segments | **missing** | 20 |
| Airways (bronchi, bronchial tree) | 100 | 48 |
| Trachea | 1 | 1 |
| Liver (main surface) | **missing** | **missing** |
| Liver (any part, excluding vessels) | 17 | 1 |
| Gallbladder | 1 | **missing** |
| Stomach | 1 | **missing** |
| Pancreas (organ) | 4 | **missing** |
| Spleen | 1 | 5 |
| Kidneys | 4 | 53 |
| Small intestine | 55 | **missing** |
| Large intestine | 7 | 9 |
| Urinary bladder | 1 | **missing** |
| Skull / cranial bones | 7 | **missing** |
| Vertebral column | 46 | 2 |
| Ribs / sternum | 29 | **missing** |
| Pelvic bones | 3 | 14 |
| Arm bones | 16 | **missing** |
| Hand bones | 14 | **missing** |
| Leg bones | 20 | **missing** |
| Foot bones | 18 | **missing** |
| Skeletal muscles (all, from system label) | 402 | **missing** |
| Tendons | 4 | **missing** |
| Ligaments | 18 | **missing** |
| Fascia / aponeurosis | 3 | **missing** |
| Male: testis, epididymis, deferent duct, prostate, seminal vesicle | 9 | **missing** |
| Female: uterus, ovary, fallopian tube, vagina | **missing** | **missing** |
| Mammary gland / breast | **missing** | **missing** |
| Thymus | 2 | 2 |
| Lymph nodes | **missing** | 10 |
| Adrenal / pituitary / pineal / thyroid gland | 4 | **missing** |
| Spinal cord | 1 | **missing** |
| Arteries / veins (all) | 1043 | 78 |
| Nerves (nervous layer, excluding brain) | 144 | **missing** |

## Findings
- Name-match caveats checked by hand: the female "liver" hit is the hepatic flexure of the colon (large intestine), the female "vertebral column" hits are the sacrum and coccyx, and the male skeletal-muscle count comes from the source's system label because most muscle names do not contain the word "muscle".
- **Male lungs and liver are incomplete.** The male data has the bronchial tree and lung vessels but no lung surface, and only the caudate lobe, bile ducts and hepatic vessels of the liver (the whole-liver and whole-lung meshes are not in this 2,234-mesh set).
- **Female lungs are present** (55 lung meshes: bronchi and bronchopulmonary segments, plus trachea and laryngeal cartilages) but the female liver, stomach, pancreas, small intestine, bladder and brain are not in the licensed data that could be obtained.
- **Female reproductive anatomy (uterus, ovaries, fallopian tubes, vagina, mammary glands) is not available.** The HuBMAP CCF v1.0 Visible Human Female release contains none of these, and later releases are hosted on a server this project could not reach. Nothing was substituted.
- **Female skeleton is the pelvis only (14 bone meshes); there are no female muscles or nerves.**
- **Male muscles are one layer** (402 muscle meshes plus 40 connective-tissue meshes). The source does not label superficial versus deep, so no such split is offered.
- **Male reproductive system is present:** testes, epididymides, deferent ducts, seminal vesicles, prostate and penile structures (12 meshes).
- **No textures, normal, roughness or ambient-occlusion maps exist in either source.** Materials are plain physically based colours chosen by this project per layer/organ.
- **Duplicates removed in the female model:** 37 vessel meshes appear in both the source heart file and the vasculature file with identical bounds (<2 mm); one copy is kept.
- One triangle was dropped from `Renal column (right)` by Meshopt repacking (all bounds identical).
- In the female heart, some great-vessel segments (carotid/subclavian/brachiocephalic parts) look detached from the aortic arch. That is how the source geometry is split, not a placement error introduced here.

## Orientation, scale and alignment checks
- Both models: Y-up, metres, feet at y = 0, anterior = +Z, patient's left = +X. Male checked from sternum vs vertebra z, kidney x and cerebellum z; female from kidney z/x. Male height 1.73 m; female 1.724 m (female arms are abducted, x ±0.52 m; male arms are at the sides).
- Female coordinates were shifted +0.8615 m vertically so the feet sit at y = 0; all female files share one coordinate frame (same Visible Human body).
- Relative positions were checked by eye in the browser (heart, lungs, spleen, kidneys, colon, pelvis in the female; the male organ cluster). They were **not** checked against published measurements, so proportions are not independently validated.
