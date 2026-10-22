<<<<<<< HEAD
# Эмулятор командной оболочки ОС

Вариант 19. GUI-эмулятор UNIX-подобной командной строки.

## Возможности
- GUI-интерфейс (tkinter), имя VFS в заголовке окна
- Парсер с поддержкой аргументов в кавычках
- VFS из JSON-файла (base64 для бинарных данных)
- Команды: ls, cd, tail, uptime, rm, mkdir, exit

## Запуск
python src/main.py --vfs my-vfs.json

## Тесты
python -m unittest discover tests


## Параметры командной строки
- `--vfs` — путь к JSON-файлу VFS
- `--script` — путь к стартовому скрипту
=======
# Potapova_O_A_IKBO-24-25
>>>>>>> f87908becd3bc910cf550e7bb997612549073d65
