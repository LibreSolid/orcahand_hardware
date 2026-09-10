"""Reviewed identity of the upstream assembly used by the simulation."""

from hashlib import sha256
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STEP_SOURCE = PROJECT_ROOT / "orca_v1" / "ORCA_Assembly" / "ORCA_v1.step"
GENERATED_ASSEMBLY = Path(__file__).with_name("v1") / "assembly.py"
GENERATED_PARTS = Path(__file__).with_name("v1") / "parts.py"

PRODUCIBLE_MESHES = {
    "bottom_tower": {
        "path": PROJECT_ROOT / "orca_v1" / "ORCA_Tower" / "BottomTower.stl",
        "bytes": 3_523_584,
        "sha256": "dd01bc5593a203d2293599aef029be18dfbc303e02f5f8cda175c6f1d22187d1",
    },
    "top_tower": {
        "path": PROJECT_ROOT / "orca_v1" / "ORCA_Tower" / "R-TopTower.stl",
        "bytes": 5_533_584,
        "sha256": "008c09533eef42c32516aeb9880e15a86ed579d059b02a98a19e07f433e5ef9d",
    },
    "carpals": {
        "path": PROJECT_ROOT / "orca_v1" / "ORCA_Tower" / "R-Carpals.stl",
        "bytes": 8_616_484,
        "sha256": "9f98bcef8d593b0c27cf92f2684426d080ac23bea8cc2c776a70884a13f76a39",
    },
    "finger_base": {
        "path": PROJECT_ROOT / "orca_v1" / "ORCA_Fingers" / "R-AP.stl",
        "bytes": 808_684,
        "sha256": "244179d03c627bad34e1d30ea583a7fb38da3167f11f9a2ef04f92056f6f803c",
    },
    "index_proximal": {
        "path": PROJECT_ROOT / "orca_v1" / "ORCA_Fingers" / "R-I-PP.stl",
        "bytes": 493_184,
        "sha256": "20365942545cce669d7035e2a6f0f75ab4e83f4fdfadae2cfc09e02d2193d1b6",
    },
    "middle_proximal": {
        "path": PROJECT_ROOT / "orca_v1" / "ORCA_Fingers" / "R-M-PP.stl",
        "bytes": 468_784,
        "sha256": "e6434bba8f2b29d2ec6fef31b5a1e6c02e9c44cbf79a7672b9231e48556fcff6",
    },
    "pinky_proximal": {
        "path": PROJECT_ROOT / "orca_v1" / "ORCA_Fingers" / "R-P-PP.stl",
        "bytes": 537_984,
        "sha256": "a3cbe405e3f9d8ae1462b8e67093ae27ad18ea9168dbc2b6c13767a06e8165a0",
    },
    "finger_middle": {
        "path": PROJECT_ROOT / "orca_v1" / "ORCA_Fingers" / "R-IP.stl",
        "bytes": 430_384,
        "sha256": "82cfda06d773cf30edfc56a62a8ef689f336e26399145e98580977c0a52a904f",
    },
    "finger_distal": {
        "path": PROJECT_ROOT / "orca_v1" / "ORCA_Fingers" / "DP.stl",
        "bytes": 214_784,
        "sha256": "0066fe4f9487669224f27199fa0dc058e99b8d955c5f28a8b982f046d698f387",
    },
    "thumb_base": {
        "path": PROJECT_ROOT / "orca_v1" / "ORCA_Fingers" / "R-T-AP.stl",
        "bytes": 1_121_284,
        "sha256": "752c0ff240787fb765ba7977babf50365a0d98c7e40aeebd7e612389707aa1af",
    },
    "thumb_proximal": {
        "path": PROJECT_ROOT / "orca_v1" / "ORCA_Fingers" / "T-TP.stl",
        "bytes": 492_584,
        "sha256": "790e78e364c08e78f2e6f9754e04fa6c186b412641b52e301bb7e8ced86541db",
    },
    "thumb_distal": {
        "path": PROJECT_ROOT / "orca_v1" / "ORCA_Fingers" / "R-T-DP.stl",
        "bytes": 578_384,
        "sha256": "fd54d2c03c0b97dde95682147fc92db25f80103e8845a2562409847596536d7c",
    },
}

STEP_SHA256 = "d34b5e7b51ff1b01765a02505de76bf3fd2babebd12bd7dd8e13d8014d49cf41"
STEP_BYTES = 41_262_983
PART_CLASS_COUNT = 152
ASSEMBLY_CLASS_COUNT = 53
OCCURRENCE_COMMENT_COUNT = 809
IDENTITY_PLACEMENT_COUNT = 341


def file_sha256(path):
    """Return a file digest without relying on mutable build artifacts."""

    digest = sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def generated_layout_counts():
    """Return stable structural counts from the generated STEP transcription."""

    assembly = GENERATED_ASSEMBLY.read_text(encoding="utf-8")
    parts = GENERATED_PARTS.read_text(encoding="utf-8")
    return {
        "part_classes": parts.count("\nclass "),
        "assembly_classes": assembly.count("\nclass "),
        "occurrence_comments": assembly.count("(ORCA_v1.step)"),
        "identity_placements": assembly.count("is placed at the identity"),
    }


def assert_actual_meshes(node, expected_sources):
    """Reject rendered leaves that are not their reviewed repository meshes."""

    from solid_node.node import StlNode

    leaves = {}

    def visit(current):
        children = list(current.children)
        if children:
            for child in children:
                visit(child)
        else:
            leaves[current.name] = current

    visit(node)
    if set(leaves) != set(expected_sources):
        raise AssertionError(
            f"rendered leaves {sorted(leaves)} != reviewed meshes "
            f"{sorted(expected_sources)}"
        )
    for name, expected in expected_sources.items():
        leaf = leaves[name]
        if not isinstance(leaf, StlNode):
            raise AssertionError(f"{name} is proxy geometry, not a StlNode")
        actual = str(type(leaf).stl_source)
        if actual != expected:
            raise AssertionError(f"{name} loads {actual!r}, expected {expected!r}")


def actual_mesh_inventory(node):
    """Count source meshes and reject any rendered non-STL proxy leaf."""

    from collections import Counter
    from solid_node.node import StlNode

    inventory = Counter()

    def visit(current):
        children = list(current.children)
        if children:
            for child in children:
                visit(child)
            return
        if not isinstance(current, StlNode):
            raise AssertionError(
                f"{current.name} is rendered proxy geometry ({type(current).__name__})"
            )
        inventory[str(type(current).stl_source)] += 1

    visit(node)
    return inventory
