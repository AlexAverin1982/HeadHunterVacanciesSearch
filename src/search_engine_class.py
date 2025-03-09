import requests
import json


class VacanciesSearchEngine:
    def __init__(self):
        pass

    def find_vacancies_with_parameters(self, search_params: dict, search_limit: int = 0) -> list:
        # взято с https://habr.com/ru/articles/666062/
        # search_params = {
        #     #'employer_id': 3529,  # ID 2ГИС
        #     'area': 32,         # Поиск в Иваново
        #     'page': 10,         # Номер страницы
        #     'per_page': 100       # Кол-во вакансий на 1 странице
        # }
        result = []
        page = 0
        while True:
            search_params['page'] = page
            req = requests.get('https://api.hh.ru/vacancies', search_params)
            if req.ok:
                data_str = req.content.decode()
                vac_data = json.loads(data_str)
                # print(json_data)
                req.close()
                result.extend(vac_data.get('items', []))
                if search_limit:
                    if len(result) >= search_limit:
                        result = result[:search_limit + 1]
                        break
                page += 1
            else:
                break
        return result
