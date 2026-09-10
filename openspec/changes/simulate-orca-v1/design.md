## Context

The repository contains two design generations. `orca_v2/base` is the current product but contains only part-local STL and STEP exports: it has no assembly hierarchy, occurrence placements, joint frames, or control ranges. `orca_v1/ORCA_Assembly/ORCA_v1.step` is the only complete machine source. It names the right-hand assembly `Assemblyhand_ORCA_v1 v30`, preserves the complete hierarchy and occurrence transforms, and includes printed parts, silicone skins, bearings, fasteners, motors, electronics, wrist, and forearm.

The v1 STEP is nevertheless not directly buildable through the current public import surface. The importer emits comment-only `render()` methods, and its generated name selectors cannot distinguish repeated products such as the fifteen products named `SHELL`. The simulation therefore uses project-owned v1 STL exports as geometry and treats the imported STEP occurrence tree as layout evidence only. Generated Python remains a readable transcription of the STEP occurrence transforms; it is not the executable model.

### Coordinates

- The machine frame is the STEP document's world frame in millimetres.
- The forearm remains at the document identity; the hand/wrist group uses the document's wrist placement as its rest transform.
- Joint zero poses are transcribed from the STEP assembly's occurrence transforms. Rotation axes are explicit simulation assumptions aligned with the visible hinge geometry because the STEP occurrence tree carries placements but no joint semantics. A driver value is an added angle in degrees from that exported rest pose, not an absolute robot-control calibration value.
- `grasp` is a 0–100 percent intent that maps to the four fingers' MCP/PIP flexion ports with digit-specific limits; `spread`, `thumb_opposition`, and `wrist` are degrees added about their named rest axes.
- A named 0.05 mm `SEAT_CLEARANCE` distinguishes seated faces from accidental positive-volume overlap where the exported source leaves coincident mating faces.

## Goals / Non-Goals

**Goals:**

- Build the printable visible v1 right-hand mechanism from its existing STL exports and STEP-derived occurrence transforms.
- Render every in-scope manufactured component from its actual repository mesh; use no primitive, decimated, or hand-modelled visual proxy for a producible part.
- Keep finger and wrist joint inputs reachable through ports while exposing no more than four maker-facing intent controls.
- Provide five concise poses that land exactly on their declared targets and exercise independent and coordinated movement.
- Prove that the selected STL geometry and imported layout evidence have not drifted, every selected printed solid is connected, the assembly's expected overlap inventory is stable, and pose targets are reached.
- Publish a finite build, inspect rest and posed snapshots, and document the source limitations the simulation reveals.

**Non-Goals:**

- ORCA v2, touch, lite, and joint-sensing models; their assembly topology and joint frames are absent from this repository.
- Force, tendon elasticity, tactile sensing, motor current, controller calibration, or contact dynamics.
- Repairing or regenerating upstream CAD, STL, STEP, 3MF, electronics, or scripts.
- Replacing a repository part mesh with a box, cylinder, envelope, decimation, or other low-level visual approximation.
- Silicone skins, motors, fasteners, bearings, and electronics that exist only as ambiguous or vendor STEP products; the simulation represents the printable mechanism rather than a bill-of-materials-complete digital twin.
- Claiming that simulation angles are calibrated hardware commands or manufacturing validation.

## Decisions

### Use printable STLs with STEP-derived placements

Run the documented `solid import-step` command into `simulation/v1/` and keep its generated `parts.py` and `assembly.py` as non-executable source-layout evidence. Project-owned wrappers load the printable v1 STL exports and apply the generated matrix-derived rotate/translate pairs. This preserves the geometry that builders actually print and the only available authoritative assembly placement without relying on ambiguous STEP product names. Source contracts pin both selected STLs and the STEP/layout transcription.

Every rendered leaf maps to a concrete repository mesh for that manufactured part. Assemblies and empty transform nodes may carry kinematics, but they contribute no proxy geometry. If a required manufactured component has no unambiguous producible mesh, it is reported as out of scope instead of approximated.

### Put motion around source-owned rest placement

Project-owned wrappers retain `render()` exclusively for the source rest placement. Small articulated assemblies add ports and `simulate()` operations around that placement. The root binds all ports, including ports held at zero by a pose. This keeps rest geometry auditable and prevents animation values from entering artifact identity.

### Expose intent rather than seventeen motor channels

Four root controls are sufficient for the demonstration: grasp percentage, finger spread, thumb opposition, and wrist angle. Digit classes retain MCP/PIP/DIP-style ports so later slices can expose independent joints without restructuring. The pose set is `Rest`, `Open`, `Fist`, `Pinch`, and `Point`; transitions use two seconds, reflecting visible servo motion without claiming a measured actuator rate.

### Treat upstream overlap as data

The printable STL set can contain seated and joint-interface intersections. `simulation/seats.py` records the pair names and measured rest-pose shared volumes found by the first exact inventory. Tests require the same set and volumes within a documented measurement tolerance; no overlap is waived by an epsilon. New, changed, or removed overlaps all require an explicit design finding.

### Use an explicit simulation material scheme

STL exports carry no material colours, so printable parts receive a consistent project-owned palette that distinguishes the palm/tower, digits, and joint pieces without implying source material data. Non-geometric wrapper assemblies exist only to group the forearm and articulated hand and therefore add no display solids.

## Findings

- All sampled v2 STL files are watertight after normal mesh processing but are exported in part-local frames; their origins alone do not locate the parts on the palm.
- Every sampled v2 STEP file is an unnamed single product rather than an occurrence tree, so it cannot recover a joint relation through `solid import-step`.
- The v1 STEP is a complete occurrence tree and is sufficient to recover the right-hand rest assembly without external repositories.
- The v1 finger, tower, palm, spool, and ancillary STL exports inspected for the fallback are watertight; `BottomTower.stl` includes four zero-volume mesh bodies in addition to its printable body, so its wrapper selects body 0 explicitly.
- A disposable seven-piece v1 probe built successfully from STL geometry and STEP-derived placements and produced coherent palm, tower, and index-finger snapshots at rest and under symbolic curl.
- The installed framework exposes the documented `solid import-step` CLI but does not export `StepAssembly` from `solid_node.node`; generated `StepNode` wrappers also fail on repeated product names, so the executable simulation avoids those interfaces.

### Findings for the framework

- `solid import-step` emits syntactically invalid comment-only `render()` methods; generated methods need an inert statement such as `pass`.
- Name-only `StepNode` selection cannot address repeated STEP products such as the fifteen ORCA products named `SHELL`; the importer needs a stable product or occurrence selector and should emit it.
- Both findings and the project workaround are recorded in `solid-node/workflow/warts.md`.

## Risks / Trade-offs

- **The v1 document is large and contains repeated vendor subassemblies** → Keep its generated adapters as layout evidence only and build the selected printable mechanism from local STL exports.
- **The layout transcription is manual evidence at the executable boundary** → Pin the STEP and selected STL identities, contract representative placements, and require review when either changes.
- **Rest-pose intersections may be numerous** → Generate and review an explicit inventory once, then contract the exact names and volumes.
- **Adding rotations to an exported posed assembly can reveal collisions** → Sample the instruction scenario at fixed cadence and route unsafe direct transitions through `Open`.
- **The source does not publish joint limits or actuator speed** → Use conservative demonstration ranges labelled as visualization offsets and state that they are not hardware calibration values.
