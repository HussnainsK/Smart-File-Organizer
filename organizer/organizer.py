from dataclasses import dataclass
from pathlib import Path
import json
import shutil
from datetime import datetime

@dataclass
class MoveRecord:
    source: str
    destination: str

class FileOrganizer:
    def __init__(self, root: str):
        self.root = Path(root).expanduser().resolve()
        self.log_dir = self.root / ".smart_file_organizer"
        self.log_file = self.log_dir / "last_operation.json"

    def _unique_destination(self, destination: Path) -> Path:
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
        plan = []
        for category, paths in grouped_files.items():
            target_dir = self.root / category
            for source in paths:
                destination = self._unique_destination(target_dir / source.name)
                plan.append((source, destination))
        return plan

    def execute(self, plan):
        self.log_dir.mkdir(exist_ok=True)
        records = []

        for source, destination in plan:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
            records.append(MoveRecord(str(source), str(destination)))

        payload = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "root": str(self.root),
            "moves": [record.__dict__ for record in records],
        }
        self.log_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return records

    def undo_last(self):
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
