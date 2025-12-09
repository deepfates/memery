"""
Simple Tkinter-based desktop shell for Memery.
"""

import os
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import List, Optional

from memery.core import Memery


class NativeMemeryApp:
    def __init__(self) -> None:
        self.memery = Memery()
        self.root = tk.Tk()
        self.root.title("Memery – Desktop Search")
        self.root.geometry("720x520")

        self.folder_var = tk.StringVar(value=os.getcwd())
        self.text_var = tk.StringVar()
        self.image_var = tk.StringVar()
        self.results: List[str] = []
        self.status_var = tk.StringVar(value="Pick a folder and run a search.")
        self.number_var = tk.IntVar(value=10)

        self._build_layout()

    def _build_layout(self) -> None:
        top_frame = tk.Frame(self.root, padx=12, pady=8)
        top_frame.pack(fill=tk.X)

        tk.Label(top_frame, text="Image folder:").grid(row=0, column=0, sticky="w")
        folder_entry = tk.Entry(top_frame, textvariable=self.folder_var, width=60)
        folder_entry.grid(row=0, column=1, sticky="we", padx=(6, 6))
        tk.Button(top_frame, text="Browse", command=self._choose_folder).grid(row=0, column=2)

        tk.Label(top_frame, text="Text query:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        text_entry = tk.Entry(top_frame, textvariable=self.text_var, width=60)
        text_entry.grid(row=1, column=1, sticky="we", padx=(6, 6), pady=(8, 0))

        tk.Label(top_frame, text="Image query (optional):").grid(row=2, column=0, sticky="w", pady=(8, 0))
        image_entry = tk.Entry(top_frame, textvariable=self.image_var, width=60)
        image_entry.grid(row=2, column=1, sticky="we", padx=(6, 6), pady=(8, 0))
        tk.Button(top_frame, text="Pick Image", command=self._choose_image).grid(row=2, column=2, pady=(8, 0))

        tk.Label(top_frame, text="Results to show:").grid(row=3, column=0, sticky="w", pady=(8, 0))
        tk.Spinbox(top_frame, from_=1, to=100, textvariable=self.number_var, width=6).grid(row=3, column=1, sticky="w", pady=(8, 0))

        top_frame.columnconfigure(1, weight=1)

        action_frame = tk.Frame(self.root, padx=12, pady=8)
        action_frame.pack(fill=tk.X)
        tk.Button(action_frame, text="Search", command=self._start_search, width=12).pack(side=tk.LEFT)
        tk.Label(action_frame, textvariable=self.status_var, anchor="w").pack(side=tk.LEFT, padx=(12, 0))

        results_frame = tk.Frame(self.root, padx=12, pady=8)
        results_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(results_frame, text="Results:").pack(anchor="w")
        self.results_box = tk.Listbox(results_frame, selectmode=tk.SINGLE)
        self.results_box.pack(fill=tk.BOTH, expand=True, pady=(6, 0))
        self.results_box.bind("<Double-Button-1>", self._open_selected)

    def _choose_folder(self) -> None:
        folder = filedialog.askdirectory(initialdir=self.folder_var.get())
        if folder:
            self.folder_var.set(folder)

    def _choose_image(self) -> None:
        filepath = filedialog.askopenfilename(
            title="Choose an image query",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")],
        )
        if filepath:
            self.image_var.set(filepath)

    def _start_search(self) -> None:
        folder = self.folder_var.get().strip()
        text_query = self.text_var.get().strip() or None
        image_query = self.image_var.get().strip() or None
        limit = max(1, self.number_var.get())

        if not text_query and not image_query:
            messagebox.showinfo("Memery", "Please provide a text or image query to search.")
            return

        self.status_var.set("Searching… this can take a moment the first time.")
        self.results_box.delete(0, tk.END)

        threading.Thread(
            target=self._run_search,
            args=(folder, text_query, image_query, limit),
            daemon=True,
        ).start()

    def _run_search(self, folder: str, text_query: Optional[str], image_query: Optional[str], limit: int) -> None:
        start_time = time.time()
        try:
            ranked = self.memery.query_flow(folder, query=text_query, image_query=image_query)
            results = ranked[:limit] if ranked else []
            duration = time.time() - start_time
            self.root.after(0, self._present_results, results, duration)
        except Exception as exc:  # noqa: BLE001
            self.root.after(0, self._handle_error, exc)

    def _present_results(self, results: List[str], duration: float) -> None:
        self.results = results
        self.results_box.delete(0, tk.END)
        for item in results:
            self.results_box.insert(tk.END, item)
        if results:
            self.status_var.set(f"Found {len(results)} results in {duration:.1f}s.")
        else:
            self.status_var.set("No results returned.")

    def _handle_error(self, exc: Exception) -> None:
        self.status_var.set("Search failed.")
        messagebox.showerror("Memery", str(exc))

    def _open_selected(self, _event=None) -> None:
        selection = self.results_box.curselection()
        if not selection:
            return
        filepath = self.results_box.get(selection[0])
        self._open_file(filepath)

    @staticmethod
    def _open_file(filepath: str) -> None:
        if sys.platform.startswith("darwin"):
            subprocess.run(["open", filepath], check=False)
        elif os.name == "nt":
            os.startfile(filepath)  # type: ignore[attr-defined]
        else:
            subprocess.run(["xdg-open", filepath], check=False)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = NativeMemeryApp()
    app.run()


if __name__ == "__main__":
    main()
