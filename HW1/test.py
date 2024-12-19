import unittest
from unittest.mock import patch
from main import VShell
import os

class TestVShell(unittest.TestCase):
    def setUp(self):
        """Инициализация для каждого теста"""
        # Указываем пути к реальным файлам, как это делается в основной программе
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Текущая директория
        self.filesystem_path = os.path.join(base_dir, 'system.zip')  # Путь к архиву
        self.config_path = os.path.join(base_dir, 'config.json')  # Путь к конфигу

        # Создаем экземпляр эмулятора оболочки, используя реальные файлы
        self.shell = VShell(self.filesystem_path, self.config_path)

    def test_ls_root(self):
        """Проверка команды ls в корневой директории."""
        output = self.shell.ls("root")  # Важно указывать абсолютный путь
        self.assertIn('file1.txt', output)
        self.assertIn('file2.txt', output)
        self.assertIn('dir1', output)
        self.assertIn('dir2', output)

    def test_ls_dir1(self):
        """Проверка команды ls в поддиректории dir1."""
        self.shell.cd('/root/dir1')  # Переход в поддиректорию с абсолютным путем
        output = self.shell.ls()
        self.assertIn('file3.txt', output)

    def test_ls_dir2(self):
        """Проверка команды ls в поддиректории dir2."""
        self.shell.cd('/root/dir2')  # Переход в поддиректорию с абсолютным путем
        output = self.shell.ls()
        self.assertIn('file4.txt', output)

    def test_cd_valid(self):
        """Проверка команды cd с существующей директорией."""
        result = self.shell.cd('/root/dir1')  # Абсолютный путь для перехода в dir1
        self.assertIn("Changed directory to root/dir1", result)
        self.assertEqual(self.shell.current_path, 'root/dir1')

    def test_cd_invalid(self):
        """Проверка команды cd с несуществующей директорией."""
        result = self.shell.cd('/root/nonexistent')  # Абсолютный путь к несуществующей директории
        self.assertIn("No such directory", result)

    def test_cd_parent(self):
        """Проверка команды cd для перехода в родительскую директорию."""
        self.shell.cd('/root/dir1')  # Переход в поддиректорию
        result = self.shell.cd('..')  # Переход в родительскую директорию
        self.assertIn("Changed directory to root", result)
        self.assertEqual(self.shell.current_path, 'root')  # Путь должен быть пустым (корень)

    def test_mv_valid(self):
        """Проверка команды mv для существующего файла."""
        result = self.shell.mv('/root/file1.txt', '/root/dir2')  # Абсолютные пути
        self.assertIn("Successfully moved", result)

    def test_mv_invalid_source(self):
        """Проверка команды mv с несуществующим файлом."""
        result = self.shell.mv('/root/nonexistent.txt', '/root/dir2')
        self.assertIn("Source not found", result)

    def test_mv_invalid_destination(self):
        """Проверка команды mv с несуществующей директорией назначения."""
        result = self.shell.mv('/root/file1.txt', '/root/nonexistent')
        self.assertIn("Destination not found", result)

    def test_whoami(self):
        """Проверка команды whoami."""
        output = self.shell.whoami()
        self.assertEqual(output, 'testuser')  # Ожидаем значение из config.json

    @patch('sys.exit')
    def test_exit(self, mock_exit):
        """Проверка команды exit."""
        self.shell.exit()
        mock_exit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
