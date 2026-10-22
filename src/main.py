"""Эмулятор командной оболочки. Этап 2: конфигурация."""
import shlex
import tkinter as tk
import argparse

VFS_NAME = "my-vfs"


class ShellEmulator:
    """Графический эмулятор командной оболочки ОС."""

    def __init__(self, root):
        """Создать окно, поле вывода и поле ввода."""
        self.root = root
        self.root.title(f"Эмулятор - [{VFS_NAME}]")

        self.output = tk.Text(root, height=20, width=80)
        self.output.pack()

        self.entry = tk.Entry(root, width=80)
        self.entry.pack()
        self.entry.bind("<Return>", self.on_enter)

    def write(self, text):
        """Вывести текст в область вывода."""
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def print_debug(self, vfs_path, script_path):
        """Вывести отладочную информацию о параметрах запуска."""
        self.write("=== Параметры запуска (debug) ===")
        self.write(f"VFS path:    {vfs_path}")
        self.write(f"Script path: {script_path}")
        self.write("=================================")

    def on_enter(self, event):
        """Обработать нажатие Enter в поле ввода."""
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self.write(f"{VFS_NAME}$ {line}")
        self.execute(line)

    def execute(self, line):
        """Разобрать и выполнить строку. Вернуть False при ошибке."""
        try:
            parts = shlex.split(line)
        except ValueError as error:
            self.write(f"Ошибка разбора: {error}")
            return False

        if not parts:
            return True

        command = parts[0]
        args = parts[1:]

        if command == "exit":
            self.root.quit()
            return True
        if command == "ls":
            self.write(f"ls {args}")
            return True
        if command == "cd":
            self.write(f"cd {args}")
            return True

        self.write(f"Ошибка: неизвестная команда '{command}'")
        return False

    def run_script(self, script_path):
        """Выполнить команды из скрипта, остановиться при ошибке."""
        try:
            with open(script_path, encoding="utf-8") as file:
                lines = file.readlines()
        except OSError as error:
            self.write(f"Ошибка открытия скрипта: {error}")
            return

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue
            self.write(f"{VFS_NAME}$ {line}")
            if self.execute(line) is False:
                self.write("Скрипт остановлен из-за ошибки.")
                break


def parse_args():
    """Разобрать аргументы командной строки."""
    parser = argparse.ArgumentParser(description="Эмулятор оболочки ОС")
    parser.add_argument("--vfs", help="Путь к физическому расположению VFS")
    parser.add_argument("--script", help="Путь к стартовому скрипту")
    return parser.parse_args()


def main():
    """Точка входа в приложение."""
    arguments = parse_args()
    window = tk.Tk()
    emulator = ShellEmulator(window)
    emulator.print_debug(arguments.vfs, arguments.script)
    if arguments.script:
        window.after(100, lambda: emulator.run_script(arguments.script))
    window.mainloop()


if __name__ == "__main__":
    main()