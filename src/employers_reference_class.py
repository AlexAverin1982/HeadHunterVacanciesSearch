import json

import requests


class EmployersReference:

    def add_employers(self, employers_data: list | dict, allow_without_vacancies: True = False) -> None:
        """
        Добавляем одного или нескольких работодателей в справочник
        """
        def add_employer(employer_data: dict) -> None:
            """
            Добавляем одного работодателя в справочник
            """
            id = employer_data.get('id')
            if not id:
                return
            elif self.items_by_id.get(id):
                return
            open_vacancies = employer_data.get('open_vacancies', 0)
            if (open_vacancies == 0) and (not allow_without_vacancies):
                return
            name = employer_data.get('name')
            url = employer_data.get('url')
            alternate_url = employer_data.get('alternate_url')
            # open_vacancies = employer_data.get('open_vacancies')
            area_id = employer_data.get('area', {}).get('id')
            if isinstance(open_vacancies, int):
                self.items_by_name[name] = {'id': id,
                                            'url': url,
                                            'alternate_url': alternate_url,
                                            'open_vacancies': open_vacancies,
                                            'area_id': area_id}

                self.items_by_id[id] = {'name': name,
                                        'url': url,
                                        'alternate_url': alternate_url,
                                        'open_vacancies': open_vacancies,
                                        'area_id': area_id}

        if isinstance(employers_data, list):
            for employer_data in employers_data:
                add_employer(employer_data)
        elif isinstance(employers_data, dict):
            add_employer(employers_data)

    def __init__(self, allow_without_vacancies: bool):  # type ignore

        # self.items_tree_by_name: dict = {}
        # self.items_tree_by_id: dict = {}
        # self.items_by_name: dict = {}
        # self.items_by_id: dict = {}
        # self.items_by_name: dict = {}
        # self.top_level_items_dict_by_id: dict = {}
        self.allow_without_vacancies: bool = allow_without_vacancies
        self.items_by_name: dict = {}
        self.items_by_id: dict = {}

        # pages_count = 20
        #
        # for page in range(pages_count):
        #     print(page)
        #     url = f"https://api.hh.ru/employers?per_page=100&page={page}"
        #     req = requests.get(url)
        #     if req.ok:
        #         data_str = req.content.decode()
        #         req.close()
        #         all_employers_list = json.loads(data_str)
        #         self.add_employers(all_employers_list.get('items'), self.allow_without_vacancies)
        #     else:
        #         req.close()

    def item_code_is_valid(self, new_item_code: str) -> bool:  # type: ignore
        """проверка, принадлежит ли указанный код данному справочнику"""
        return new_item_code in self.items_by_id.keys()

    def add_by_id(self, emp_id: str) -> None:
        """
        Добавляем данные о работодателе по id
        """
        req = requests.get(f"https://api.hh.ru/employers/{emp_id}")
        if req.ok:
            data_str = req.content.decode()
            req.close()
            employer_data = json.loads(data_str)
            self.add_employers(employer_data, allow_without_vacancies=True)

    def get_by_id(self, emp_id: str) -> dict:
        """
        Получаем информацию о работодателе
        """
        if self.item_code_is_valid(emp_id):
            return self.items_by_id[emp_id]
        else:
            self.add_by_id(emp_id)
        if self.item_code_is_valid(emp_id):
            return self.items_by_id[emp_id]
        else:
            return {}
