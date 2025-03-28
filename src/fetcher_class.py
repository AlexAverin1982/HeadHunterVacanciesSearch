from abc import ABC, abstractmethod

class Fetcher(ABC):
    """
    Абстрактный класс для работы с API сервиса с вакансиями.
    """

    @abstractmethod
    def __init__(self):  # type: ignore
        pass

    # @abstractmethod
    # def __connection_ok(self) -> bool:
    #     """
    #     Проверка связи
    #     :return:  True - связь с сайтом есть
    #     """
    #     pass

    @abstractmethod
    def fetch(self, search_params: dict, search_limit: int = 0) -> None:
        """
        Метод для получения искомых данных по заданным параметрам
        :param search_params:  параметры
        :param search_limit:  максимальное число искомых записей
        :return:
        """
        pass
