import tempfile
import unittest
from pathlib import Path

from organizer.scanner import scan_folder
from organizer.organizer import FileOrganizer

class OrganizerTests(unittest.TestCase):
    def test_scan_categories(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "photo.jpg").touch()
            (root / "song.mp3").touch()
            (root / "unknown.xyz").touch()

            result = scan_folder(tmp)

            self.assertEqual(len(result["Images"]), 1)
            self.assertEqual(len(result["Music"]), 1)
            self.assertEqual(len(result["Others"]), 1)

    def test_execute_and_undo(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "test.txt"
            source.write_text("hello", encoding="utf-8")

            organizer = FileOrganizer(tmp)
            plan = organizer.plan(scan_folder(tmp))
            records = organizer.execute(plan)

            self.assertEqual(len(records), 1)
            self.assertFalse(source.exists())
            self.assertTrue((root / "Documents" / "test.txt").exists())

            restored = organizer.undo_last()
            self.assertEqual(restored, 1)
            self.assertTrue(source.exists())

if __name__ == "__main__":
    unittest.main()
