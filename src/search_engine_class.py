import json

import requests

from src.fetcher_class import Fetcher


class VacanciesSearchEngine(Fetcher):
    """
    Класс, наследующийся от абстрактного класса, для работы с платформой hh.ru.
    Класс должен уметь подключаться к API и получать вакансии.
    """

    def __init__(self):  # type: ignore
        super().__init__()

    def __connection_ok(self) -> bool:
        """
        Проверка связи
        :return:  True - связь с сайтом есть
        """
        req = requests.get("https://api.hh.ru/vacancies")
        return req.ok

    def fetch(self, search_params: dict, search_limit: int = 0) -> list:            # type: ignore[override]
        """
        Получение данных о вакансиях по указанным параметрам и в указанном количестве
        :param search_params: параметры поиска
        :param search_limit: максимальное число записей
        :return:
        """
        # взято с https://habr.com/ru/articles/666062/
        # search_params = {
        #     #'employer_id': 3529,  # ID 2ГИС
        #     'area': 32,         # Поиск в Иваново
        #     'page': 10,         # Номер страницы
        #     'per_page': 100       # Кол-во вакансий на 1 странице
        # }
        if not self.__connection_ok():
            raise Exception("Связь с сайтом отсутствует")

        super().fetch(search_params, search_limit)
        del search_params["page"]
        result = []
        page = 0
        params = ""
        for name, value in search_params.items():
            params += f"{name}={value}&"
        while True:
            # search_params['page'] = page
            params1 = params + f"page={page}"
            req = requests.get(f"https://api.hh.ru/vacancies?{params1}")
            if req.ok:
                data_str = req.content.decode()
                vac_data = json.loads(data_str)
                # print(json_data)
                req.close()
                result.extend(vac_data.get("items", []))
                # if search_limit:
                #     if len(result) >= search_limit:
                #         result = result[:search_limit + 1]
                #         break
                page += 1
            else:
                break
        return result
