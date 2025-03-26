import os
from plistlib import loads

import jsonpickle

from src.storage_manager_class import StorageManager
from typing import Any, Callable
import json
import codecs

from src.vacancy_class import Vacancy

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
        self.filter_method: Callable | None = None

        if not self.filename.endswith(self.extension):
            self.filename += self.extension

    def save(self, content: Any, append: bool) -> None:
        """
        сохранение content в файл
        :param content: - данные, которые надо записать
        :param append - если True, дозаписывает content в конец существующего файла, если False - перезаписывает
        """
        full_filename = os.path.join(self.working_dir, self.filename)
        # jsonpickle.set_preferred_backend('json')
        # jsonpickle.set_encoder_options('json', ensure_ascii=True)
        # json_string = jsonpickle.encode(content, include_properties=True, indent=4)
        # json_string = jsonpickle.encode(content)

        if self.serialization_method:
            json_string = json.dumps(content, default=self.serialization_method, ensure_ascii=False, indent=4)
        else:
            json_string = json.dumps(content, ensure_ascii=False, indent=4)

        if append:
            write_mode = 'a'
        else:
            write_mode = 'w'
        # with open(full_filename, write_mode, encoding='') as f:
        #     json.dump(json_string, f, ensure_ascii=False, indent=4)

        with codecs.open(full_filename, write_mode, "utf-16") as f:  # or utf-8
            json.dump(json_string, f, ensure_ascii=False, indent=4)

    def full_filename(self) -> str:
        """полный путь к файлу"""
        return os.path.join(self.working_dir, self.filename)

    def load(self, conditions: Any | None = None, fail_if_none: bool = True) -> list[Vacancy] | None:
        """
        загрузка из файла
        :param conditions - условия для фильтрации данных из файла
        :param fail_if_none: True: если свойство условия в вакансии не указано, вакансия считается неподходящей
        """
        result = []
        full_filename = os.path.join(self.working_dir, self.filename)
        if not os.path.exists(full_filename):
            raise FileNotFoundError
        with codecs.open(full_filename, 'r', encoding='utf-16') as f:
            json_string = json.load(f)
        content = json.loads(json_string)

        if content and isinstance(content, dict):
            items = content.get('items')
            if items and isinstance(items, list):
                for item in items:
                    vacancy_data = item.get('_Vacancy__fields')
                    if vacancy_data:
                        if self.filter_method and self.filter_method(vacancy_data, conditions, fail_if_none):
                            vacancy = Vacancy(vacancy_data)
                            result.append(vacancy)

        return result

    def delete(self, conditions: Any | None = None) -> Any:
        pass
