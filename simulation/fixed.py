"""Fixed printable palm and tower at ORCA v1 STEP-derived placements."""

from solid_node.node import AssemblyNode

from .parts import BottomTower, RightCarpals, RightTopTower


class FixedLowerAssembly(AssemblyNode):
    """Actual producible meshes before the articulated digits are added."""

    bottom_tower = BottomTower()
    top_tower = RightTopTower()
    carpals = RightCarpals()

    def render(self):
        self.bottom_tower.rotate(-90.0, (0.0, 1.0, 0.0))
        self.bottom_tower.translate((40.628908451, 0.0, -40.628925418))

        self.top_tower.rotate(90.0, (0.0, 0.0, 1.0))
        self.top_tower.translate((40.628908451, 0.0, 64.871074582))

        self.carpals.rotate(10.0, (1.0, 0.0, 0.0))
        self.carpals.translate((38.628908451, -5.304184188, 143.252425156))
