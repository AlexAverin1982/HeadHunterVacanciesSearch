from src.dictionary_class import Dictionary
from src.display_options_class import DisplayOptions
from src.menu_class import Menu
from src.search_engine_class import VacanciesSearchEngine
from src.search_parameters_class import SearchParameters
from src.sort_parameters_class import SortParameter
from src.vacancy_class import Vacancy


class Application:
    work_is_over: bool = False

    @classmethod
    def terminate(cls):
        cls.work_is_over = True

    def __init__(self):

        self.search_params = SearchParameters()
        self.search_engine = VacanciesSearchEngine()
        self.vacancies = []
        self.vacancies_by_id = {}

        self.sort_parameters = [SortParameter(SortParameter.SALARY_MIN)]

        self.menus: dict = {}
        self.current_menu: Menu | None = None
        self.display_options = DisplayOptions()

    def show_search_parameters(self):
        print('Параметры поиска')
        print(self.search_params)

    def show_current_menu(self):
        """
        Отображаем текущее меню приложения
        """
        print(self.current_menu.caption)
        print('-' * 100 + '\n')
        if self.display_options.always_show_search_parameters:
            self.show_search_parameters()

        print(self.current_menu)
        print(f'Сейчас найдено {len(self.vacancies)} вакансий')

    def change_search_params(self):
        self.current_menu = self.menus['change_search_params']

    def find_vacancies(self) -> None:
        """
        Ищем вакансии по текущим параметрам
        """
        vac_data = self.search_engine.find_vacancies_with_parameters(self.search_params.params(),
                                                                     self.search_params.search_limit)
        # resetting search results
        self.vacancies = []
        self.vacancies_by_id = {}

        for item in vac_data:
            vac = Vacancy(item)
            self.vacancies.append(vac)
            self.vacancies_by_id[vac.id] = len(self.vacancies) - 1

    def set_search_limit(self) -> None:
        valid_input = False
        search_limit = 0
        while not valid_input:
            try:
                search_limit = int(input('Введите максимальное число искомых вакансий: '))
                valid_input = True
            except ValueError:
                print('Введите целое число')
        self.search_params.search_limit = search_limit
        if search_limit < 100:
            self.search_params.page_items_count = search_limit

    def set_search_area(self) -> None:
        from hh_dictionaries_class import HeadHunterApiDictionaries
        print('Как вы хотите указать регион?')
        print('1. Ввести код региона')
        print('2. Выбрать код региона из списка всех регионов')
        print('3. Подобрать регион по подстроке\n')
        print('4. Отменить выбор')

        valid_input = False
        user_response = 4
        while not valid_input:
            try:
                user_response = int(input('Ваш выбор: '))
                valid_input = user_response in range(1, 5)
                if not valid_input:
                    print('Введите 1, 2, 3 или 4')
                    continue

            except ValueError:
                print('Введите 1, 2, 3 или 4')
        if user_response == 1:
            valid_input = False
            while not valid_input:
                try:
                    self.search_params.area = int(input('Введите код региона (113 - вся Россия): '))
                    valid_input = True
                except ValueError:
                    print('Введен неверный код')
        if user_response == 2:
            print('Выберите регион: ')

            HeadHunterApiDictionaries.list_of_areas()
        elif user_response == 4:
            return

    def return_to_main_menu(self):
        self.current_menu = self.menus['main_menu']

    def init_menus(self) -> None:
        self.menus = {'main_menu': Menu('Добро пожаловать в приложение для поиска вакансий с сайта HeadHunter.ru',
                                        [('Изменить параметры поиска', self.change_search_params),
                                         ('Найти вакансии', self.find_vacancies),
                                         ('Просмотреть найденные вакансии', self.find_vacancies),
                                         ('Отфильтровать найденные вакансии', self.find_vacancies),
                                         ('Отсортировать найденные вакансии', self.find_vacancies),
                                         ('Сохранить найденные вакансии в файл', self.find_vacancies),
                                         ('Загрузить вакансии из файла', self.find_vacancies),
                                         ('Выйти из программы.', Application.terminate),
                                         ]
                                        ),
                      'change_search_params': Menu('Укажите параметры поиска:',
                                                   [('Указать регион', self.set_search_area),
                                                    ('Указать минимальную зарплату', self.find_vacancies),
                                                    ('Указать максимальную зарплату', Application.terminate),
                                                    ('Указать число вакансий', self.set_search_limit),
                                                    ('Указать отрасль', Application.terminate),
                                                    ('Установить параметры поика по умолчанию', Application.terminate),
                                                    ('Вернуться в главное меню', self.return_to_main_menu),
                                                    ('Выйти из программы', Application.terminate)
                                                    ]
                                                   ),
                      }
        """
          self.area: int = 113  # whole Russia
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
        """

        self.current_menu = self.menus['main_menu']

    def run(self) -> None:
        self.search_params.area = 10
        while not Application.work_is_over:

            self.show_current_menu()
            user_response = input('Ваш выбор: ')
            if user_response.isdigit():
                user_response = int(user_response) - 1
                self.current_menu.items[user_response][1]()

    # def sort_vacancies(self):
    #     for sort_param in self.sort_parameters:
    #         pass
