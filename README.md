```markdown
# Эмулятор языка оболочки ОС (VShell)

## Описание
VShell — это эмулятор оболочки операционной системы, который имитирует поведение UNIX-подобной командной строки. Программа позволяет пользователю работать с виртуальной файловой системой, представленной в формате ZIP, и выполнять стандартные команды оболочки.

Эмулятор работает в режиме **GUI (графического интерфейса пользователя)** и предоставляет удобное текстовое окно для взаимодействия с файловой системой.

---

## Функциональность

### Поддерживаемые команды:
1. **`ls`** — выводит содержимое текущей или указанной директории.
2. **`cd`** — позволяет переходить между директориями.
3. **`mv`** — перемещает файлы и директории в указанное место.
4. **`whoami`** — отображает имя текущего пользователя (заданное в конфигурационном файле).
5. **`exit`** — завершает работу эмулятора.

### Дополнительные возможности:
- Поддержка виртуальной файловой системы в формате ZIP (не требуется предварительная распаковка).
- Автоматическое выполнение команд из стартового скрипта `script.txt`.
- Настраиваемые параметры через конфигурационный файл `config.json`.

---

## Запуск программы

### 1. Установите Python
Убедитесь, что на вашем компьютере установлен Python версии 3.6 или выше.

### 2. Склонируйте репозиторий
Склонируйте репозиторий программы с GitHub:

```bash
git clone https://github.com/<ваш-репозиторий>/Homework1.git
cd Homework1
```

### 3. Подготовьте файлы
Создайте или проверьте наличие следующих файлов:
- **`system.zip`** — архив с виртуальной файловой системой.
- **`config.json`** — файл конфигурации программы.
- **`script.txt`** — файл со стартовыми командами (опционально).

### Пример `config.json`:
```json
{
    "user_name": "testuser",
    "computer_name": "testpc",
    "file_system_path": "system.zip",
    "startup_script_path": "script.txt"
}
```

### Пример `script.txt`:
```plaintext
ls
cd root/dir1
whoami
```

### 4. Запустите эмулятор
Используйте следующую команду для запуска программы:

```bash
python main.py --filesystem system.zip --config config.json
```

---

## Как работает программа

1. При запуске программа загружает:
   - Архив виртуальной файловой системы (`system.zip`).
   - Настройки из файла `config.json`.
   - Стартовые команды из файла `script.txt` (если указан в конфигурации).

2. Открывается графический интерфейс, где пользователь может вводить команды, используя текстовое поле.

3. Команды выполняются внутри виртуальной файловой системы, а их результаты отображаются в текстовом поле.

4. Пользователь может взаимодействовать с эмулятором, как в обычной командной строке UNIX, до выполнения команды `exit`.

---

## Пример использования

### 1. Список содержимого текущей директории:
```plaintext
ls
```

### 2. Переход в поддиректорию `root/dir1`:
```plaintext
cd root/dir1
```

### 3. Перемещение файла `file1.txt` из директории `dir1` в `dir2`:
```plaintext
mv root/dir1/file1.txt root/dir2/file1.txt
```

### 4. Отображение текущего пользователя:
```plaintext
whoami
```

### 5. Завершение работы эмулятора:
```plaintext
exit
```

---

## Структура проекта
```plaintext
Homework1/
├── main.py           # Основной файл программы
├── config.json       # Конфигурационный файл
├── script.txt        # Файл стартовых команд
├── system.zip        # Архив виртуальной файловой системы
├── README.md         # Документация (этот файл)
```

---

## Требования

- Python 3.6 или выше.
- Модули:
  - `zipfile`
  - `argparse`
  - `json`
  - `tkinter`

---

## Примечания
- Для обеспечения безопасности используйте правильные пути к файлам в `config.json`.
```

---

Скопируйте этот текст в файл `README.md` в вашем репозитории на GitHub. Если нужно добавить или изменить что-то, дайте знать! 😊
