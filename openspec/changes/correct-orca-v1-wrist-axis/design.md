## Context

The v1 simulation translates the articulated hand to the STEP wrist-bearing point `(74.728908451, 0, 104.871074582)` and currently rotates its geometry about local Y. The source assembly supplies no explicit joint semantics, but it does supply the complete wrist drive train: the XC430 wrist servo places its local Z pinion axis on world `+X`, and the carpal assembly rotates the 42-tooth gear's local Z axis onto world `-X`. Their centers share `y = 0` and `z ≈ 104.871 mm`, so the two opposite vectors describe one coaxial world-X hinge.

## Goals / Non-Goals

**Goals:**

- Rotate the complete hand around the evidenced world-X wrist axis.
- Add a mesh-based contract that fails for the former world-Y implementation.
- Preserve the wrist pivot, driver range, instructions, finger kinematics, and actual printable mesh inventory.

**Non-Goals:**

- Changing finger or thumb motion.
- Adding the omitted servo, gears, bearing, fasteners, skins, or electronics to the printable-parts simulation.
- Claiming calibrated wrist limits, torque, backlash, or actuator timing.

## Decisions

The wrist motion axis will be the constant `(1, 0, 0)` in the hand wrapper's frame. The wrapper is translated directly to the STEP wrist-bearing point, so its local axes remain aligned with the STEP world axes; rotating its geometry about local X therefore uses the drive train's world-X centerline. Keeping the existing bearing point is valid because it lies on the same infinite X-axis as the gear centers.

The regression contract will compare a printable palm mesh at wrist zero and at a nonzero wrist angle. Correct X-axis rotation preserves every vertex's X coordinate while changing its Y/Z coordinates; the old Y-axis rotation changes X. This measures rendered geometry and distinguishes the two implementations without introducing proxy geometry.

The driver and instructions remain unchanged because their values already represent signed visualization offsets in degrees. Only the physical axis used to interpret those values changes.

## Risks / Trade-offs

- The STEP document encodes placements rather than joints → The axis is cross-checked from both meshing wrist gears, whose transformed local Z axes are collinear and opposite.
- The executable simulation omits the drive gears → The contract measures the actual printable palm moved about the drive train centerline, while the source-derived axis calculation is recorded in measurements.
- Rotation sign may not match a hardware controller convention → Preserve the existing signed range and continue labelling it as a visualization offset, not calibrated control data.
