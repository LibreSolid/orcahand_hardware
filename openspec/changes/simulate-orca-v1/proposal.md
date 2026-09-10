## Why

The repository publishes the parts of the ORCA hand, but its drawings alone do not let a builder pose the complete mechanism or verify that its finger, palm, wrist, and forearm interfaces remain assembled through motion. The pilot requested: "simulate projects/Robotic-Hands/orcahand_hardware".

## What Changes

- Add a thin `simulation/` package that composes the printable right-hand ORCA v1 parts from their project-owned STL exports without changing upstream geometry, using the STEP occurrence tree only as placement evidence.
- Present the hand through intent-level controls for grasp, finger spread, thumb opposition, and wrist motion, with every moved joint represented by a bound kinematic port.
- Add a small `Rest`, `Open`, `Fist`, `Pinch`, and `Point` demonstration set with physically meaningful durations.
- Give the printable mechanism a consistent simulation colour scheme while retaining every selected STL's source geometry.
- Add assembly, motion, source-layout, and whole-model integrity contracts, including an explicit inventory for overlaps already present in the upstream assembly.
- Document the exact commands, controls, poses, ground-up model sequence, measurements, and design findings in the project README and simulation records.

## Capabilities

### New Capabilities

- `orca-v1-assembly`: The printable ORCA v1 right-hand mechanism is available from its authoritative STL geometry and STEP-derived occurrence placements, with its missing source relationships made explicit and testable.
- `orca-v1-joint-motion`: A maker can drive and demonstrate the hand in builder-facing terms while contracts verify the articulated interfaces and final pose targets.

### Modified Capabilities

None.

## Impact

The change adds project-owned OpenSpec records, `pyproject.toml`, a `simulation/` Python package, tests, measurements, README instructions, and ignore rules for solid-node outputs. It depends on the workspace solid-node installation, the existing printable exports under `orca_v1/`, and `orca_v1/ORCA_Assembly/ORCA_v1.step` as layout evidence; all upstream CAD, STL, 3MF, electronics, and scripts remain untouched. ORCA v2 and its touch, lite, and joint-sensing variants are out of scope because this repository does not include their assembly topology or joint frames; only v1 has a complete assembly source from which the simulation can be derived without inventing layout.
