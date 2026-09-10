## 1. Project and source contract

- [ ] 1.1 Add the manifest, simulation package skeleton, ignore rules, and root integrity tests; run the faceted tests red before a root exists.
- [ ] 1.2 Import the v1 STEP occurrence tree with `solid import-step`, record the source digest and occurrence measurements, and make the source-drift contract green.

## 2. Fixed lower assembly

- [ ] 2.1 Add red contracts for the forearm, wrist bearing, and carpals presence and source placement.
- [ ] 2.2 Compose the fixed lower assembly from imported nodes, make its contracts green, and verify a placement mutation fails them.

## 3. Articulated hand

- [ ] 3.1 Add red contracts for digit presence, named joint ports, and complete root wiring.
- [ ] 3.2 Add finger and thumb port-driven motion on top of source rest transforms and make the wiring contracts green.
- [ ] 3.3 Verify a deliberately omitted or sign-flipped joint binding fails the intended contract, restore it, and record the mutation result.

## 4. Controls and demonstration

- [ ] 4.1 Add red tests for the four-driver control surface, five instruction targets, and exact pose landing.
- [ ] 4.2 Implement the intent mapping and `Rest`, `Open`, `Fist`, `Pinch`, and `Point` instructions, then make the pose tests green.
- [ ] 4.3 Run the instruction scenario on a fixed cadence, establish and review the source-overlap inventory, and verify an inventory mutation fails.

## 5. Delivery evidence

- [ ] 5.1 Run the full faceted regression for every simulation node file and inspect `solid build` plus `viewer.json` for the complete tree, operations, drivers, instructions, and model files.
- [ ] 5.2 Render and inspect rest and posed isometric snapshots plus an alignment-axis view; keep all generated images and build artifacts ignored.
- [ ] 5.3 Document commands, controls, poses, ground-up models, measurements, limitations, and findings in the README and simulation docs.
- [ ] 5.4 Run the full exact regression once, validate the OpenSpec change, sync its delta specs, archive it, and commit the delivered clean state.
