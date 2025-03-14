import os

from src.storage_manager_class import StorageManager
from typing import Any
"""
Создать класс для сохранения информации о вакансиях в JSON-файл. 
"""

class TextFileManager(StorageManager):
    def __init__(self, storage_name: str, working_dir: str = ''):
        super().__init__(storage_name)
        self.filename: str = storage_name
        self.working_dir: str = working_dir
        self.extension = '.txt'

        if not self.filename.endswith(self.extension):
            self.filename += self.extension

    def save(self, content: Any, append: bool) -> None:
        """
        сохранение content в файл
        :param content: - данные, которые надо записать
        :param append - если True, дозаписывает content в конец существующего файла, если False - перезаписывает
        """
        full_filename = os.path.join(self.working_dir, self.filename)
        if append:
            write_mode = 'a'
        else:
            write_mode = 'w'
        with open(full_filename, write_mode) as f:
            f.write(content)

    def full_filename(self) -> str:
        """полный путь к файлу"""
        return os.path.join(self.working_dir, self.filename)


    def load(self, conditions: Any | None = None) -> Any:
        pass

    def delete(self, conditions: Any | None = None) -> Any:
        pass
