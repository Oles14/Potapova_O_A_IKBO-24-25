
"""Основные команды эмулятора. Этап 4."""

import time


class CommandError(Exception):
    """Ошибка выполнения команды."""
    pass


class ShellCommands:
    """Работа с командами и виртуальными путями."""

    def __init__(self, vfs):
        self.vfs = vfs

        # Текущий путь: пустой список означает корень /
        self.cwd = []

        # Время запуска эмулятора
        self.start_time = time.monotonic()

    def current_path(self):
        """Получить текущий путь в виде строки."""

        if not self.cwd:
            return "/"

        return "/" + "/".join(self.cwd)

    def normalize_path(self, path):
        """Превратить путь в список его частей."""

        if path.startswith("/"):
            parts = []
        else:
            parts = self.cwd.copy()

        for part in path.split("/"):
            if part in ("", "."):
                continue

            if part == "..":
                if parts:
                    parts.pop()
            else:
                parts.append(part)

        return parts

    def get_node(self, parts):
        """Найти элемент VFS по частям пути."""

        node = self.vfs.root

        for part in parts:
            if node["type"] != "dir":
                raise CommandError(
                    f"Не является каталогом: {part}"
                )

            children = node["children"]

            if part not in children:
                raise CommandError(
                    f"Путь не найден: /{'/'.join(parts)}"
                )

            node = children[part]

        return node

    def resolve(self, path):
        """Получить узел VFS по относительному или абсолютному пути."""

        parts = self.normalize_path(path)
        node = self.get_node(parts)

        return node, parts

    def ls(self, arguments):
        """Показать содержимое каталога."""

        show_hidden = False
        paths = []

        for arg in arguments:
            if arg == "-a":
                show_hidden = True
            elif arg.startswith("-") and arg != "-":
                raise CommandError(
                    f"ls: неизвестный параметр {arg}"
                )
            else:
                paths.append(arg)

        if len(paths) > 1:
            raise CommandError(
                "ls: укажите не более одного пути"
            )

        path = paths[0] if paths else "."

        node, _ = self.resolve(path)

        if node["type"] == "file":
            return path.split("/")[-1]

        names = []

        for name, child in sorted(
            node["children"].items()
        ):
            if name.startswith(".") and not show_hidden:
                continue

            if child["type"] == "dir":
                names.append(name + "/")
            else:
                names.append(name)

        if not names:
            return "(пустой каталог)"

        return "  ".join(names)

    def cd(self, arguments):
        """Изменить текущий каталог."""

        if len(arguments) > 1:
            raise CommandError(
                "cd: слишком много аргументов"
            )

        path = arguments[0] if arguments else "/"

        node, parts = self.resolve(path)

        if node["type"] != "dir":
            raise CommandError(
                f"cd: это не каталог: {path}"
            )

        self.cwd = parts

        return f"Текущий каталог: {self.current_path()}"

    def tail(self, arguments):
        """Показать последние строки текстового файла."""

        count = 10
        path = None
        index = 0

        while index < len(arguments):
            arg = arguments[index]

            if arg == "-n":
                if index + 1 >= len(arguments):
                    raise CommandError(
                        "tail: после -n требуется число"
                    )

                try:
                    count = int(arguments[index + 1])
                except ValueError:
                    raise CommandError(
                        "tail: количество строк должно быть числом"
                    )

                if count < 0:
                    raise CommandError(
                        "tail: количество строк не может быть отрицательным"
                    )

                index += 2
                continue

            if arg.startswith("-"):
                raise CommandError(
                    f"tail: неизвестный параметр {arg}"
                )

            if path is not None:
                raise CommandError(
                    "tail: укажите только один файл"
                )

            path = arg
            index += 1

        if path is None:
            raise CommandError(
                "tail: не указан файл"
            )

        node, _ = self.resolve(path)

        if node["type"] != "file":
            raise CommandError(
                f"tail: это не файл: {path}"
            )

        lines = node["content"].splitlines()

        if count == 0:
            return ""

        return "\n".join(lines[-count:])

    def uptime(self, arguments):
        """Показать время работы эмулятора."""

        if arguments:
            raise CommandError(
                "uptime: команда не принимает аргументы"
            )

        seconds = int(
            time.monotonic() - self.start_time
        )

        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return (
            "Время работы эмулятора: "
            f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        )

    def execute(self, command, arguments):
        """Выполнить одну из основных команд."""

        if command == "ls":
            return self.ls(arguments)

        if command == "cd":
            return self.cd(arguments)

        if command == "tail":
            return self.tail(arguments)

        if command == "uptime":
            return self.uptime(arguments)

        raise CommandError(
            f"Неизвестная команда: {command}"
        )
