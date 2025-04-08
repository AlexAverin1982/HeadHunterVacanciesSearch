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

    def __init__(self, storage_name: str = "", working_dir: str = "", method: Callable | None = None):  # type: ignore
        """
        конструктор
        :param storage_name:    имя файла
        :param working_dir:     каталог для сохранения
        :param method:          метод для сохранения данных класса в строку json
        """
        super().__init__(storage_name)
        self.__filename: str = "new_vacancies.json"
        if storage_name:
            self.__filename = storage_name
        self.working_dir: str = working_dir
        self.extension = ".json"
        self.serialization_method: Callable = method  # type: ignore[assignment]
        self.filter_method: Callable | None = None

        if not self.filename.endswith(self.extension):
            self.filename += self.extension

    @property
    def filename(self) -> str:
        """
        :return: Имя файла с данными
        """
        return self.__filename

    @filename.setter
    def filename(self, new_filename: str) -> None:
        """
        Установка имени файла
        :param new_filename:имя файла для работы
        """
        self.__filename = new_filename

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

        if append:
            if os.path.exists(full_filename):
                old_vacs = self.load()
                if old_vacs:
                    old_vacs_ids = {
                        old_vac.properties.get("id", {}).get("value"): ind
                        for ind, old_vac in enumerate(old_vacs)
                    }

                    new_vacs = content.get("items")
                    new_vacs_ids = {
                        new_vac.properties.get("id", {}).get("value"): ind
                        for ind, new_vac in enumerate(new_vacs)
                    }
                    old_ids_set = set(old_vacs_ids.keys())
                    new_ids_set = set(new_vacs_ids.keys())

                    dups = old_ids_set.intersection(new_ids_set)
                    if dups:
                        new_vacs_inds_to_delete = []

                        for new_vac_id, new_ind in new_vacs_ids.items():
                            old_ind = old_vacs_ids.get(new_vac_id)
                            if old_ind is not None:
                                s1 = str(old_vacs[old_ind]).lower()
                                s2 = str(new_vacs[new_ind]).lower()
                                if s1 == s2:
                                    new_vacs_inds_to_delete.append(new_ind)

                        new_vacs_inds_to_delete.sort(reverse=True)
                        for ind in new_vacs_inds_to_delete:
                            del new_vacs[ind]
                        if not len(new_vacs):
                            return
                        content = {"items": old_vacs}
                    old_vacs.extend(new_vacs)
                    content = {"items": old_vacs}
        if self.serialization_method is not None:
            json_string = json.dumps(
                content, default=self.serialization_method, ensure_ascii=False, indent=4
            )
        else:
            json_string = json.dumps(content, ensure_ascii=False, indent=4)

        with codecs.open(full_filename, "w", "utf-8") as f:  # or utf-8
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
        with codecs.open(full_filename, "r", encoding="utf-8") as f:
            json_string = json.load(f)
        content = json.loads(json_string)

        if content and isinstance(content, dict):
            items = content.get("items")
            if items and isinstance(items, list):
                for item in items:
                    vacancy_data = item.get("_Vacancy__fields")
                    if vacancy_data:
                        if conditions:
                            if self.filter_method and self.filter_method(
                                    vacancy_data, conditions, fail_if_none
                            ):
                                vacancy = Vacancy(vacancy_data)
                                result.append(vacancy)
                        else:
                            vacancy = Vacancy(vacancy_data)
                            result.append(vacancy)

        return result

    def delete(
            self,
            conditions: Any | None = None,
            delete_if_none: bool = True,
            delete_if_match: bool = False,
    ) -> int:
        """
        Удаление вакансий из файла по указанным параметрам
        :param conditions: параметры для указания вакансий, которые нужно удалить или оставить
        :param delete_if_none:  Если True, удалять запись в файле, если нет поля, указанного в условии
        :param delete_if_match: Если True, удалять запись в файле, если условия удовлетворены
        """
        if os.path.exists(self.full_filename()):
            # загружаем все вакансии из файла
            vacancies = self.load()
            ids_to_delete = []
            old_count = len(vacancies)
            for ind, v in enumerate(vacancies):  # type: ignore[union-attr]
                if delete_if_match == vacancy_complies(v.fields(), conditions,
                                                       delete_if_none):  # type: ignore[arg-type]
                    # print(str(v))
                    # del v
                    ids_to_delete.append(ind)
            ids_to_delete.sort(reverse=True)
            for i in ids_to_delete:
                del vacancies[i]
            if vacancies:
                new_count = len(vacancies)
                self.save(content={"items": vacancies}, append=False)
                return old_count - new_count
            else:
                return 0
        else:
            raise FileNotFoundError
