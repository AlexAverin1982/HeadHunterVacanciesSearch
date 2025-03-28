import codecs
import json
import os
from typing import Any, Callable

from src.misc_tools import vacancy_complies
from src.storage_manager_class import StorageManager
from src.vacancy_class import Vacancy


class JSONFileManager(StorageManager):
    """
    Класс для сохранения информации о вакансиях в JSON-файл.
    """

    def __init__(self, storage_name: str, working_dir: str = "", method: Callable | None = None):  # type: ignore
        """
        конструктор
        :param storage_name:    имя файла
        :param working_dir:     каталог для сохранения
        :param method:          метод для сохранения данных класса в строку json
        """
        super().__init__(storage_name)
        self.filename: str = storage_name
        self.working_dir: str = working_dir
        self.extension = ".json"
        self.serialization_method: Callable = method        # type: ignore[assignment]
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

        if self.serialization_method is not None:
            json_string = json.dumps(
                content, default=self.serialization_method, ensure_ascii=False, indent=4
            )
        else:
            json_string = json.dumps(content, ensure_ascii=False, indent=4)

        if append:
            write_mode = "a"
        else:
            write_mode = "w"
        # with open(full_filename, write_mode, encoding='') as f:
        #     json.dump(json_string, f, ensure_ascii=False, indent=4)

        with codecs.open(full_filename, write_mode, "utf-16") as f:  # or utf-8
            json.dump(json_string, f, ensure_ascii=False, indent=4)

    def full_filename(self) -> str:
        """полный путь к файлу"""
        return os.path.join(self.working_dir, self.filename)

    def load(
        self, conditions: Any | None = None, fail_if_none: bool = True
    ) -> list[Vacancy] | None:
        """
        загрузка из файла
        :param conditions - условия для фильтрации данных из файла
        :param fail_if_none: True: если свойство условия в вакансии не указано, вакансия считается неподходящей
        :return возвращает список объектов вакансий
        """
        result = []
        full_filename = os.path.join(self.working_dir, self.filename)
        if not os.path.exists(full_filename):
            raise FileNotFoundError
        with codecs.open(full_filename, "r", encoding="utf-16") as f:
            json_string = json.load(f)
        content = json.loads(json_string)

        if content and isinstance(content, dict):
            items = content.get("items")
            if items and isinstance(items, list):
                for item in items:
                    vacancy_data = item.get("_Vacancy__fields")
                    if vacancy_data:
                        if self.filter_method and self.filter_method(
                            vacancy_data, conditions, fail_if_none
                        ):
                            vacancy = Vacancy(vacancy_data)
                            result.append(vacancy)

        return result

    def delete(
        self,
        conditions: Any | None = None,
        fail_if_none: bool = True,
        delete_if_match: bool = False,
    ) -> None:
        """
        Удаление вакансий из файла по указанным параметрам
        :param conditions: параметры для указания вакансий, которые нужно удалить или оставить
        :param fail_if_none: True: если свойство условия в вакансии не указано, вакансия считается неподходящей
        :param delete_if_match - Если False, вакансии, подходящие по условиям остаются в файле
        """
        if os.path.exists(self.full_filename()):
            if delete_if_match:
                vacancies = self.load(fail_if_none)
                vacancies_to_save = [
                    v
                    for v in vacancies      # type: ignore[union-attr]
                    if not vacancy_complies(v.fields(), conditions, fail_if_none)       # type: ignore[arg-type]
                ]
                self.save(content={"items": vacancies_to_save}, append=False)
            else:
                vacancies = self.load(conditions, fail_if_none)
                self.save(content={"items": vacancies}, append=False)
        else:
            raise FileNotFoundError
