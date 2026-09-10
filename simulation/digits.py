"""Port-driven ORCA v1 digits built only from producible source meshes."""

from solid_node.motion.ports import RotationalPort
from solid_node.node import AssemblyNode

from .parts import (
    FingerBase,
    FingerDistal,
    FingerMiddle,
    IndexProximal,
    MiddleProximal,
    PinkyProximal,
    ThumbBase,
    ThumbDistal,
    ThumbProximal,
)


FLEX_AXIS = (0.0, 1.0, 0.0)
DISTAL_FLEX_AXIS = (0.0, 0.0, -1.0)
SPREAD_AXIS = (0.0, 0.0, 1.0)
THUMB_OPPOSITION_AXIS = (-0.578532546, 0.342020143, -0.740487890)


class FingerTipStage(AssemblyNode):
    """Intermediate and distal printable links about the DIP frame."""

    middle = FingerMiddle()
    distal = FingerDistal()
    dip = RotationalPort(unit="deg")

    def render(self):
        self.distal.rotate(
            106.779596493,
            (0.742941838, 0.473306151, -0.473306151),
        )
        self.distal.translate((3.35456271, 6.5, 20.0))

    def simulate(self):
        self.distal.rotate(self.dip.value, DISTAL_FLEX_AXIS)


class _FingerMcpStage(AssemblyNode):
    """Common MCP stage behavior; subclasses provide exact source poses."""

    pip = RotationalPort(unit="deg")
    dip = RotationalPort(unit="deg")

    def render(self):
        self.proximal.rotate(self.proximal_angle, FLEX_AXIS)
        self.tip.rotate(self.tip_angle, FLEX_AXIS)
        self.tip.translate(self.tip_translation)

    def simulate(self):
        self.tip.rotate(self.pip.value, FLEX_AXIS)
        self.connect(self.dip, self.tip.dip)


class PinkyMcpStage(_FingerMcpStage):
    proximal = PinkyProximal()
    tip = FingerTipStage()
    proximal_angle = -80.0
    tip_angle = -75.0
    tip_translation = (-32.411831761, 0.0, 6.222793739)


class RingMcpStage(_FingerMcpStage):
    proximal = MiddleProximal()
    tip = FingerTipStage()
    proximal_angle = -100.0
    tip_angle = -100.0
    tip_translation = (-45.387980727, 0.0, -7.495412296)


class MiddleMcpStage(_FingerMcpStage):
    proximal = MiddleProximal()
    tip = FingerTipStage()
    proximal_angle = -90.0
    tip_angle = -90.0
    tip_translation = (-46.0, 0.0, 0.5)


class IndexMcpStage(_FingerMcpStage):
    proximal = IndexProximal()
    tip = FingerTipStage()
    proximal_angle = -117.0
    tip_angle = -137.0
    tip_translation = (-34.085243169, 0.0, -16.806135728)


class _Finger(AssemblyNode):
    mcp = RotationalPort(unit="deg")
    pip = RotationalPort(unit="deg")
    dip = RotationalPort(unit="deg")
    spread = RotationalPort(unit="deg")

    def simulate(self):
        self.motion.rotate(self.spread.value, SPREAD_AXIS)
        self.motion.rotate(self.mcp.value, FLEX_AXIS)
        self.connect(self.pip, self.motion.pip)
        self.connect(self.dip, self.motion.dip)


class PinkyFinger(_Finger):
    base = FingerBase()
    motion = PinkyMcpStage()


class RingFinger(_Finger):
    base = FingerBase()
    motion = RingMcpStage()


class MiddleFinger(_Finger):
    base = FingerBase()
    motion = MiddleMcpStage()


class IndexFinger(_Finger):
    base = FingerBase()
    motion = IndexMcpStage()


class ThumbCurlStage(AssemblyNode):
    """Printable thumb links moving inside the opposition stage."""

    proximal = PinkyProximal()
    distal = ThumbDistal()
    pip = RotationalPort(unit="deg")

    def render(self):
        self.proximal.rotate(
            -128.698595339,
            (-0.173389108, 0.417438659, 0.892009632),
        )
        self.distal.rotate(
            -142.584649701,
            (0.060328473, 0.502040564, 0.862737357),
        )
        self.distal.translate((-19.334231174, 15.098029402, 22.079108068))

    def simulate(self):
        self.distal.rotate(self.pip.value, FLEX_AXIS)


class ThumbFinger(AssemblyNode):
    anchor = ThumbProximal()
    base = ThumbBase()
    curl = ThumbCurlStage()
    opposition = RotationalPort(unit="deg")
    mcp = RotationalPort(unit="deg")
    pip = RotationalPort(unit="deg")

    def render(self):
        self.base.rotate(
            -78.476301898,
            (0.857373044, -0.421613876, -0.295217214),
        )
        self.base.translate((-23.640322608, 0.0, 18.46984426))
        self.curl.translate((-23.640322608, 0.0, 18.46984426))

    def simulate(self):
        self.curl.rotate(
            self.opposition.value + self.mcp.value,
            THUMB_OPPOSITION_AXIS,
        )
        self.connect(self.pip, self.curl.pip)


class Digits(AssemblyNode):
    """Five source-placed right-hand digits around the wrist pivot."""

    thumb = ThumbFinger()
    pinky = PinkyFinger()
    ring = RingFinger()
    middle = MiddleFinger()
    index = IndexFinger()

    def render(self):
        self.thumb.rotate(
            -90.109885746,
            (-0.389348058, 0.14961519, 0.908858286),
        )
        self.thumb.translate((-64.309038239, 14.490185157, 28.458350628))

        self.pinky.rotate(
            122.527718822,
            (0.488917559, 0.700719645, -0.519568667),
        )
        self.pinky.translate((9.890350132, -3.421552771, 66.014155066))

        self.ring.rotate(
            126.319741078,
            (0.563308444, 0.643442165, -0.518329795),
        )
        self.ring.translate((-12.843121029, -10.593407483, 78.821434484))

        self.middle.rotate(
            125.93195832,
            (0.608120402, 0.608120402, -0.510273605),
        )
        self.middle.translate((-36.1, -13.986593071, 87.621738225))

        self.index.rotate(
            129.501001644,
            (0.623528122, 0.58074717, -0.523397941),
        )
        self.index.translate((-60.19178493, -11.569695565, 83.131584202))
