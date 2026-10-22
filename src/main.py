"""Эмулятор командной оболочки. Этап 1: REPL с GUI."""
import shlex
import tkinter as tk


VFS_NAME = "my-vfs"


class ShellEmulator:
    """Графический эмулятор командной оболочки ОС."""

    def __init__(self, root):
        self.root = root
        self.root.title(f"Эмулятор - [{VFS_NAME}]")

        self.output = tk.Text(root, height=20, width=80)
        self.output.pack()

        self.entry = tk.Entry(root, width=80)
        self.entry.pack()
        self.entry.bind("<Return>", self.on_enter)

    def write(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def on_enter(self, event):
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self.write(f"{VFS_NAME}$ {line}")
        self.execute(line)

    def execute(self, line):
        try:
            parts = shlex.split(line)
        except ValueError as err:
            self.write(f"ошибка парсинга: {err}")
            return
        if not parts:
            return
        self.run_command(parts[0], parts[1:])

    def run_command(self, command, args):
        if command == "exit":
            self.root.destroy()
        elif command == "ls":
            self.write(f"ls {args}")
        elif command == "cd":
            self.write(f"cd {args}")
        else:
            self.write(f"ошибка: неизвестная команда '{command}'")


def main():
    root = tk.Tk()
    ShellEmulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()