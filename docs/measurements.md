# ORCA v1 simulation measurements

The simulation loads the actual printable meshes under `orca_v1/`; it does not redraw, decimate, or approximate them. `orca_v1/ORCA_Assembly/ORCA_v1.step` supplies occurrence layout evidence only. These readings pin the sources and the imported occurrence transcription reviewed on 2026-09-10.

| Reading | Value |
| --- | ---: |
| STEP size | 41,262,983 bytes |
| STEP SHA-256 | `d34b5e7b51ff1b01765a02505de76bf3fd2babebd12bd7dd8e13d8014d49cf41` |
| STEP product adapters | 152 |
| STEP assembly adapters | 53 |
| Occurrence comments | 809 |
| Identity placements | 341 |

The imported root is `Assemblyhand_ORCA_v1 v30`. Its directly visible source children are the carpals, forearm/tower assembly, thumb, pinky, ring, middle, index, wrist bearing, and table-tennis demonstration ball. The executable simulation selects the printable palm, tower, and digit meshes. It excludes the demonstration ball and the silicone skins, motors, fasteners, bearings, and electronics that exist only as ambiguous or vendor STEP products.

## Producible mesh inventory

The published tree contains 23 instances from 12 unique source meshes:

| Source mesh | Instances |
| --- | ---: |
| `ORCA_Tower/BottomTower.stl` | 1 |
| `ORCA_Tower/R-TopTower.stl` | 1 |
| `ORCA_Tower/R-Carpals.stl` | 1 |
| `ORCA_Fingers/R-AP.stl` | 4 |
| `ORCA_Fingers/R-I-PP.stl` | 1 |
| `ORCA_Fingers/R-M-PP.stl` | 2 |
| `ORCA_Fingers/R-P-PP.stl` | 2 |
| `ORCA_Fingers/R-IP.stl` | 4 |
| `ORCA_Fingers/DP.stl` | 4 |
| `ORCA_Fingers/R-T-AP.stl` | 1 |
| `ORCA_Fingers/T-TP.stl` | 1 |
| `ORCA_Fingers/R-T-DP.stl` | 1 |

`simulation/source.py` records the byte size and SHA-256 of every unique mesh.
`simulation/test_source.py` fails if any source changes. `BottomTower.stl` is a
mesh pack with one positive-volume printable body and four zero-volume
components; the adapter selects reviewed body 0 without repairing it.

## Coordinate readings

All transforms are millimetres and degrees in the source STEP world frame. Representative root placements retained by the generated transcription are:

| Child | Rotation | Translation |
| --- | --- | --- |
| Carpals | 10° about `(1, 0, 0)` | `(38.628908451, -5.304184188, 143.252425156)` |
| Thumb | -90.109885746° about `(-0.389348058, 0.149615190, 0.908858286)` | `(10.419870212, 14.490185157, 133.329425210)` |
| Pinky | 122.527718822° about `(0.488917559, 0.700719645, -0.519568667)` | `(84.619258583, -3.421552771, 170.885229648)` |
| Ring | 126.319741078° about `(0.563308444, 0.643442165, -0.518329795)` | `(61.885787422, -10.593407483, 183.692509066)` |
| Middle | 125.931958320° about `(0.608120402, 0.608120402, -0.510273605)` | `(38.628908451, -13.986593071, 192.492812807)` |
| Index | 129.501001644° about `(0.623528122, 0.580747170, -0.523397941)` | `(14.537123521, -11.569695565, 188.002658784)` |
| Wrist bearing | 114.404497338° about `(-0.540716203, 0.644400478, -0.540716203)` | `(74.728908451, 0, 104.871074582)` |

These transforms locate the exported rest pose. The wrist bearing point is
`(74.728908451, 0, 104.871074582)`. The 42-tooth carpal gear center is
`(70.628908451, 0, 104.871074582)` and its transformed local Z axis is world
`-X`; those points share one wrist centerline. The XC430's 23-tooth pinion
center is `(64.728908451, -12, 75.206280633)`, 32 mm from the carpal gear in
the YZ plane, and its transformed local Z axis is world `+X`. The parallel,
opposite gear axes establish world X as the wrist rotation direction; the
existing bearing point remains a valid pivot because it lies on the carpal
gear's axis. The thumb base and proximal link share the local pivot
`(-23.640322608, 0, 18.469844260)` and common transformed axis
`(-0.578532546, 0.342020143, -0.740487890)`. Simulation controls add
visualization offsets to these frames; they are not calibrated hardware joint
values.

The source layout provides no evidenced finger-abduction joint, so the model
does not invent a spread motion. MCP and PIP flexion remain driven. DIP ports
are present and explicitly bound to zero because the available exports do not
identify a collision-free distal pivot.

## Reviewed contacts

At Rest, the only positive-volume mesh intersections are four source-seat
contacts between each `R-IP.stl` and `DP.stl` pair:

| Digit | Shared volume (mm³) |
| --- | ---: |
| Pinky | 0.000043930769 |
| Ring | 0.000072305371 |
| Middle | 0.000015547065 |
| Index | 0.000042081962 |

The one-second cadence scenario checks every transition through Rest, Open,
Fist, Open, Pinch, Open, and Point. It permits only those four named pairs and
rejects any contact over 0.001 mm³. An empty allowed-pair mutation fails as
expected.

## Framework findings

`solid import-step` exposed two framework warts: generated comment-only
`render()` methods do not parse, and name-only `StepNode` selectors cannot
address duplicate products (`SHELL` occurs 15 times). Both are recorded in
`solid-node/workflow/warts.md`. The project workaround retains the generated
tree as layout evidence and renders only its actual local producible meshes.
