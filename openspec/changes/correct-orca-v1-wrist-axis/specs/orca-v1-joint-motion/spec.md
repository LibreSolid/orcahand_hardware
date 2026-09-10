## MODIFIED Requirements

### Requirement: Motion follows evidenced pivots
The simulation SHALL move actual part meshes only around STEP-derived or geometry-evidenced joint pivots and axes, SHALL rotate the wrist around the coaxial world-X servo-pinion and carpal-gear axis, and SHALL NOT invent finger abduction where the source assembly provides no such joint.

#### Scenario: Point pose extends the index
- **WHEN** the `Point` instruction closes the other fingers
- **THEN** `index_extension` counteracts index MCP/PIP flexion while all finger spread ports remain explicitly bound to zero

#### Scenario: Wrist motion follows its drive train
- **WHEN** a nonzero `wrist` state rotates the hand from its STEP-derived rest pose
- **THEN** printable hand meshes rotate around the wrist drive train's world-X centerline without motion along that axis
