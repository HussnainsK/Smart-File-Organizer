from pathlib import Path
from .categories import category_for


def scan_folder(folder: str):
    """Find files directly inside a folder and group them by category.

    HOW IT WORKS:
    1. Convert the supplied folder string into a Path object.
    2. Make sure the path is actually a directory.
    3. Read the files directly inside that directory.
    4. Use category_for() to decide where each file belongs.
    5. Return a dictionary such as {"Images": [file1, file2]}.

    CUSTOMIZE HERE:
    Change category rules in organizer/categories.py rather than changing
    this function. This keeps scanning and file-type rules separate.
    """
    root = Path(folder).expanduser().resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Not a folder: {root}")

    result = {}
    for item in root.iterdir():
        # Only files in the selected folder are scanned; subfolders are not
        # recursively scanned by the current version of SFO.
        if item.is_file():
            result.setdefault(category_for(item), []).append(item)
    return result
