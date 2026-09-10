"""Reviewed positive-volume intersections in the printable ORCA assembly."""

from itertools import combinations

import numpy as np
import trimesh


def mesh_leaves(node, prefix=""):
    """Return qualified names and actual leaf nodes below an assembled root."""

    path = f"{prefix}.{node.name}" if prefix else node.name
    children = list(node.children)
    if not children:
        return [(path, node)]
    leaves = []
    for child in children:
        leaves.extend(mesh_leaves(child, path))
    return leaves


def measured_intersections(node):
    """Measure every positive-volume leaf intersection on source meshes."""

    overlaps = {}
    leaves = mesh_leaves(node)
    for (left_name, left), (right_name, right) in combinations(leaves, 2):
        left_mesh = left.mesh
        right_mesh = right.mesh
        lower = np.maximum(left_mesh.bounds[0], right_mesh.bounds[0])
        upper = np.minimum(left_mesh.bounds[1], right_mesh.bounds[1])
        if np.any(lower > upper):
            continue
        shared = trimesh.boolean.intersection(
            [left_mesh, right_mesh], engine="manifold"
        )
        volume = float(shared.volume) if shared is not None else 0.0
        if volume > 0.0:
            overlaps[(left_name, right_name)] = volume
    return overlaps


# Reviewed default-pose inventory; values are mm^3 on the source meshes.
EXPECTED_REST_OVERLAPS = {
    (
        "OrcaV1.hand.geometry.digits.pinky.motion.tip.middle",
        "OrcaV1.hand.geometry.digits.pinky.motion.tip.distal",
    ): 0.000043930768584,
    (
        "OrcaV1.hand.geometry.digits.ring.motion.tip.middle",
        "OrcaV1.hand.geometry.digits.ring.motion.tip.distal",
    ): 0.000072305370698,
    (
        "OrcaV1.hand.geometry.digits.middle.motion.tip.middle",
        "OrcaV1.hand.geometry.digits.middle.motion.tip.distal",
    ): 0.000015547064512,
    (
        "OrcaV1.hand.geometry.digits.index.motion.tip.middle",
        "OrcaV1.hand.geometry.digits.index.motion.tip.distal",
    ): 0.000042081962083,
}


def assert_rest_overlap_inventory(node):
    """Require the reviewed rest-pose pair set and measured volumes."""

    actual = measured_intersections(node)
    if set(actual) != set(EXPECTED_REST_OVERLAPS):
        raise AssertionError(
            f"overlap pairs changed: {sorted(actual)} != "
            f"{sorted(EXPECTED_REST_OVERLAPS)}"
        )
    for pair, expected in EXPECTED_REST_OVERLAPS.items():
        difference = abs(actual[pair] - expected)
        if difference > 0.000001:
            raise AssertionError(
                f"overlap volume changed for {pair}: {actual[pair]} != {expected}"
            )


def assert_only_reviewed_joint_contacts(node, allowed_pairs=None):
    """Allow only the four measured sub-microlitre distal seat contacts."""

    actual = measured_intersections(node)
    allowed = set(EXPECTED_REST_OVERLAPS) if allowed_pairs is None else set(allowed_pairs)
    unexpected = set(actual) - allowed
    oversized = {pair: volume for pair, volume in actual.items() if volume > 0.001}
    if unexpected or oversized:
        raise AssertionError(
            f"unexpected overlaps={sorted(unexpected)}, oversized={oversized}"
        )
