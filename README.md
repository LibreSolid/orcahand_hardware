<p align="center">
  <img src="assets/banner.png" alt="ORCA Hand" width="100%"/>
</p>

<div align="center" style="line-height: 1;">
  <a href="https://arxiv.org/abs/2504.04259" target="_blank"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2504.04259-B31B1B?logo=arxiv"/></a>
  <a href="https://discord.gg/xvGyxaccRa" target="_blank"><img alt="Discord" src="https://img.shields.io/badge/Discord-orcahand-7289da?logo=discord&logoColor=white&color=7289da"/></a>
  <a href="https://x.com/orcahand" target="_blank"><img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/orcahand?style=social"/></a>
  <a href="https://orcahand.com" target="_blank"><img alt="Website" src="https://img.shields.io/badge/Website-orcahand.com-blue?style=flat&logo=google-chrome"/></a>
  <br>
  <a href="https://github.com/orcahand/orca_files" target="_blank"><img alt="GitHub stars" src="https://img.shields.io/github/stars/orcahand/orca_files?style=social"/></a>
</div>

# ORCA Hand Files

CAD and print files for the ORCA robotic hand.

The ORCA Hand now supports both **Feetech** and **Dynamixel** servos. Every printable variant ships two ready-to-print plates — `*-FT.3mf` for Feetech and `*-DX.3mf` for Dynamixel — so you can build the hand around whichever actuators you have. STL sources are shared across both; only the motor-specific parts (forearm/wrist structures, adapters) differ between the FT and DX plates.

## Structure

```
orca_v2/                          # Current ORCA hand — shared base + variants
  base/                           # Canonical full hand
    Prints-1000-DX.3mf            # Dynamixel print plate
    Prints-1000-FT.3mf            # Feetech print plate
    Clips-Only.3mf
    01_Fingers/*.stl              # STL source files in subdirs
    02_Carpals/*.stl
    03_Wrist/*.stl
    04_ForeArm/*.stl
    05_Spools/*.stl
    07_Molds/*.stl
    ...
  touch/                          # Touch-sensor variant
    Prints-2000-DX.3mf            # Pulls base + touch STLs in one pass
    Prints-2000-FT.3mf
    01_Fingers/*-Touch.stl        # Override STLs only
    02_Carpals/*.stl
  lite/                           # Lite variant — STL sources (3MFs TBD)
    01_ForeArm/*.stl
    02_Spools/Lite-*.stl
  joint-sensing/                  # Joint-sensing variant — STL sources (3MFs TBD)
    01_Fingers/*JS*.stl

orca_v1/                         # V1 design (self-contained)
  Print_Files_Bambu/*.3mf         # Print files in dedicated subdir
  ORCA_Fingers/*.stl              # STLs in sibling dirs
  ORCA_Tower/*.stl
  ...
```

Variant 3MFs under `orca_v2/<variant>/` automatically resolve part names against the whole `orca_v2/` tree, so they pick up shared STLs from `orca_v2/base/` without duplication. Edit a base STL once and every variant 3MF that references it gets updated.

## ORCA v1 Simulation

`simulation/` adds a solid-node model of the printable right-hand v1
mechanism. Every one of its 23 rendered leaves loads the actual repository
STL for that manufactured part. The simulation does not substitute boxes,
cylinders, envelopes, decimated meshes, or other visual proxies. Empty
assembly nodes supply kinematics only.

The v1 STEP document supplies the authoritative occurrence layout. It is not
used as executable geometry because its generated adapters cannot currently
select repeated product names such as `SHELL`. The imported transcription is
kept under `simulation/v1/` as reviewable placement evidence; source hashes,
placements, exclusions, and measured contacts are recorded in
[`docs/measurements.md`](docs/measurements.md).

From this project directory in a LibreSolid Studio development workspace:

```bash
# Source identities and layout transcription
../../../.venv/bin/python -m unittest simulation.test_source -v

# Fast development contracts and the complete motion scenario
../../../.venv/bin/solid test --faceted simulation/fixed.py:FixedLowerAssembly
../../../.venv/bin/solid test --faceted simulation/machine.py:OrcaV1

# Publish the interactive model
../../../.venv/bin/solid build simulation/machine.py:OrcaV1

# Visual evidence from actual part meshes
../../../.venv/bin/solid snapshot simulation/machine.py:OrcaV1 -o snapshot-v1-rest.png --autocenter --viewall
../../../.venv/bin/solid snapshot simulation/poses.py:FistPose -o snapshot-v1-fist.png --autocenter --viewall
../../../.venv/bin/solid snapshot simulation/poses.py:PointPose -o snapshot-v1-point.png --autocenter --viewall
../../../.venv/bin/solid snapshot simulation/machine.py:OrcaV1 -o snapshot-v1-axes.png --autocenter --viewall --view axes
```

The viewer exposes four intent controls:

| Control | Range | Meaning |
| --- | ---: | --- |
| `grasp` | 0–100% | Coordinated MCP/PIP flexion of the four fingers |
| `index_extension` | 0–100% | Counteracts index flexion for the Point pose |
| `thumb_opposition` | -10–35° | Thumb rotation about the evidenced base/proximal hinge |
| `wrist` | -25–25° | Hand rotation about the STEP-derived wrist pivot |

`Rest`, `Open`, `Fist`, `Pinch`, and `Point` are two-second viewer
instructions. Their values are visualization offsets from the exported rest
pose, not calibrated hardware commands. Tendons, compliance, servo rates,
forces, tactile sensing, and controller dynamics are not simulated.

For ground-up inspection, start with
`simulation/fixed.py:FixedLowerAssembly`, then inspect
`simulation/machine.py:OrcaV1` at Rest, and finally compare the standalone
`FistPose` and `PointPose` snapshot roots. Generated `_build/` content and
`snapshot*.png` files are ignored.

## Updating Print Files After STL Changes

```bash
# Find which 3MF(s) contain a given STL (cascades across variants)
python3 scripts/find_3mf_for_file.py orca_v2/base/05_Spools/BaseSpool.stl

# Update all parts in a 3MF from source STLs (variants pull base parts too)
python3 scripts/update_3mf.py orca_v2/touch/Prints-2000-DX.3mf --all

# Preview without writing
python3 scripts/update_3mf.py orca_v2/base/Prints-1000-DX.3mf --all --dry-run

# List parts inside a 3MF
python3 scripts/update_3mf.py orca_v2/base/Prints-1000-DX.3mf --list
```

## License

Copyright (c) 2026 ORCA Dexterity, Inc.

All files in this repository — hardware designs (CAD/STL/3MF) and source code —
are licensed under the [Creative Commons Attribution 4.0 International License
(CC BY 4.0)](LICENSE). You may share and adapt the material for any purpose,
including commercially, with appropriate credit. No patent or trademark rights
are granted.
