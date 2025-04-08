from abc import ABC, abstractmethod
from typing import Any

"""
Абстрактный класс, который обязывает реализовать методы для:
- добавления вакансий в файл,
- получения данных из файла по указанным критериям и
- удаления информации о вакансиях.

Данный класс выступит в роли основы для коннектора, заменяя который (класс-коннектор),
можно использовать в качестве хранилища одну из баз данных
или удаленное хранилище со своей специфической системой обращений.
"""


class StorageManager(ABC):
    @abstractmethod
    def __init__(self, storage_name: str):  # type: ignore
        pass

    @abstractmethod
    def save(self, content: Any, append: bool) -> None:
        """
        сохранение content в файл
        :param content: - данные, которые надо записать
        :param append - если True, дозаписывает content в конец существующего файла, если False - перезаписывает
        """
        pass

    @abstractmethod
    def load(self, conditions: Any | None = None, fail_if_none: bool = True) -> Any:
        """
        загрузка из файла
        :param conditions - условия для фильтрации данных из файла
        :param fail_if_none: True: если свойство условия в вакансии не указано, вакансия считается неподходящей
        :return возвращает список объектов вакансий
        """
        pass

    @abstractmethod
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
        pass
