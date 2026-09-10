"""Source-drift contract independent of geometry build cost."""

import unittest

from .source import (
    ASSEMBLY_CLASS_COUNT,
    IDENTITY_PLACEMENT_COUNT,
    OCCURRENCE_COMMENT_COUNT,
    PART_CLASS_COUNT,
    STEP_BYTES,
    STEP_SHA256,
    STEP_SOURCE,
    PRODUCIBLE_MESHES,
    file_sha256,
    generated_layout_counts,
)


class SourceEvidenceTest(unittest.TestCase):

    def test_step_identity(self):
        self.assertEqual(STEP_SOURCE.stat().st_size, STEP_BYTES)
        self.assertEqual(file_sha256(STEP_SOURCE), STEP_SHA256)

    def test_generated_layout_inventory(self):
        self.assertEqual(
            generated_layout_counts(),
            {
                "part_classes": PART_CLASS_COUNT,
                "assembly_classes": ASSEMBLY_CLASS_COUNT,
                "occurrence_comments": OCCURRENCE_COMMENT_COUNT,
                "identity_placements": IDENTITY_PLACEMENT_COUNT,
            },
        )

    def test_selected_mesh_identities(self):
        for evidence in PRODUCIBLE_MESHES.values():
            path = evidence["path"]
            self.assertEqual(path.stat().st_size, evidence["bytes"])
            self.assertEqual(file_sha256(path), evidence["sha256"])
