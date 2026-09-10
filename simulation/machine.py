"""Complete printable ORCA v1 hand simulation."""

from solid_node.motion.ports import RotationalPort
from solid_node.node import AssemblyNode
from solid_node.simulation import Driver, Instruction

from .digits import Digits
from .parts import BottomTower, RightCarpals, RightTopTower


WRIST_PIVOT = (74.728908451, 0.0, 104.871074582)
WRIST_AXIS = (1.0, 0.0, 0.0)


def bind_intent(root):
    """Bind a root's four intent drivers to the complete port hierarchy."""

    digits = root.hand.digits
    root.connect(root.wrist, root.hand.wrist)

    index_factor = 1.0 - root.index_extension / 100.0
    finger_values = {
        digits.pinky: (-0.55, -0.75, 0.0),
        digits.ring: (-0.60, -0.80, 0.0),
        digits.middle: (-0.62, -0.82, 0.0),
        digits.index: (
            -0.55 * index_factor,
            -0.75 * index_factor,
            0.0,
        ),
    }
    for digit, (mcp, pip, dip) in finger_values.items():
        root.connect(root.grasp * mcp, digit.mcp)
        root.connect(root.grasp * pip, digit.pip)
        root.connect(root.grasp * dip, digit.dip)
        root.connect(0.0, digit.spread)

    thumb = digits.thumb
    root.connect(root.thumb_opposition, thumb.opposition)
    root.connect(0.0, thumb.mcp)
    root.connect(0.0, thumb.pip)


class ForearmTower(AssemblyNode):
    bottom = BottomTower()
    top = RightTopTower()

    def render(self):
        self.bottom.rotate(-90.0, (0.0, 1.0, 0.0))
        self.bottom.translate((40.628908451, 0.0, -40.628925418))
        self.top.rotate(90.0, (0.0, 0.0, 1.0))
        self.top.translate((40.628908451, 0.0, 64.871074582))


class HandGeometry(AssemblyNode):
    palm = RightCarpals()
    digits = Digits()

    def render(self):
        self.palm.rotate(10.0, (1.0, 0.0, 0.0))
        self.palm.translate((-36.1, -5.304184188, 38.381350574))


class ArticulatedHand(AssemblyNode):
    geometry = HandGeometry()
    wrist = RotationalPort(unit="deg")

    @property
    def digits(self):
        return self.geometry.digits

    def simulate(self):
        self.geometry.rotate(self.wrist.value, WRIST_AXIS)


class OrcaV1(AssemblyNode):
    """Builder-facing v1 model using exact repository meshes."""

    tower = ForearmTower()
    hand = ArticulatedHand()

    grasp = Driver(default=0.0, range=(0.0, 100.0), unit="percent")
    index_extension = Driver(default=0.0, range=(0.0, 100.0), unit="percent")
    thumb_opposition = Driver(default=0.0, range=(-10.0, 35.0), unit="deg")
    wrist = Driver(default=0.0, range=(-25.0, 25.0), unit="deg")

    instructions = {
        "Rest": Instruction(
            {"grasp": 0.0, "index_extension": 0.0, "thumb_opposition": 0.0, "wrist": 0.0},
            duration=2.0,
        ),
        "Open": Instruction(
            {"grasp": 0.0, "index_extension": 0.0, "thumb_opposition": 0.0, "wrist": 0.0},
            duration=2.0,
        ),
        "Fist": Instruction(
            {"grasp": 100.0, "index_extension": 0.0, "thumb_opposition": 15.0, "wrist": 0.0},
            duration=2.0,
        ),
        "Pinch": Instruction(
            {"grasp": 55.0, "index_extension": 20.0, "thumb_opposition": 30.0, "wrist": 0.0},
            duration=2.0,
        ),
        "Point": Instruction(
            {"grasp": 100.0, "index_extension": 100.0, "thumb_opposition": 10.0, "wrist": 0.0},
            duration=2.0,
        ),
    }

    def render(self):
        self.hand.translate(WRIST_PIVOT)

    def simulate(self):
        bind_intent(self)
