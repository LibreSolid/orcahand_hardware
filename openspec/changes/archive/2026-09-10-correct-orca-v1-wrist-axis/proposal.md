## Why

The ORCA v1 viewer currently rotates the hand about world Y, but the source assembly places the wrist servo pinion and carpal gear on parallel world-X axes, with the carpal gear coaxial to the wrist bearing. The wrist control therefore depicts the wrong mechanical degree of freedom and must follow the evidenced carpal-gear axis.

## What Changes

- Correct wrist motion to rotate the complete hand about the STEP-derived world-X wrist axis.
- Add a geometric contract that distinguishes the correct wrist axis from the former world-Y axis.
- Rebuild and visually inspect the wrist poses while preserving every actual producible part mesh and all existing finger motion.
- Correct the wrist-axis description and measurements in project documentation.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `orca-v1-joint-motion`: Require wrist motion to follow the carpal gear and wrist bearing's world-X axis evidenced by the v1 STEP assembly.

## Impact

This changes only the project-owned v1 simulation, its contracts, measurements, README, and OpenSpec records. Upstream CAD/STL/3MF files, printable mesh selection, finger kinematics, framework code, and the public four-driver control surface remain unchanged.
