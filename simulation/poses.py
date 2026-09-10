"""Snapshot-only roots with driver defaults fixed to reviewed demo poses."""

from solid_node.node import AssemblyNode
from solid_node.simulation import Driver

from .machine import ArticulatedHand, ForearmTower, WRIST_PIVOT, bind_intent


class FistPose(AssemblyNode):
    tower = ForearmTower()
    hand = ArticulatedHand()

    grasp = Driver(default=100.0, range=(0.0, 100.0), unit="percent")
    index_extension = Driver(default=0.0, range=(0.0, 100.0), unit="percent")
    thumb_opposition = Driver(default=15.0, range=(-10.0, 35.0), unit="deg")
    wrist = Driver(default=0.0, range=(-25.0, 25.0), unit="deg")

    def render(self):
        self.hand.translate(WRIST_PIVOT)

    def simulate(self):
        bind_intent(self)


class PointPose(AssemblyNode):
    tower = ForearmTower()
    hand = ArticulatedHand()

    grasp = Driver(default=100.0, range=(0.0, 100.0), unit="percent")
    index_extension = Driver(default=100.0, range=(0.0, 100.0), unit="percent")
    thumb_opposition = Driver(default=10.0, range=(-10.0, 35.0), unit="deg")
    wrist = Driver(default=0.0, range=(-25.0, 25.0), unit="deg")

    def render(self):
        self.hand.translate(WRIST_PIVOT)

    def simulate(self):
        bind_intent(self)
