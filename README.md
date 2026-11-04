# Эмулятор командной оболочки ОС

**Конфигурационное управление | Вариант № 19**

## О проекте

Графический эмулятор UNIX-подобной командной оболочки на Python с использованием Tkinter.

Программа поддерживает работу с виртуальной файловой системой (VFS), загружаемой из JSON. Все изменения выполняются в оперативной памяти без изменения исходных файлов.

## Этапы разработки

| Этап | Ветка | Реализованная функциональность |
|---|---|---|
| 1. REPL | [stage-1-repl](https://github.com/Oles14/Potapova_O_A_IKBO-24-25/tree/stage-1-repl) | GUI, парсер, заглушки команд |
| 2. Конфигурация | [stage-2-config](https://github.com/Oles14/Potapova_O_A_IKBO-24-25/tree/stage-2-config) | Параметры запуска, стартовые сценарии |
| 3. VFS | [stage-3-vfs](https://github.com/Oles14/Potapova_O_A_IKBO-24-25/tree/stage-3-vfs) | Загрузка VFS из JSON |
| 4. Основные команды | [stage-4-commands](https://github.com/Oles14/Potapova_O_A_IKBO-24-25/tree/stage-4-commands) | `ls`, `cd`, `tail`, `uptime` |
| 5. Дополнительные команды | [stage-5-filesystem](https://github.com/Oles14/Potapova_O_A_IKBO-24-25/tree/stage-5-filesystem) | `mkdir`, `rm` |

## Поддерживаемые команды

`ls`, `cd`, `tail`, `uptime`, `mkdir`, `rm`, `exit`.

Поддерживаются абсолютные и относительные пути, аргументы в кавычках и обработка ошибок.

## Структура проекта

```text
src/       — исходный код эмулятора
scripts/   — JSON-файлы VFS и стартовые сценарии
tests/     — автоматические тесты
README.md  — документация
```

## Запуск

Требуется Python 3 с поддержкой Tkinter.

**Интерактивный режим:**

```powershell
py src/main.py --vfs scripts/vfs_stage5.json
```

**Успешный стартовый сценарий:**

```powershell
.\scripts\run_stage5_ok.bat
```

**Сценарий с ошибкой:**

```powershell
.\scripts\run_stage5_error.bat
```

## Тестирование

```powershell
py -m unittest discover -s tests -v
```

## Результат

Реализованы пять этапов учебного эмулятора командной оболочки по варианту № 19. История разработки сохранена в отдельных ветках Git.

