## Context

The repository contains two design generations. `orca_v2/base` is the current product but contains only part-local STL and STEP exports: it has no assembly hierarchy, occurrence placements, joint frames, or control ranges. `orca_v1/ORCA_Assembly/ORCA_v1.step` is the only complete machine source. It names the right-hand assembly `Assemblyhand_ORCA_v1 v30`, preserves the complete hierarchy and occurrence transforms, and includes printed parts, silicone skins, bearings, fasteners, motors, electronics, wrist, and forearm.

The simulation therefore imports the v1 document as-is through `solid import-step`, then adds only project-owned kinematic wiring and documentation. The source STEP remains authoritative for geometry, colour, hierarchy, and rest placement. Generated Python is a readable transcription of the STEP occurrence tree, not a copied or redrawn design.

### Coordinates

- The machine frame is the STEP document's world frame in millimetres.
- The forearm remains at the document identity; the hand/wrist group uses the document's wrist placement as its rest transform.
- Joint axes and zero poses are the axes and transforms stored by the STEP assembly. A driver value is an added angle in degrees from that exported rest pose, not an absolute robot-control calibration value.
- `grasp` is a 0–100 percent intent that maps to the four fingers' MCP/PIP flexion ports with digit-specific limits; `spread`, `thumb_opposition`, and `wrist` are degrees added about their named rest axes.
- A named 0.05 mm `SEAT_CLEARANCE` distinguishes seated faces from accidental positive-volume overlap where the exported source leaves coincident mating faces.

## Goals / Non-Goals

**Goals:**

- Build the complete visible v1 right hand from the existing STEP products and occurrence transforms.
- Keep finger and wrist joint inputs reachable through ports while exposing no more than four maker-facing intent controls.
- Provide five concise poses that land exactly on their declared targets and exercise independent and coordinated movement.
- Prove that the imported source has not drifted, every selected printed solid is connected, the assembly's expected overlap inventory is stable, and pose targets are reached.
- Publish a finite build, inspect rest and posed snapshots, and document the source limitations the simulation reveals.

**Non-Goals:**

- ORCA v2, touch, lite, and joint-sensing models; their assembly topology and joint frames are absent from this repository.
- Force, tendon elasticity, tactile sensing, motor current, controller calibration, or contact dynamics.
- Repairing or regenerating upstream CAD, STL, STEP, 3MF, electronics, or scripts.
- Claiming that simulation angles are calibrated hardware commands or manufacturing validation.

## Decisions

### Import the v1 STEP hierarchy once

Run the documented `solid import-step` command into `simulation/v1/` and keep its generated `parts.py` and `assembly.py` as the source-layout transcription. This preserves source product names and matrix-derived rotate/translate pairs, and edits to the STEP invalidate every dependent node. Hand-writing parts or using the v2 print STLs would either duplicate geometry or invent missing placements.

### Put motion around source-owned rest placement

The generated classes retain `render()` exclusively for STEP rest placement. Small project-owned subclasses/wrappers add ports and `simulate()` operations inside that placement. The root binds all ports, including ports held at zero by a pose. This keeps rest geometry auditable and prevents animation values from entering artifact identity.

### Expose intent rather than seventeen motor channels

Four root controls are sufficient for the demonstration: grasp percentage, finger spread, thumb opposition, and wrist angle. Digit classes retain MCP/PIP/DIP-style ports so later slices can expose independent joints without restructuring. The pose set is `Rest`, `Open`, `Fist`, `Pinch`, and `Point`; transitions use two seconds, reflecting visible servo motion without claiming a measured actuator rate.

### Treat upstream overlap as data

The full STEP contains intentional nested skins, fasteners, bearings, and seated components. `simulation/seats.py` records the pair names and measured rest-pose shared volumes found by the first exact inventory. Tests require the same set and volumes within a documented measurement tolerance; no overlap is waived by an epsilon. New, changed, or removed overlaps all require an explicit design finding.

### Preserve source colours and identify simulation-only groups

STEP products use their embedded colours. No upstream material colour is overridden. Non-geometric wrapper assemblies exist only to group the forearm and articulated hand and therefore add no display solids.

## Findings

- All sampled v2 STL files are watertight after normal mesh processing but are exported in part-local frames; their origins alone do not locate the parts on the palm.
- Every sampled v2 STEP file is an unnamed single product rather than an occurrence tree, so it cannot recover a joint relation through `solid import-step`.
- The v1 STEP is a complete occurrence tree and is sufficient to recover the right-hand rest assembly without external repositories.
- The installed framework exposes the documented `solid import-step` CLI but does not export `StepAssembly` from `solid_node.node`; the simulation avoids that unavailable Python import.

### Findings for the framework

- The public API description should identify the supported import path for `StepAssembly`, or the package should export it from the documented namespace. The project uses the supported CLI as its workaround.

## Risks / Trade-offs

- **The v1 document is large and contains repeated vendor subassemblies** → Keep generated adapters mechanical, use coarse STEP tessellation, and test the selected machine rather than every generated class independently.
- **The source may contain product-name ambiguity or unsupported placements** → Stop on the importer/build error and record it; do not guess a framework interface or repair the STEP.
- **Rest-pose intersections may be numerous** → Generate and review an explicit inventory once, then contract the exact names and volumes.
- **Adding rotations to an exported posed assembly can reveal collisions** → Sample the instruction scenario at fixed cadence and route unsafe direct transitions through `Open`.
- **The source does not publish joint limits or actuator speed** → Use conservative demonstration ranges labelled as visualization offsets and state that they are not hardware calibration values.
