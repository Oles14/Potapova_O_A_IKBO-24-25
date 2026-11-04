
"""Загрузка и проверка виртуальной файловой системы."""

import copy
import json
from pathlib import Path


class VFSError(Exception):
    """Ошибка виртуальной файловой системы."""
    pass


def validate_node(node, location="/"):
    """Проверить структуру файла или каталога."""

    if not isinstance(node, dict):
        raise VFSError(
            f"Неверный формат узла: {location}"
        )

    node_type = node.get("type")

    if node_type == "dir":
        children = node.get("children")

        if not isinstance(children, dict):
            raise VFSError(
                f"Каталог {location}: children должен быть объектом"
            )

        for name, child in children.items():
            if (
                not isinstance(name, str)
                or not name
                or name in (".", "..")
                or "/" in name
                or "\\" in name
            ):
                raise VFSError(
                    f"Недопустимое имя элемента: {name!r}"
                )

            child_path = (
                location.rstrip("/") + "/" + name
            )

            validate_node(child, child_path)

    elif node_type == "file":
        content = node.get("content")

        if not isinstance(content, str):
            raise VFSError(
                f"Файл {location}: content должен быть строкой"
            )

    else:
        raise VFSError(
            f"Неизвестный тип элемента: {location}"
        )


class VirtualFileSystem:
    """Файловая система, работающая в памяти."""

    def __init__(self, path=None):
        self.source_path = path

        if path is None:
            self.root = {
                "name": "my-vfs",
                "type": "dir",
                "children": {}
            }
        else:
            self.root = self.load(path)

    @staticmethod
    def load(path):
        """Прочитать и проверить JSON-файл."""

        file_path = Path(path)

        try:
            text = file_path.read_text(
                encoding="utf-8-sig"
            )
        except FileNotFoundError as error:
            raise VFSError(
                f"Файл VFS не найден: {path}"
            ) from error
        except (OSError, UnicodeError) as error:
            raise VFSError(
                f"Не удалось прочитать VFS: {error}"
            ) from error

        try:
            data = json.loads(text)
        except json.JSONDecodeError as error:
            raise VFSError(
                f"Неверный JSON: {error}"
            ) from error

        validate_node(data)

        if data["type"] != "dir":
            raise VFSError(
                "Корень VFS должен быть каталогом"
            )

        if not isinstance(data.get("name"), str):
            raise VFSError(
                "Имя VFS должно быть строкой"
            )

        return copy.deepcopy(data)

    @property
    def name(self):
        return self.root["name"]

    def statistics(self):
        """Подсчитать файлы, папки и глубину дерева."""

        files = 0
        directories = 0
        max_depth = 0

        def walk(node, depth):
            nonlocal files, directories, max_depth

            max_depth = max(max_depth, depth)

            if node["type"] == "file":
                files += 1
                return

            directories += 1

            for child in node["children"].values():
                walk(child, depth + 1)

        walk(self.root, 0)

        return {
            "files": files,
            "directories": directories,
            "max_depth": max_depth
        }
