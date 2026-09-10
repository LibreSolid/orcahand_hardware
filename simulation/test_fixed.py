"""Contracts for the source-placed printable palm and tower."""

from solid_node.test import TestCase

from .fixed import FixedLowerAssembly
from .source import assert_actual_meshes


class FixedLowerAssemblyTest(TestCase):
    node = FixedLowerAssembly

    def assert_bounds(self, node, expected):
        for actual_row, expected_row in zip(node.mesh.bounds, expected):
            for actual, target in zip(actual_row, expected_row):
                self.assertAlmostEqual(float(actual), target, places=5)

    def test_required_subassemblies_are_present(self):
        self.assertEqual(
            [child.name for child in self.node.children],
            ["bottom_tower", "top_tower", "carpals"],
        )

    def test_every_leaf_is_its_actual_producible_mesh(self):
        assert_actual_meshes(
            self.node,
            {
                "bottom_tower": "../orca_v1/ORCA_Tower/BottomTower.stl",
                "top_tower": "../orca_v1/ORCA_Tower/R-TopTower.stl",
                "carpals": "../orca_v1/ORCA_Tower/R-Carpals.stl",
            },
        )

    def test_carpals_keep_the_source_placement(self):
        self.assert_bounds(
            self.node.carpals,
            (
                (-11.933335964, -20.422961081, 95.021255043),
                (91.041425999, 21.715284673, 178.043128731),
            ),
        )

    def test_tower_keeps_the_source_placement(self):
        self.assert_bounds(
            self.node.top_tower,
            (
                (-0.571092312, -48.0, 64.871074582),
                (81.828909214, 48.0, 109.875217343),
            ),
        )

    def test_placement_mutation_is_rejected(self):
        moved = FixedLowerAssembly()
        moved.assemble()
        moved.build_stls()
        moved.carpals.translate((1.0, 0.0, 0.0))
        with self.assertRaises(AssertionError):
            self.assert_bounds(
                moved.carpals,
                (
                    (-11.933335964, -20.422961081, 95.021255043),
                    (91.041425999, 21.715284673, 178.043128731),
                ),
            )

    def test_proxy_geometry_substitution_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, "loads"):
            assert_actual_meshes(
                self.node,
                {
                    "bottom_tower": "proxy.stl",
                    "top_tower": "../orca_v1/ORCA_Tower/R-TopTower.stl",
                    "carpals": "../orca_v1/ORCA_Tower/R-Carpals.stl",
                },
            )
