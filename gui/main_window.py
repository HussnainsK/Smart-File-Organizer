import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from organizer.scanner import scan_folder
from organizer.organizer import FileOrganizer


class FileOrganizerApp(tk.Tk):
    """Modern, Windows-friendly GUI for Smart File Organizer."""

    BG = "#071225"
    PANEL = "#0d1a33"
    PANEL_2 = "#15233d"
    PANEL_3 = "#1b2b49"
    TEXT = "#f8fbff"
    MUTED = "#91a7c4"
    ACCENT = "#19bfff"
    ACCENT_2 = "#3d5cff"
    GREEN = "#19d66b"
    PURPLE = "#b86cff"
    BORDER = "#29405f"
    ROW = "#0a162b"
    ROW_ALT = "#0d1b31"

    def __init__(self):
        super().__init__()
        self.title("Smart File Organizer")
        self.geometry("1160x780")
        self.minsize(980, 680)
        self.configure(bg=self.BG)

        self.folder_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready — choose a folder to begin.")
        self.dry_run_var = tk.BooleanVar(value=True)
        self.plan = []

        self._build_style()
        self._build_ui()

    def _build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background=self.BG)
        style.configure("TLabel", background=self.BG, foreground=self.TEXT, font=("Segoe UI", 10))
        style.configure("Panel.TFrame", background=self.PANEL)
        style.configure("Brand.TLabel", background=self.BG, foreground=self.ACCENT,
                        font=("Segoe UI", 12, "bold"))
        style.configure("Title.TLabel", background=self.BG, foreground=self.TEXT,
                        font=("Segoe UI", 31, "bold"))
        style.configure("Subtitle.TLabel", background=self.BG, foreground=self.MUTED,
                        font=("Segoe UI", 10))
        style.configure("CardTitle.TLabel", background=self.PANEL, foreground=self.TEXT,
                        font=("Segoe UI", 11, "bold"))
        style.configure("Dark.TEntry", fieldbackground=self.PANEL_2, foreground=self.TEXT,
                        insertcolor=self.TEXT, bordercolor=self.BORDER, lightcolor=self.BORDER,
                        darkcolor=self.BORDER, padding=11)
        style.configure("Dark.TButton", font=("Segoe UI", 10, "bold"), padding=(16, 10),
                        background=self.PANEL_2, foreground=self.TEXT, borderwidth=0)
        style.map("Dark.TButton", background=[("active", self.PANEL_3)])
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=(18, 11),
                        background=self.ACCENT, foreground="#03243a", borderwidth=0)
        style.map("Primary.TButton", background=[("active", "#63d8ff")])
        style.configure("Green.TButton", font=("Segoe UI", 10, "bold"), padding=(18, 11),
                        background=self.GREEN, foreground="#032512", borderwidth=0)
        style.map("Green.TButton", background=[("active", "#55e990")])
        style.configure("Dark.TCheckbutton", background=self.PANEL, foreground=self.TEXT,
                        font=("Segoe UI", 10, "bold"))
        style.map("Dark.TCheckbutton", background=[("active", self.PANEL)])
        style.configure("Treeview", background= self.ROW, fieldbackground=self.ROW,
                        foreground=self.TEXT, rowheight=36, borderwidth=0,
                        font=("Segoe UI", 9))
        style.configure("Treeview.Heading", background=self.PANEL_2, foreground="#a9c0de",
                        font=("Segoe UI", 9, "bold"), padding=11, relief="flat")
        style.map("Treeview", background=[("selected", "#075985")], foreground=[("selected", "white")])
        style.configure("Vertical.TScrollbar", background=self.PANEL_2, troughcolor=self.BG,
                        bordercolor=self.BG, arrowcolor=self.MUTED)
        style.configure("Horizontal.TScrollbar", background=self.PANEL_2, troughcolor=self.BG,
                        bordercolor=self.BG, arrowcolor=self.MUTED)

    def _panel(self, parent, padx=1):
        return tk.Frame(parent, bg=self.PANEL, highlightbackground=self.BORDER,
                        highlightthickness=1, bd=0)

    def _build_ui(self):
        outer = tk.Frame(self, bg=self.BG)
        outer.pack(fill="both", expand=True, padx=30, pady=22)

        # Header / branding
        header = tk.Frame(outer, bg=self.BG)
        header.pack(fill="x", pady=(0, 18))

        left_head = tk.Frame(header, bg=self.BG)
        left_head.pack(side="left", fill="x", expand=True)
        tk.Label(left_head, text="▣  SMART FILE ORGANIZER", bg=self.BG, fg=self.ACCENT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w")
        tk.Label(left_head, text="Smart File Organizer", bg=self.BG, fg=self.TEXT,
                 font=("Segoe UI", 31, "bold")).pack(anchor="w", pady=(2, 0))
        tk.Label(left_head, text="Clean your folders in seconds. Preview first, organize safely, undo anytime.",
                 bg=self.BG, fg=self.MUTED, font=("Segoe UI", 10)).pack(anchor="w", pady=(3, 0))

        # Stylish author badge: intentionally visible in the actual GUI.
        author = tk.Frame(header, bg=self.BG)
        author.pack(side="right", anchor="ne", padx=(20, 0), pady=(8, 0))
        tk.Label(author, text="By", bg=self.BG, fg=self.TEXT,
                 font=("Segoe UI", 18, "italic")).pack(side="left", padx=(0, 6))
        tk.Label(author, text="Hussnain sK", bg=self.BG, fg=self.ACCENT,
                 font=("Segoe UI", 20, "bold italic")).pack(side="left")
        tk.Label(author, text="✦", bg=self.BG, fg=self.PURPLE,
                 font=("Segoe UI", 15, "bold")).pack(side="left", padx=(7, 0))
        tk.Frame(author, bg=self.PURPLE, height=2, width=145).pack(side="bottom", fill="x", pady=(3, 0))

        # Folder selection
        folder = self._panel(outer)
        folder.pack(fill="x", pady=(0, 14))
        tk.Label(folder, text="  ▣  FOLDER TO ORGANIZE", bg=self.PANEL, fg=self.TEXT,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=12, pady=(12, 7))
        path_row = tk.Frame(folder, bg=self.PANEL)
        path_row.pack(fill="x", padx=14, pady=(0, 14))
        tk.Label(path_row, text="📁", bg=self.PANEL_2, fg=self.ACCENT,
                 font=("Segoe UI Emoji", 13)).pack(side="left", fill="y", ipadx=8, ipady=3)
        ttk.Entry(path_row, textvariable=self.folder_var, style="Dark.TEntry").pack(
            side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(path_row, text="📂  Browse…", style="Dark.TButton",
                   command=self.choose_folder).pack(side="right")

        # Stats
        stats = tk.Frame(outer, bg=self.BG)
        stats.pack(fill="x", pady=(0, 14))
        self.stat_files = self._make_stat(stats, "▤", "FILES FOUND", "0", self.ACCENT)
        self.stat_status = self._make_stat(stats, "⚙", "MODE", "PREVIEW", self.GREEN)
        self.stat_action = self._make_stat(stats, "◷", "LAST ACTION", "—", self.PURPLE)
        self.stat_safe = self._make_stat(stats, "♢", "SAFE MODE", "PREVIEW FIRST", self.ACCENT)

        # Action bar
        actions = self._panel(outer)
        actions.pack(fill="x", pady=(0, 14))
        left = tk.Frame(actions, bg=self.PANEL)
        left.pack(side="left", padx=14, pady=12)
        ttk.Button(left, text="▶  Scan Folder", style="Primary.TButton", command=self.scan).pack(side="left", padx=(0, 8))
        ttk.Button(left, text="✓  Organize Files", style="Green.TButton", command=self.organize).pack(side="left", padx=8)
        ttk.Button(left, text="↶  Undo Last", style="Dark.TButton", command=self.undo).pack(side="left", padx=8)

        safety = tk.Frame(actions, bg=self.PANEL)
        safety.pack(side="right", padx=16, pady=8)
        tk.Label(safety, text="➜", bg=self.PANEL, fg=self.ACCENT,
                 font=("Segoe UI", 34, "bold")).pack(side="left", padx=(0, 9))
        ttk.Checkbutton(safety, text="Preview only", variable=self.dry_run_var,
                        style="Dark.TCheckbutton", command=self._update_mode).pack(side="left")

        # Results
        results = self._panel(outer)
        results.pack(fill="both", expand=True)
        top = tk.Frame(results, bg=self.PANEL)
        top.pack(fill="x", padx=14, pady=(12, 7))
        tk.Label(top, text="  ▤  PREVIEW / RESULTS", bg=self.PANEL, fg=self.TEXT,
                 font=("Segoe UI", 11, "bold")).pack(side="left")
        tk.Label(top, text="Files will be grouped by type  ⓘ", bg=self.PANEL, fg=self.MUTED,
                 font=("Segoe UI", 9)).pack(side="right")

        table_frame = tk.Frame(results, bg=self.PANEL)
        table_frame.pack(fill="both", expand=True, padx=14, pady=(0, 12))
        columns = ("file", "category", "destination")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("file", text="  FILE")
        self.tree.heading("category", text="  CATEGORY")
        self.tree.heading("destination", text="  DESTINATION")
        self.tree.column("file", width=320, anchor="w")
        self.tree.column("category", width=170, anchor="w")
        self.tree.column("destination", width=560, anchor="w")
        self.tree.tag_configure("even", background=self.ROW)
        self.tree.tag_configure("odd", background=self.ROW_ALT)

        yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        xscroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Empty state shown until a scan happens.
        self.empty_state = tk.Label(table_frame,
                                    text="📁\n\nNo files scanned yet\nClick “Scan Folder” to get started",
                                    bg=self.ROW, fg=self.MUTED,
                                    font=("Segoe UI", 11), justify="center")
        self.empty_state.place(relx=0.5, rely=0.52, anchor="center")

        # Footer with status and author.
        footer = tk.Frame(outer, bg=self.BG)
        footer.pack(fill="x", pady=(9, 0))
        status_left = tk.Frame(footer, bg=self.BG)
        status_left.pack(side="left")
        tk.Label(status_left, text="●", bg=self.BG, fg=self.GREEN,
                 font=("Segoe UI", 11)).pack(side="left", padx=(0, 7))
        tk.Label(status_left, textvariable=self.status_var, bg=self.BG, fg=self.MUTED,
                 font=("Segoe UI", 9)).pack(side="left")

        tk.Label(footer, text="✦  By Hussnain sK", bg=self.BG, fg=self.PURPLE,
                 font=("Segoe UI", 10, "bold italic")).pack(side="right")

    def _make_stat(self, parent, icon, title, value, accent):
        card = tk.Frame(parent, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1)
        card.pack(side="left", fill="x", expand=True, padx=(0, 9))
        tk.Frame(card, bg=accent, width=4).pack(side="left", fill="y")
        icon_box = tk.Frame(card, bg=self.PANEL_2, width=48, height=48)
        icon_box.pack(side="left", padx=(12, 8), pady=10)
        icon_box.pack_propagate(False)
        tk.Label(icon_box, text=icon, bg=self.PANEL_2, fg=accent,
                 font=("Segoe UI", 17, "bold")).pack(expand=True)
        body = tk.Frame(card, bg=self.PANEL)
        body.pack(fill="both", expand=True, padx=(0, 12), pady=9)
        tk.Label(body, text=title, bg=self.PANEL, fg=self.MUTED,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        label = tk.Label(body, text=value, bg=self.PANEL, fg=self.TEXT,
                         font=("Segoe UI", 17, "bold"))
        label.pack(anchor="w", pady=(2, 0))
        return label

    def _update_mode(self):
        mode = "PREVIEW" if self.dry_run_var.get() else "LIVE"
        self.stat_status.config(text=mode)
        self.stat_safe.config(text="PREVIEW FIRST" if mode == "PREVIEW" else "LIVE MODE")
        self.status_var.set(
            f"{mode} mode enabled — " +
            ("nothing will be moved." if mode == "PREVIEW" else "files can now be moved.")
        )

    def choose_folder(self):
        folder = filedialog.askdirectory(title="Choose a folder to organize")
        if folder:
            self.folder_var.set(folder)
            self.clear_table()
            self.stat_files.config(text="0")
            self.stat_action.config(text="—")
            self.status_var.set("Folder selected. Click Scan Folder.")

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.plan = []
        if hasattr(self, "empty_state"):
            self.empty_state.place(relx=0.5, rely=0.52, anchor="center")

    def scan(self):
        folder = self.folder_var.get().strip()
        if not folder:
            messagebox.showwarning("Folder required", "Please choose a folder first.")
            return
        try:
            grouped = scan_folder(folder)
            organizer = FileOrganizer(folder)
            self.plan = organizer.plan(grouped)
        except Exception as exc:
            messagebox.showerror("Scan failed", str(exc))
            return

        for item in self.tree.get_children():
            self.tree.delete(item)
        if self.plan:
            self.empty_state.place_forget()
        else:
            self.empty_state.place(relx=0.5, rely=0.52, anchor="center")

        for index, (source, destination) in enumerate(self.plan):
            category = destination.parent.name
            self.tree.insert("", "end", values=(source.name, category, str(destination)),
                             tags=("even" if index % 2 == 0 else "odd",))
        total = len(self.plan)
        self.stat_files.config(text=str(total))
        self.stat_action.config(text="SCANNED")
        self.status_var.set(f"Found {total} file(s) ready to organize.")

    def organize(self):
        if not self.folder_var.get().strip():
            messagebox.showwarning("Folder required", "Please choose a folder first.")
            return
        if not self.plan:
            self.scan()
            if not self.plan:
                return
        if self.dry_run_var.get():
            messagebox.showinfo(
                "Preview mode",
                f"{len(self.plan)} file(s) are ready.\n\n"
                "Uncheck 'Preview only' and click Organize Files to move them."
            )
            return
        if not messagebox.askyesno("Confirm organization", f"Move {len(self.plan)} file(s) into category folders?"):
            return
        try:
            records = FileOrganizer(self.folder_var.get()).execute(self.plan)
            self.scan()
            self.stat_action.config(text="ORGANIZED")
            self.status_var.set(f"Done. Moved {len(records)} file(s).")
            messagebox.showinfo("Completed", f"Successfully moved {len(records)} file(s).")
        except Exception as exc:
            messagebox.showerror("Organization failed", str(exc))

    def undo(self):
        folder = self.folder_var.get().strip()
        if not folder:
            messagebox.showwarning("Folder required", "Choose the same folder used for the last operation.")
            return
        if not messagebox.askyesno("Undo last operation", "Restore files from the last organization operation?"):
            return
        try:
            restored = FileOrganizer(folder).undo_last()
            self.scan()
            self.stat_action.config(text="UNDONE")
            self.status_var.set(f"Restored {restored} file(s).")
            messagebox.showinfo("Undo complete", f"Restored {restored} file(s).")
        except Exception as exc:
            messagebox.showerror("Undo failed", str(exc))


if __name__ == "__main__":
    FileOrganizerApp().mainloop()
