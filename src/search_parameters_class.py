from typing import Any


class SearchParameters:
    """
    Параметры поиска вакансий
    """

    def reset(self) -> None:
        self.__area: int = 113  # whole Russia регион поиска
        self.page_items_count: int = 100  # количество результатов поиска на странице
        self.page: int = 0  # номер страницы для просмотра
        self.search_field: str = ''  # поле поиска ключевого слова
        self.experience: str = ''  # требуемый опыт работы
        self.text: str = ''  # ключевое слово для поиска
        self.employment: str = ''  # тип занятости
        self.search_limit = 0  # количество вакасний, которые надо найти

    def __init__(self, owner: Any | None = None):
        self.__area: int = 113  # whole Russia
        self.page_items_count: int = 100
        self.page: int = 0
        self.search_field: str = ''
        self.experience: str = ''
        self.text: str = ''
        self.employment: str = ''
        self.__area_name = ''
        self.salary_min: int = 0
        self.salary_max: int = 0
        self.search_limit = 0
        self.owner: Any | None = owner

    @property
    def area(self) -> int:
        return self.__area


    def __str__(self):
        result = ""
        if self.__area == 113:
            result = "Регион поиска вакансий: вся Россия\n"
        else:
            result = f"Регион поиска вакансий: {self.__area_name}\n"

        if self.employment:
            result += f"Искомая должность: {self.employment}\n"
        else:
            result += "Искомая должность: не указана\n"

        if self.salary_min:
            result += f"Минимальная зарплата: {self.salary_min} руб.\n"
        else:
            result += "Минимальная зарплата: не указана\n"
        if self.salary_max:
            result += f"Максимальная зарплата: {self.salary_max} руб.\n"
        else:
            result += "Максимальная зарплата: не указана\n"
        if self.employment:
            result += f"Требуемый опыт: {self.employment}\n"
        else:
            result += "Требуемый опыт: не указан\n"
        if self.search_limit:
            result += f"Количество вакансий: {self.search_limit}\n"
        else:
            result += "Количество вакансий: не указано\n"

        return result

    def params(self) -> dict:
        result = {'area': self.__area,
                  'page': self.page,
                  'per_page': self.page_items_count}
        if self.text:
            result['text'] = self.text
        if self.search_field:
            result['search_field'] = self.search_field
        if self.experience:
            result['experience'] = self.experience
        return result

    def show(self):
        print(self.params())

    # def set_key_words(self, key_words: list[str]):
    #     words = ', '.join(key_words)

    @area.setter
    def area(self, new_area_code: int):
        from src.hh_dictionaries_class import HeadHunterApiDictionaries
        if HeadHunterApiDictionaries.area_code_is_valid(new_area_code):
            self.__area = new_area_code
        else:
            raise ValueError

