from pathlib import Path
from .categories import category_for

def scan_folder(folder: str):
    """Return files directly inside folder, grouped by category."""
    root = Path(folder).expanduser().resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Not a folder: {root}")

    result = {}
    for item in root.iterdir():
        if item.is_file():
            result.setdefault(category_for(item), []).append(item)
    return result
