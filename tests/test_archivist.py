import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import archivist  # noqa: E402

STORY = json.loads((ROOT / "bible" / "story.json").read_text(encoding="utf-8"))
CLEAN = (ROOT / "story" / "part1-the-boy-without-a-book.md").read_text(encoding="utf-8")


class ArchivistTests(unittest.TestCase):
    def test_color_near_eyes(self):
        self.assertEqual(archivist.find_color_near("Hina's green eyes narrowed.", "eyes"), "green")

    def test_contradiction_flagged(self):
        findings = archivist.check_story(STORY, "Hina's green eyes narrowed.")
        self.assertTrue(any(f["type"] == "continuity" for f in findings))

    def test_slop_flagged(self):
        findings = archivist.check_story(STORY, "The rain was a testament to the storm.")
        self.assertTrue(any("testament" in f["message"] for f in findings))

    def test_clean_chapter_has_no_hard_findings(self):
        findings = archivist.check_story(STORY, CLEAN)
        hard = [f for f in findings if f["type"] in {"continuity", "rating", "north_star"}]
        self.assertEqual(hard, [])

    def test_context_pack(self):
        pack = archivist.context_pack(STORY)
        self.assertIn("North Star", pack)
        self.assertIn("Open threads", pack)

    def test_threads_report(self):
        report = archivist.threads_report(STORY)
        self.assertIn("T1", report)
        self.assertIn("Open", report)


if __name__ == "__main__":
    unittest.main()
