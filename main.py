import requests
import json

if __name__ == '__main__':
    params = {
        #'employer_id': 3529,  # ID 2ГИС
        'area': 32,         # Поиск в Иваново
        'page': 10,         # Номер страницы
        'per_page': 100       # Кол-во вакансий на 1 странице
    }
    req = requests.get('https://api.hh.ru/vacancies', params)
    data_str = req.content.decode()
    json_data = json.loads(data_str)
    req.close()