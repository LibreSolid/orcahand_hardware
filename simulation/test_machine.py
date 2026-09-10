"""Whole-machine contracts for the ORCA v1 simulation."""

from solid_node.motion.ports import declared_ports
from solid_node.simulation import ScenarioTest, qualified_drivers, qualified_instructions
from solid_node.test import TestCase

from .machine import OrcaV1
from .seats import (
    assert_only_reviewed_joint_contacts,
    assert_rest_overlap_inventory,
)
from .source import actual_mesh_inventory


class OrcaV1Test(TestCase):
    node = OrcaV1

    def test_solid_integrity(self):
        self.assertNoDisconnectedSolids(self.node)

    def test_every_rendered_leaf_is_an_actual_producible_mesh(self):
        self.assertEqual(
            actual_mesh_inventory(self.node),
            {
                "../orca_v1/ORCA_Tower/BottomTower.stl": 1,
                "../orca_v1/ORCA_Tower/R-TopTower.stl": 1,
                "../orca_v1/ORCA_Tower/R-Carpals.stl": 1,
                "../orca_v1/ORCA_Fingers/R-AP.stl": 4,
                "../orca_v1/ORCA_Fingers/R-I-PP.stl": 1,
                "../orca_v1/ORCA_Fingers/R-M-PP.stl": 2,
                "../orca_v1/ORCA_Fingers/R-P-PP.stl": 2,
                "../orca_v1/ORCA_Fingers/R-IP.stl": 4,
                "../orca_v1/ORCA_Fingers/DP.stl": 4,
                "../orca_v1/ORCA_Fingers/R-T-AP.stl": 1,
                "../orca_v1/ORCA_Fingers/T-TP.stl": 1,
                "../orca_v1/ORCA_Fingers/R-T-DP.stl": 1,
            },
        )

    def test_assembly_integrity(self):
        self.node.set_state(
            grasp=0.0,
            index_extension=0.0,
            thumb_opposition=0.0,
            wrist=0.0,
        )
        assert_rest_overlap_inventory(self.node)

    def test_overlap_inventory_mutation_is_rejected(self):
        self.node.set_state(
            grasp=0.0,
            index_extension=0.0,
            thumb_opposition=0.0,
            wrist=0.0,
        )
        with self.assertRaises(AssertionError):
            assert_only_reviewed_joint_contacts(self.node, allowed_pairs=())

    def test_all_five_digits_are_present(self):
        self.assertEqual(
            [child.name for child in self.node.hand.digits.children],
            ["thumb", "pinky", "ring", "middle", "index"],
        )

    def test_finger_ports_are_named(self):
        for name in ("pinky", "ring", "middle", "index"):
            digit = getattr(self.node.hand.digits, name)
            self.assertEqual(
                set(declared_ports(type(digit))),
                {"mcp", "pip", "dip", "spread"},
            )

    def test_thumb_and_wrist_ports_are_named(self):
        self.assertEqual(
            set(declared_ports(type(self.node.hand.digits.thumb))),
            {"mcp", "pip", "opposition"},
        )
        self.assertEqual(set(declared_ports(type(self.node.hand))), {"wrist"})

    def test_every_port_is_bound_at_defaults(self):
        self.node.set_state()
        for name in ("pinky", "ring", "middle", "index"):
            digit = getattr(self.node.hand.digits, name)
            for port in declared_ports(type(digit)):
                self.assertIsNotNone(getattr(digit, port).value, f"{name}.{port}")
        thumb = self.node.hand.digits.thumb
        for port in declared_ports(type(thumb)):
            self.assertIsNotNone(getattr(thumb, port).value, f"thumb.{port}")
        self.assertIsNotNone(self.node.hand.wrist.value, "hand.wrist")

    def assert_positive_index_flexion(self, grasp):
        distal = self.node.hand.digits.index.motion.tip.distal
        self.node.set_state(
            grasp=0.0, index_extension=0.0, thumb_opposition=0.0, wrist=0.0
        )
        rest_z = float(distal.mesh.centroid[2])
        self.node.set_state(
            grasp=grasp, index_extension=0.0, thumb_opposition=0.0, wrist=0.0
        )
        posed_z = float(distal.mesh.centroid[2])
        self.assertLess(posed_z - rest_z, -60.0)

    def test_positive_grasp_flexes_the_index_inward(self):
        self.assert_positive_index_flexion(100.0)

    def test_sign_flipped_grasp_is_rejected(self):
        with self.assertRaises(AssertionError):
            self.assert_positive_index_flexion(-100.0)

    def test_control_surface_has_exactly_four_intent_drivers(self):
        self.assertEqual(
            set(qualified_drivers(self.node)),
            {"grasp", "index_extension", "thumb_opposition", "wrist"},
        )

    def test_demonstration_set_is_complete(self):
        self.assertEqual(
            set(qualified_instructions(self.node)),
            {"Rest", "Open", "Fist", "Pinch", "Point"},
        )


class OrcaV1InstructionTest(ScenarioTest):
    node = OrcaV1
    dt = 0.1
    meshes = True

    def test_each_instruction_lands_exactly(self):
        targets = {
            "Rest": (0.0, 0.0, 0.0, 0.0),
            "Open": (0.0, 0.0, 0.0, 0.0),
            "Fist": (100.0, 0.0, 15.0, 0.0),
            "Pinch": (55.0, 20.0, 30.0, 0.0),
            "Point": (100.0, 100.0, 10.0, 0.0),
        }
        for instruction, expected in targets.items():
            sim = self.simulation()
            sim.at(0.0).trigger(instruction)
            sim.run(2.0)
            self.assertEqual(
                tuple(sim.state[name] for name in (
                    "grasp", "index_extension", "thumb_opposition", "wrist"
                )),
                expected,
            )

    def test_demonstration_sequence_keeps_only_reviewed_contacts(self):
        sim = self.simulation()
        for time, instruction in (
            (0.0, "Rest"),
            (2.0, "Open"),
            (4.0, "Fist"),
            (6.0, "Open"),
            (8.0, "Pinch"),
            (10.0, "Open"),
            (12.0, "Point"),
        ):
            sim.at(time).trigger(instruction)
        sim.every(1.0, assert_only_reviewed_joint_contacts, self.node)
        sim.run(14.0)
