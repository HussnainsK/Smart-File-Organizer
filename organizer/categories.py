from pathlib import Path

CATEGORIES = {
    "Images": {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".tif",
        ".ico", ".svg", ".heic", ".avif"
    },
    "Videos": {
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".3gp"
    },
    "Music": {
        ".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma", ".opus"
    },
    "Documents": {
        ".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx",
        ".csv", ".ppt", ".pptx", ".odp", ".ods"
    },
    "Archives": {
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"
    },
    "Programs": {
        ".exe", ".msi", ".msix", ".bat", ".cmd", ".com"
    },
    "Code": {
        ".py", ".js", ".ts", ".html", ".css", ".json", ".xml", ".java",
        ".c", ".cpp", ".h", ".hpp", ".cs", ".php", ".sql", ".sh", ".ps1"
    },
}

def category_for(path: Path) -> str:
    return next((name for name, exts in CATEGORIES.items() if path.suffix.lower() in exts), "Others")
