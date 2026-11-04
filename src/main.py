
"""Эмулятор командной оболочки. Вариант 19. Этап 3."""

import argparse
import shlex
import tkinter as tk
from pathlib import Path

from vfs import VirtualFileSystem, VFSError


class ShellEmulator:
    """Графический эмулятор командной оболочки."""

    def __init__(self, root, vfs_path=None, script_path=None):
        self.root = root
        self.vfs = None
        self.running = True

        self.output = tk.Text(
            root,
            height=20,
            width=80,
            state="disabled"
        )
        self.output.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.entry = tk.Entry(root, width=80)
        self.entry.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        self.entry.bind("<Return>", self.on_enter)

        self.write("Эмулятор командной оболочки")
        self.write("Этап 3: виртуальная файловая система")
        self.write("")

        self.print_debug(vfs_path, script_path)

        try:
            self.vfs = VirtualFileSystem(vfs_path)

        except VFSError as error:
            self.write(f"Ошибка загрузки VFS: {error}")
            self.write("Работа эмулятора остановлена.")
            self.entry.config(state="disabled")
            self.root.title("Эмулятор - [ошибка VFS]")
            return

        self.root.title(
            f"Эмулятор - [{self.vfs.name}]"
        )

        self.write(
            f"VFS успешно загружена: {self.vfs.name}"
        )

        stats = self.vfs.statistics()

        self.write(
            f"Файлов: {stats['files']}"
        )
        self.write(
            f"Каталогов: {stats['directories']}"
        )
        self.write(
            f"Максимальная глубина: {stats['max_depth']}"
        )
        self.write("")

        self.entry.focus_set()

        if script_path is not None:
            self.root.after(
                100,
                lambda: self.run_script(script_path)
            )

    def write(self, text):
        """Вывести строку в графическое окно."""

        self.output.config(state="normal")
        self.output.insert("end", str(text) + "\n")
        self.output.see("end")
        self.output.config(state="disabled")

    def print_debug(self, vfs_path, script_path):
        """Показать параметры запуска."""

        self.write("=== Параметры запуска ===")
        self.write(f"VFS path: {vfs_path}")
        self.write(f"Script path: {script_path}")
        self.write("========================")
        self.write("")

    def on_enter(self, event=None):
        """Обработать нажатие Enter."""

        if not self.running:
            return

        command_line = self.entry.get()
        self.entry.delete(0, tk.END)

        self.write(f"$ {command_line}")

        self.execute_command(command_line)

    def execute_command(self, command_line):
        """Разобрать и выполнить команду."""

        try:
            args = shlex.split(command_line)
        except ValueError as error:
            self.write(f"Ошибка разбора команды: {error}")
            return False

        if not args:
            return True

        command = args[0]
        arguments = args[1:]

        if command == "exit":
            if arguments:
                self.write("Ошибка: exit не принимает аргументы")
                return False

            self.write("Завершение работы.")
            self.running = False
            self.entry.config(state="disabled")
            self.root.after(300, self.root.destroy)
            return True

        if command == "ls":
            self.write(
                f"Заглушка ls. Аргументы: {arguments}"
            )
            return True

        if command == "cd":
            self.write(
                f"Заглушка cd. Аргументы: {arguments}"
            )
            return True

        self.write(
            f"Ошибка: неизвестная команда '{command}'"
        )
        return False

    def run_script(self, script_path):
        """Выполнить стартовый сценарий."""

        try:
            lines = Path(script_path).read_text(
                encoding="utf-8-sig"
            ).splitlines()

        except (OSError, UnicodeError) as error:
            self.write(
                f"Ошибка загрузки сценария: {error}"
            )
            return

        self.write("=== Выполнение стартового сценария ===")

        for number, line in enumerate(lines, start=1):
            command = line.strip()

            if not command:
                continue

            self.write(f"$ {command}")

            success = self.execute_command(command)

            if not success:
                self.write(
                    f"Ошибка в строке {number}. "
                    "Выполнение сценария остановлено."
                )
                return

            if not self.running:
                return

        self.write("=== Сценарий завершён ===")


def main():
    """Точка входа в программу."""

    parser = argparse.ArgumentParser(
        description="Эмулятор командной оболочки"
    )

    parser.add_argument(
        "--vfs",
        default=None,
        help="Путь к JSON-файлу VFS"
    )

    parser.add_argument(
        "--script",
        default=None,
        help="Путь к стартовому сценарию"
    )

    args = parser.parse_args()

    root = tk.Tk()

    ShellEmulator(
        root,
        vfs_path=args.vfs,
        script_path=args.script
    )

    root.mainloop()


if __name__ == "__main__":
    main()
