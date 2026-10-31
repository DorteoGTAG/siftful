from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from .interpreter import SiftfulInterpreter


class SiftfulStudio(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("SIFTFUL Studio Prototype")
        self.geometry("1100x700")
        self.configure(bg="#111111")

        self.current_file: Path | None = None
        self.interpreter = SiftfulInterpreter()

        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open .sft", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        self.toolbar = tk.Frame(self, bg="#1b1b1b")
        self.toolbar.pack(fill=tk.X, padx=6, pady=(6, 0))

        self.run_button = ttk.Button(self.toolbar, text="Run", command=self.run_code)
        self.run_button.pack(side=tk.LEFT, padx=(0, 8))

        self.stop_button = ttk.Button(self.toolbar, text="Stop", command=self.stop_run)
        self.stop_button.pack(side=tk.LEFT)

        self.main_split = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_split.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        editor_container = tk.Frame(self.main_split, bg="#1f1f1f")
        editor_container.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(editor_container, text="SIFTFUL Editor", fg="#d9d9d9", bg="#1f1f1f", anchor="w")
        title_label.pack(fill=tk.X, padx=8, pady=(8, 0))

        self.editor = tk.Text(editor_container, bg="#111111", fg="#dcdcdc", insertbackground="white", wrap=tk.NONE, font=("Consolas", 11))
        self.editor.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self._apply_syntax_coloring()

        output_container = tk.Frame(self.main_split, bg="#1f1f1f")
        output_container.pack(fill=tk.BOTH, expand=True)

        output_label = tk.Label(output_container, text="Console", fg="#d9d9d9", bg="#1f1f1f", anchor="w")
        output_label.pack(fill=tk.X, padx=8, pady=(8, 0))

        self.output = tk.Text(output_container, bg="#0d0d0d", fg="#f2f2f2", wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 10))
        self.output.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.main_split.add(editor_container)
        self.main_split.add(output_container)

        self.editor.insert(tk.END, 'new.varible("score")\nscore = 100\nscore += 10\nprint.inst("Score is:")\nprint.inst(score)\n\nif.inst(score > 50) {\n    print.inst("You win!")\n} else.inst() {\n    print.inst("Try again")\n}\n')

    def _apply_syntax_coloring(self) -> None:
        self.editor.tag_configure("keyword", foreground="#8ab4f8")
        self.editor.tag_configure("string", foreground="#f7c779")
        self.editor.tag_configure("number", foreground="#c58af9")
        self.editor.tag_configure("comment", foreground="#5f8f5f")

    def new_file(self) -> None:
        self.editor.delete("1.0", tk.END)
        self.current_file = None

    def open_file(self) -> None:
        path = filedialog.askopenfilename(defaultextension=".sft", filetypes=[("SIFTFUL files", "*.sft"), ("All files", "*.*")])
        if not path:
            return
        file = Path(path)
        self.current_file = file
        self.editor.delete("1.0", tk.END)
        self.editor.insert(tk.END, file.read_text(encoding="utf-8"))

    def save_file(self) -> None:
        if self.current_file is None:
            self.save_file_as()
            return
        self.current_file.write_text(self.editor.get("1.0", tk.END), encoding="utf-8")

    def save_file_as(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".sft", filetypes=[("SIFTFUL files", "*.sft")])
        if not path:
            return
        file = Path(path)
        self.current_file = file
        self.save_file()

    def stop_run(self) -> None:
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, "\n[Stop requested]\n")
        self.output.configure(state=tk.DISABLED)

    def run_code(self) -> None:
        code = self.editor.get("1.0", tk.END)
        self.output.configure(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)

        try:
            results = self.interpreter.run(code)
            for line in results:
                self.output.insert(tk.END, f"{line}\n")
        except Exception as exc:
            self.output.insert(tk.END, f"ERROR: {exc}\n")
        finally:
            self.output.configure(state=tk.DISABLED)


def main() -> None:
    app = SiftfulStudio()
    app.mainloop()


if __name__ == "__main__":
    main()
