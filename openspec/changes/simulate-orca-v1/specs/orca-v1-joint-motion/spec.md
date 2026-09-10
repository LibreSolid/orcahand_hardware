## ADDED Requirements

### Requirement: Intent-level control surface
The simulation SHALL expose at most four root drivers named `grasp`, `spread`, `thumb_opposition`, and `wrist`, with units and ranges that state their visualization meaning.

#### Scenario: Maker inspects controls
- **WHEN** the model is published to `viewer.json`
- **THEN** the driver table contains exactly those four qualified root ids with their declared defaults, ranges, and units

### Requirement: Joint motion remains reachable
Every articulated finger and wrist motion SHALL be represented by a bound port, including ports held at zero in the current intent mapping.

#### Scenario: Root wiring is complete
- **WHEN** any supported driver state is evaluated
- **THEN** every declared joint port has a numeric or symbolic binding and no node substitutes an unbound port with zero

### Requirement: Demonstration poses
The simulation SHALL provide `Rest`, `Open`, `Fist`, `Pinch`, and `Point` instructions that land exactly on their declared targets and route coordinated closing moves through the open state when required for clearance.

#### Scenario: Pose sequence completes
- **WHEN** the scenario triggers Rest, Open, Fist, Open, Pinch, Open, and Point in order
- **THEN** each instruction lands exactly on its targets and the hand remains within the reviewed overlap inventory at every sampled instant

### Requirement: Motion semantics are honest
Driver angles SHALL be documented as visualization offsets from the STEP rest pose and SHALL NOT be presented as calibrated ORCA hardware commands.

#### Scenario: Maker reads control documentation
- **WHEN** the maker reviews the simulation controls
- **THEN** the documentation distinguishes simulation offsets from robot joint calibration and identifies the unmodeled tendon and control dynamics
