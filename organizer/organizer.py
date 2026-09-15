from dataclasses import dataclass
from pathlib import Path
import json
import shutil
from datetime import datetime


@dataclass
class MoveRecord:
    """Store one file's original and final paths for undo support."""
    source: str
    destination: str


class FileOrganizer:
    """Plan, execute and undo file moves for one selected root folder."""

    def __init__(self, root: str):
        """Initialize the organizer and the local undo-log paths.

        The .smart_file_organizer folder is created only when an operation is
        actually executed, so preview/scan mode does not create a log.
        """
        self.root = Path(root).expanduser().resolve()
        self.log_dir = self.root / ".smart_file_organizer"
        self.log_file = self.log_dir / "last_operation.json"

    def _unique_destination(self, destination: Path) -> Path:
        """Return a free destination path without overwriting another file.

        If report.pdf already exists, SFO tries report (1).pdf, report (2).pdf,
        and so on until it finds a free name.
        """
        if not destination.exists():
            return destination
        stem, suffix = destination.stem, destination.suffix
        counter = 1
        while True:
            candidate = destination.with_name(f"{stem} ({counter}){suffix}")
            if not candidate.exists():
                return candidate
            counter += 1

    def plan(self, grouped_files):
        """Create a move plan without changing any files.

        HOW IT WORKS:
        - Receives the groups produced by scanner.py.
        - Creates a destination folder for each category.
        - Calculates a unique destination for every source file.
        - Returns pairs of (source, destination) for the GUI preview.
        """
        plan = []
        for category, paths in grouped_files.items():
            target_dir = self.root / category
            for source in paths:
                destination = self._unique_destination(target_dir / source.name)
                plan.append((source, destination))
        return plan

    def execute(self, plan):
        """Move every file in a plan and save an undo record.

        This is the operation that actually changes files on disk. The GUI
        calls it only after Preview mode has been disabled and the user has
        confirmed the operation.
        """
        self.log_dir.mkdir(exist_ok=True)
        records = []

        for source, destination in plan:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
            records.append(MoveRecord(str(source), str(destination)))

        # Save enough information to restore this operation later.
        payload = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "root": str(self.root),
            "moves": [record.__dict__ for record in records],
        }
        self.log_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return records

    def undo_last(self):
        """Restore files from the most recent saved operation.

        The records are processed in reverse order. If the original filename
        is already occupied, _unique_destination() prevents an overwrite.
        After the restore, the one-time undo log is removed.
        """
        if not self.log_file.exists():
            return 0

        data = json.loads(self.log_file.read_text(encoding="utf-8"))
        restored = 0

        for record in reversed(data.get("moves", [])):
            source = Path(record["source"])
            destination = Path(record["destination"])

            if destination.exists():
                source.parent.mkdir(parents=True, exist_ok=True)
                final_source = self._unique_destination(source)
                shutil.move(str(destination), str(final_source))
                restored += 1

        self.log_file.unlink(missing_ok=True)
        return restored
