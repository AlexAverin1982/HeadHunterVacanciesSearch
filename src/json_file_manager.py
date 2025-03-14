import os
import jsonpickle

from src.storage_manager_class import StorageManager
from typing import Any, Callable
import json
"""
Создать класс для сохранения информации о вакансиях в JSON-файл. 
"""

class JSONFileManager(StorageManager):
    def __init__(self, storage_name: str, working_dir: str = '', method: Callable | None = None):
        super().__init__(storage_name)
        self.filename: str = storage_name
        self.working_dir: str = working_dir
        self.extension = '.json'
        self.serialization_method: Callable = method

        if not self.filename.endswith(self.extension):
            self.filename += self.extension

    def save(self, content: Any, append: bool) -> None:
        """
        сохранение content в файл
        :param content: - данные, которые надо записать
        :param append - если True, дозаписывает content в конец существующего файла, если False - перезаписывает
        """
        full_filename = os.path.join(self.working_dir, self.filename)
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=True)
        # json_string = jsonpickle.encode(content, include_properties=True, indent=4)
        # json_string = jsonpickle.encode(content)

        if self.serialization_method:
            json_string = json.dumps(content, default=self.serialization_method, ensure_ascii=False, indent=4)
        else:
            json_string = json.dumps(content, ensure_ascii=False, indent=4)
        # print(json_string)

        if append:
            write_mode = 'a'
        else:
            write_mode = 'w'
        with open(full_filename, write_mode) as f:
            json.dump(json_string, f, ensure_ascii=False, indent=4)

    def full_filename(self) -> str:
        """полный путь к файлу"""
        return os.path.join(self.working_dir, self.filename)


    def load(self, conditions: Any | None = None) -> Any:
        pass

    def delete(self, conditions: Any | None = None) -> Any:
        pass