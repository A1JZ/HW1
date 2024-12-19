import posixpath
import zipfile
import argparse
import json
import sys
import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class VShell:
    def __init__(self, filesystem_path, config_path=None):
        """Инициализация виртуальной оболочки."""
        self.filesystem = zipfile.ZipFile(filesystem_path)
        self.current_path = ""
        self.config = self._load_config(config_path) if config_path else {}
        self.user_name = self.config.get("user_name", "user")
        self.computer_name = self.config.get("computer_name", "vshell")
        self.script_path = self.config.get("startup_script_path")
        self.gui = None  # Ссылка на GUI будет установлена позже

    def _load_config(self, config_path):
        """Загрузка конфигурационного файла JSON."""
        with open(config_path, 'r') as file:
            return json.load(file)

    def _get_directories(self):
        filenames = [f.filename for f in self.filesystem.infolist()]
        directories = set()
        for name in filenames:
            parts = name.split('/')
            for i in range(1, len(parts)):
                directories.add('/'.join(parts[:i]))
        print(f"DEBUG: Directories found: {directories}")  # Для отладки
        return directories

    def ls(self, path=""):
        """Отображение содержимого директории."""
        if path:
            target_path = self._resolve_path(path)
        else:
            target_path = self.current_path

        if target_path:
            target_path += "/" if not target_path.endswith("/") else ""

        items = {f.filename for f in self.filesystem.infolist() if f.filename.startswith(target_path)}
        print(f"DEBUG: Items found in {target_path}: {items}")  # Для отладки
        if not items:
            return f"No such directory: {path or self.current_path}"

        children = set()
        for item in items:
            relative = item[len(target_path):]
            if relative:
                part = relative.split('/')[0]
                children.add(part)

        result = "\n".join(sorted(children))
        return result if result else f"No files in {path or self.current_path}."

    def cd(self, path=""):
        """Смена текущей директории."""
        if path == "..":
            if self.current_path == "":
                return "Already in the root directory."
            self.current_path = posixpath.dirname(self.current_path)
            return f"Changed directory to {self.current_path}" if self.current_path else "Changed to root directory."

        target_path = self._resolve_path(path)
        directories = self._get_directories()

        if target_path == "":
            self.current_path = ""
            return "Changed to root directory."

        if target_path not in directories:
            return f"No such directory: {path}"
        self.current_path = target_path
        return f"Changed directory to {self.current_path}"

    def mv(self, src, dest):
        """Перемещение файла или директории (симуляция)."""
        src_path = self._resolve_path(src)
        dest_path = self._resolve_path(dest)

        print(f"DEBUG: Moving from {src_path} to {dest_path}")  # Для отладки

        # Проверяем, существует ли источник
        if not any(f.filename.startswith(src_path) for f in self.filesystem.infolist()):
            return f"Source not found: {src}"

        # Проверяем, существует ли директория назначения
        directories = self._get_directories()
        if dest_path != "" and dest_path not in directories:
            return f"Destination not found: {dest}"

        # Симуляция перемещения файлов
        moved_files = []
        for file in self.filesystem.infolist():
            if file.filename.startswith(src_path):
                relative_path = file.filename[len(src_path):].lstrip('/')
                new_name = posixpath.join(dest_path, relative_path).strip("/")
                moved_files.append((file.filename, new_name))

        if not moved_files:
            return f"No files moved from {src} to {dest}."

        for old_name, new_name in moved_files:
            print(f"DEBUG: Moved {old_name} -> {new_name}")

        return f"Successfully moved {len(moved_files)} item(s) from {src} to {dest}."

    def whoami(self):
        """Вывод имени текущего пользователя."""
        return self.user_name

    def exit(self):
        """Выход из эмулятора."""
        if self.gui:
            self.gui.root.quit()
        else:
            sys.exit()

    def _resolve_path(self, path):
        """Приведение пути к абсолютному формату."""
        if path.startswith("/"):
            return path.strip("/")
        if path == "~" or path == "":
            return ""
        combined_path = posixpath.join(self.current_path, path)
        normalized_path = posixpath.normpath(combined_path)
        return normalized_path.strip("/")

    def execute_command(self, command):
        """Исполнение команды."""
        cmd = command.strip().split(maxsplit=1)
        print(f"DEBUG: Command = {cmd}")  # Для отладки

        if not cmd:
            return ''

        command = cmd[0].lower()
        args = cmd[1].split(maxsplit=1) if len(cmd) > 1 else []
        print(f"DEBUG: Args = {args}")  # Для отладки

        output = ''
        if command == "ls":
            output = self.ls(*args)
        elif command == "cd":
            output = self.cd(*args)
        elif command == "mv":
            if len(args) < 2:
                output = "Usage: mv <source> <destination>"
            else:
                output = self.mv(args[0], args[1])
        elif command == "whoami":
            output = self.whoami()
        elif command == "exit":
            output = "Exiting VShell..."
            self.exit()
        else:
            output = f"Unknown command: {command}"
        return output


class VShellGUI:
    def __init__(self, shell):
        self.shell = shell
        self.shell.gui = self
        self.root = tk.Tk()
        self.root.title(f"{self.shell.user_name}@{self.shell.computer_name}")
        self.create_widgets()
        self.display_prompt()

    def create_widgets(self):
        self.text_area = ScrolledText(self.root, state='disabled', wrap='word')
        self.text_area.pack(expand=True, fill='both')
        self.entry = tk.Entry(self.root)
        self.entry.bind('<Return>', self.execute_command)
        self.entry.pack(fill='x')
        self.entry.focus()

    def display_prompt(self):
        prompt = f"{self.shell.user_name}@{self.shell.computer_name}:{self.shell.current_path}$ "
        self.append_text(prompt)

    def append_text(self, text):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, text)
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)

    def execute_command(self, event):
        command = self.entry.get().strip()
        if command:
            self.append_text(command + '\n')
            output = self.shell.execute_command(command)
            if output:
                self.append_text(output + '\n')
        self.entry.delete(0, tk.END)
        if command.lower() != 'exit':
            self.display_prompt()

    def run(self):
        self.root.mainloop()


def main():
    parser = argparse.ArgumentParser(description="VShell Emulator")
    parser.add_argument("--filesystem", required=True, help="Path to the ZIP filesystem.")
    parser.add_argument("--config", required=True, help="Path to the JSON config file.")
    args = parser.parse_args()

    try:
        shell = VShell(args.filesystem, args.config)
        gui = VShellGUI(shell)
        gui.run()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()