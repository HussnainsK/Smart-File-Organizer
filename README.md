# 📁 Smart File Organizer

A clean, safe, Windows-friendly Python GUI that automatically organizes files into folders such as **Images, Videos, Music, Documents, Archives, Programs, Code, and Others**.

## ✨ Features

- 🖥️ Simple Tkinter desktop GUI
- 🔍 Scan a folder before making changes
- 👀 Preview mode enabled by default
- 📂 Automatic file categorization by extension
- 🔁 Safe duplicate-name handling (`file (1).txt`, etc.)
- ↩️ Undo the last organization operation
- 📝 Saves a local operation log for undo
- 🛡️ Does not require administrator access for normal folders
- 📦 No third-party Python packages required
- 🧪 Includes unit tests

## 🗂️ Categories

| Category | Examples |
|---|---|
| Images | JPG, PNG, GIF, WEBP, SVG |
| Videos | MP4, MKV, AVI, MOV, WEBM |
| Music | MP3, WAV, FLAC, AAC |
| Documents | PDF, DOCX, XLSX, PPTX, TXT |
| Archives | ZIP, RAR, 7Z, TAR, GZ |
| Programs | EXE, MSI, BAT, CMD |
| Code | PY, JS, HTML, CSS, JSON, C++, Java |
| Others | Unknown extensions |

## 🚀 Requirements

- Windows, macOS, or Linux
- Python 3.10+
- Tkinter (normally included with standard Python installers)

## ▶️ Run

```bash
git clone https://github.com/YOUR-USERNAME/Smart-File-Organizer.git
cd Smart-File-Organizer
py app.py
```

On systems where `py` is unavailable:

```bash
python app.py
```

## 🧪 Run tests

```bash
py -m unittest discover -s tests -v
```

## 🛡️ Recommended workflow

1. Open the app.
2. Select a test folder.
3. Keep **Preview only** enabled.
4. Click **Scan Folder**.
5. Review the proposed destinations.
6. Uncheck **Preview only**.
7. Click **Organize Files**.
8. Use **Undo Last** if you need to restore the previous operation.

> ⚠️ Always test the application on a copy of important files first. The app moves files; it does not create backups.

## 🏗️ Project structure

```text
Smart-File-Organizer/
├── app.py
├── organizer/
│   ├── __init__.py
│   ├── categories.py
│   ├── scanner.py
│   └── organizer.py
├── gui/
│   ├── __init__.py
│   └── main_window.py
├── tests/
│   └── test_organizer.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## 🔮 Roadmap

- [ ] Custom category editor
- [ ] Sort by year/month
- [ ] File search
- [ ] Dark mode
- [ ] Drag-and-drop support
- [ ] Export operation history
- [ ] Windows `.exe` release
- [ ] Folder watching / automatic organization

## 📜 License

MIT License.
