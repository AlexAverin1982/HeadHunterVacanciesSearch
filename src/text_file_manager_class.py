import os
from typing import Any

from src.misc_tools import vacancy_complies
from src.storage_manager_class import StorageManager


class TextFileManager(StorageManager):
    """
    Класс для сохранения информации о вакансиях в текстовый файл.
    """

    def __init__(self, storage_name: str, working_dir: str = ""):  # type: ignore
        """
        Конструктор менеджера
        :param storage_name: имя файла
        :param working_dir: имя каталога для сохранения
        """
        super().__init__(storage_name)
        self.filename: str = storage_name
        self.working_dir: str = working_dir
        self.extension = ".txt"

        if not self.filename.endswith(self.extension):
            self.filename += self.extension

    def save(self, content: Any, append: bool, encoding: str = "utf-8") -> None:
        """
        сохранение content в файл
        :param content: - данные, которые надо записать
        :param append - если True, дозаписывает content в конец существующего файла, если False - перезаписывает
        :param encoding - кодировка симоволов
        """
        full_filename = os.path.join(self.working_dir, self.filename)
        if append:
            write_mode = "a"
        else:
            write_mode = "w"
        with open(full_filename, write_mode, encoding=encoding) as f:
            f.write(content)

    def full_filename(self) -> str:
        """полный путь к файлу"""
        return os.path.join(self.working_dir, self.filename)

    def load(
            self,
            conditions: Any | None = None,
            fail_if_none: bool = False,
            encoding: str = "utf-8",
    ) -> list[dict] | None:
        """
        загрузка из файла
        :param conditions - условия для фильтрации данных из файла
        :param fail_if_none: True: если свойство условия в вакансии не указано, вакансия считается неподходящей
        :param encoding кодировка
        :return возвращает список объектов вакансий
        """

        with open(self.full_filename(), "r", encoding=encoding) as f:
            content = f.readlines()
        if content:
            result: list = []
            item: dict = {}
            for line in content:
                line = line.replace("\n", "")
                if line.find(": ") == -1:
                    if len(item.keys()):
                        result.append(item)
                        item = {}
                else:
                    key = value = ""
                    try:
                        key, value = line.split(": ")
                    except ValueError:
                        key = line.split(": ")[0]
                        value = ""
                    finally:
                        item[key] = value
            return result
        else:
            return None

    def delete(
            self,
            conditions: Any | None = None,
            delete_if_none: bool = True,
            delete_if_match: bool = False,
            encoding: str = "utf-8",
    ) -> None:
        """
        Удаление вакансий из файла по указанным параметрам
        :param conditions: параметры для указания вакансий, которые нужно удалить или оставить
        :param delete_if_none: True: если свойство условия в вакансии не указано, вакансия считается неподходящей
        :param delete_if_match - Если False, вакансии, подходящие по условиям остаются в файле
        :param encoding кодировка файла
        """
        if os.path.exists(self.full_filename()):
            if delete_if_match:
                vacancies = self.load(delete_if_none)
                vacancies_to_save = [
                    v
                    for v in vacancies  # type: ignore[union-attr]
                    if not vacancy_complies(v.fields(), conditions, delete_if_none)
                    # type: ignore[arg-type, union-attr]
                ]
                self.save(content={"items": vacancies_to_save}, append=False)
            else:
                vacancies = self.load(conditions, delete_if_none)
                self.save(content={"items": vacancies}, append=False)
        else:
            raise FileNotFoundError
