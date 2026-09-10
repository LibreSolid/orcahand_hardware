## ADDED Requirements

### Requirement: Source-owned complete assembly
The simulation SHALL build the printable visible ORCA v1 right-hand mechanism from project-owned v1 STL exports, preserving their geometry and applying occurrence placements transcribed from `orca_v1/ORCA_Assembly/ORCA_v1.step` without editing upstream files.

#### Scenario: Build from the authoritative document
- **WHEN** a maker runs `solid build`
- **THEN** the published root contains the palm/tower, thumb, and four fingers composed from the v1 printable exports at their STEP-derived rest placements

### Requirement: Source drift is detectable
The simulation SHALL record the identities of the STEP layout source and selected STL geometry and SHALL fail its source contract when either source or its transcribed occurrence layout changes without a corresponding simulation review.

#### Scenario: Upstream assembly changes
- **WHEN** selected STL content, STEP content, or an occurrence transform differs from the reviewed measurement record
- **THEN** the source-layout contract fails and names the changed evidence

### Requirement: Producible geometry is exact
Every rendered manufactured component in scope SHALL use its actual project-owned producible mesh and SHALL NOT use a primitive, decimated, or hand-modelled visual approximation. Kinematic grouping nodes MAY be geometry-free.

#### Scenario: Published geometry is audited
- **WHEN** the published model's rendered leaves are inspected
- **THEN** each leaf names and loads the repository mesh for that manufactured part, and no rendered leaf substitutes proxy geometry

#### Scenario: A component lacks an unambiguous mesh
- **WHEN** a manufactured component cannot be mapped to one authoritative producible repository mesh
- **THEN** the component is explicitly excluded and documented rather than approximated

### Requirement: Mechanical integrity is explicit
Every selected printed solid SHALL be connected, and every positive-volume overlap between topmost rigid parts SHALL be represented in the reviewed upstream overlap inventory.

#### Scenario: A selected part becomes disconnected
- **WHEN** an imported selected printed part contains more than one disconnected solid
- **THEN** the solid-integrity contract fails and names the part

#### Scenario: The assembly overlap set changes
- **WHEN** a positive-volume overlap appears, disappears, or changes beyond its recorded measurement tolerance
- **THEN** the overlap-inventory contract fails and names the affected pair

### Requirement: Project-native operation
The project SHALL provide finite build, test, snapshot, control, pose, ground-up inspection, and findings instructions while keeping generated outputs outside version control.

#### Scenario: A maker follows the README
- **WHEN** a maker uses the documented workspace commands
- **THEN** the model builds, its contracts run, and rest and posed snapshots can be produced without modifying upstream design files
