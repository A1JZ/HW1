
# Эмулятор языка оболочки ОС (VShell)

## Описание
VShell — это программа, которая эмулирует поведение UNIX-подобной командной строки. Она позволяет работать с виртуальной файловой системой в формате ZIP и выполнять базовые команды оболочки. Программа поддерживает графический интерфейс для удобного взаимодействия с файловой системой.

## Функциональность
1. **Команды работы с директориями и файлами**:
   - `ls` — отображает содержимое текущей или указанной директории.
   - `cd` — позволяет переходить между директориями (включая возврат на уровень выше через `..`).
   - `mv` — симулирует перемещение файлов или директорий.

2. **Информация о системе**:
   - `whoami` — выводит имя текущего пользователя.

3. **Завершение работы**:
   - `exit` — завершает работу программы.

4. **Особенности**:
   - Интерфейс поддерживает выполнение команд через GUI.
   - Поддержка конфигурации через JSON-файл.
   - Возможность выполнения команд при старте через `script.txt`.

## Запуск программы
1. Убедитесь, что у вас установлен Python версии 3.6 или выше.
2. Подготовьте необходимые файлы:
   - `system.zip` — виртуальная файловая система.
   - `config.json` — файл конфигурации. Пример:
     ```json
     {
         "user_name": "testuser",
         "computer_name": "testpc",
         "file_system_path": "system.zip",
         "startup_script_path": "script.txt"
     }
     ```
   - `script.txt` — список команд, которые будут выполнены при старте программы (опционально).

3. Запустите программу командой:
   ```bash
   python main.py --filesystem system.zip --config config.json
   ```

## Пример использования программы
- **Вывод содержимого текущей директории**:
  ```bash
  ls
  ```
- **Переход в поддиректорию**:
  ```bash
  cd root/dir1
  ```
- **Перемещение файла**:
  ```bash
  mv root/dir1/file1.txt root/dir2/file1.txt
  ```
- **Вывод имени пользователя**:
  ```bash
  whoami
  ```
- **Выход из программы**:
  ```bash
  exit
  ```

## Требования
- Python 3.6+
- Модули:
  - `zipfile`
  - `argparse`
  - `json`
  - `tkinter`

## Проверка работоспособности и прохождения тестов
### Скриншот работы программы
![Работа программы](программа.png)

### Скриншот прохождения тестов
![Прохождение тестов](tests.png)
