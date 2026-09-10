## ADDED Requirements

### Requirement: Source-owned complete assembly
The simulation SHALL build the visible ORCA v1 right hand from `orca_v1/ORCA_Assembly/ORCA_v1.step`, preserving the document's product geometry, hierarchy, occurrence placements, and colours without editing upstream files.

#### Scenario: Build from the authoritative document
- **WHEN** a maker runs `solid build`
- **THEN** the published root contains the forearm, wrist, carpals, thumb, and four fingers imported from the v1 STEP document

### Requirement: Source drift is detectable
The simulation SHALL record the source document identity and SHALL fail its source contract when the imported STEP or its transcribed occurrence layout changes without a corresponding simulation review.

#### Scenario: Upstream assembly changes
- **WHEN** the STEP content or an occurrence transform differs from the reviewed measurement record
- **THEN** the source-layout contract fails and names the changed evidence

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
