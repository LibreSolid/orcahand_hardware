"""Exact repository mesh adapters for the printable ORCA v1 mechanism."""

from solid_node.node import StlNode


PRINTED_BLACK = "#25272A"
PRINTED_BLUE = "#1D70B8"
PRINTED_LIGHT = "#E6E8EA"
PRINTED_ORANGE = "#E87722"


class RightCarpals(StlNode):
    """Printable right palm/carpals mesh."""

    stl_source = "../orca_v1/ORCA_Tower/R-Carpals.stl"
    color = PRINTED_BLUE


class RightTopTower(StlNode):
    """Printable right upper forearm tower mesh."""

    stl_source = "../orca_v1/ORCA_Tower/R-TopTower.stl"
    color = PRINTED_BLACK


class BottomTower(StlNode):
    """Printable lower forearm tower mesh.

    The source pack contains one positive-volume printable body followed by
    four zero-volume mesh components.  Body zero is the reviewed part.
    """

    stl_source = "../orca_v1/ORCA_Tower/BottomTower.stl"
    body = 0
    color = PRINTED_BLACK


class FingerBase(StlNode):
    stl_source = "../orca_v1/ORCA_Fingers/R-AP.stl"
    color = PRINTED_BLACK


class IndexProximal(StlNode):
    stl_source = "../orca_v1/ORCA_Fingers/R-I-PP.stl"
    color = PRINTED_LIGHT


class MiddleProximal(StlNode):
    stl_source = "../orca_v1/ORCA_Fingers/R-M-PP.stl"
    color = PRINTED_LIGHT


class PinkyProximal(StlNode):
    stl_source = "../orca_v1/ORCA_Fingers/R-P-PP.stl"
    color = PRINTED_LIGHT


class FingerMiddle(StlNode):
    stl_source = "../orca_v1/ORCA_Fingers/R-IP.stl"
    color = PRINTED_LIGHT


class FingerDistal(StlNode):
    stl_source = "../orca_v1/ORCA_Fingers/DP.stl"
    color = PRINTED_LIGHT


class ThumbBase(StlNode):
    stl_source = "../orca_v1/ORCA_Fingers/R-T-AP.stl"
    color = PRINTED_BLACK


class ThumbProximal(StlNode):
    stl_source = "../orca_v1/ORCA_Fingers/T-TP.stl"
    color = PRINTED_ORANGE


class ThumbDistal(StlNode):
    stl_source = "../orca_v1/ORCA_Fingers/R-T-DP.stl"
    color = PRINTED_LIGHT
