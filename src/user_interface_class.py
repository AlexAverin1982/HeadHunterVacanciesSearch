import os
from msvcrt import getch
import json

from typing_extensions import Any, Callable

# from src.display_options_class import DisplayOptions
from src.menu_class import Menu
# from src.search_engine_class import VacanciesSearchEngine
# from src.search_parameters_class import SearchParameters
# from src.sort_parameters_class import SortParameter
# from src.text_file_manager_class import TextFileManager
# from src.vacancy_class import Vacancy
# from src.hh_reference_class import HeadHunterReference as HhRef
# from src.misc_tools import get_indices
# from src.json_file_manager import JSONFileManager


class UserInterface:

    def __init__(self, menu_handlers: dict | None = None):

        # self.search_params = SearchParameters()
        # self.search_engine = VacanciesSearchEngine()
        # self.vacancies = []
        # self.vacancies_by_id = {}
        #
        # self.sort_parameters = [SortParameter(SortParameter.SALARY_MIN)]

        self.__menus: dict = {}
        self.__menu_names: list = []
        # self.__vacancies: list = []
        self.__current_menu: Menu | None = None
        # self.__previous_menu: Menu | None = None
        self.__user_response: dict = {}
        self.__menu_handlers = menu_handlers
        self.__previous_menus: list = []
        self.init_menus()
        # self.__menu_items_handlers: dict[str: Callable] = {}

        # self.__previous_menu: Menu | None = None
        # self.display_options = DisplayOptions()

    def init_menus(self) -> None:
        if not self.__menu_handlers:
            self.__menu_handlers = {}

        self.__menu_handlers['Искать вакансии'] = self.__find_vacancies
        self.__menu_handlers['Вернуться в главное меню'] = self.return_to_main_menu

        main_menu = Menu(name='main_menu',
                         caption='Добро пожаловать в приложение для поиска вакансий с сайта HeadHunter.ru',
                         status_bar=self.__menu_handlers.get('vacancies_count'))

        self.__menus['main_menu'] = main_menu

        """
                                         # ('Отфильтровать найденные вакансии', self.find_vacancies),
                                         # ('Отсортировать найденные вакансии', self.find_vacancies),
                                         # ('Сохранить найденные вакансии в файл', self.find_vacancies),
                                        ),
                      'change_search_params': Menu('Укажите параметры поиска:',
                                                   [('Указать регион', self.set_search_area),
                                                    ('Указать минимальную зарплату', self.set_min_salary),
                                                    ('Указать подстроку для поиска', self.set_search_substring),
                                                    # ('Указать максимальную зарплату', Application.terminate),
                                                    ('Указать максимальное число вакансий', self.set_search_limit),
                                                    ('Указать отрасль', Application.terminate),
                                                    ('Указать профессию', Application.terminate),
                                                    ('Уточнить поиск вакансий без зарплаты',
                                                     self.set_igore_without_salary),
                                                    # ('Указать поле для поиска подстроки', Application.terminate),
                                                    ('Установить параметры поика по умолчанию', Application.terminate),
                                                    ('Вернуться в главное меню', self.return_to_main_menu),
                                                    ('Искать вакансии', self.find_vacancies)
                                                    ]
                                                   ),
                      'select_area': Menu('Как вы хотите указать регион?',
                                          [('Ввести код региона', self.set_area_code),
                                           ('Подобрать регион по подстроке', self.search_area_by_substring),
                                           ('Показать все регионы, сортировать в алфавитном порядке',
                                            self.show_all_regions_sorted_by_name),
                                           ('Показать все регионы, сортировать по коду',
                                            self.show_all_regions_sorted_by_code),
                                           ('Выводить региоры по иерхии, начиная со стран',
                                            self.show_regions_structured),
                                           ('Вернуться в прежнее меню', self.return_to_previous_menu),
                                           ('Отменить выбор региона', self.change_search_params),
                                           ('Вернуться в главное меню', self.return_to_main_menu),
                                           ('Вернуться в предыдущее меню', self.return_to_previous_menu),
                                           ('Выйти из программы', Application.terminate)
                                           ])

                      # print('3. Подобрать регион по подстроке\n')
                      }

        """

        main_menu.add_item(caption='Изменить параметры поиска', pos=0, function=self.__change_search_params)
        main_menu.add_item(caption='Искать вакансии', pos=1)
        main_menu.add_item(caption='Загрузить вакансии из файла', pos=98, function=self.__load_vacancies_from_file)
        main_menu.add_item(caption='Выйти из программы.', pos=99)
        # --------------------------------------------------------------------------------------------------------
        search_params_menu = Menu(name='change_search_params',
                         caption='Укажите параметры поиска:',
                         status_bar=self.__menu_handlers.get('vacancies_count'))
        self.__menus['change_search_params'] = search_params_menu
        search_params_menu.add_item(caption='Указать регион', pos=0, function=self.__set_area)
        search_params_menu.add_item(caption='Указать минимальную зарплату', pos=1, function=self.__set_min_salary)
        search_params_menu.add_item(caption='Указать подстроку для поиска', pos=2, function=self.__set_search_substring)
        search_params_menu.add_item(caption='Указать максимальное число вакансий', pos=3, function=self.__set_area)
        search_params_menu.add_item(caption='Указать отрасль', pos=4, function=self.__set_area)
        search_params_menu.add_item(caption='Указать профессию', pos=5, function=self.__set_area)
        search_params_menu.add_item(caption='Уточнить поиск вакансий без зарплаты', pos=6, function=self.__set_area)
        search_params_menu.add_item(caption='Установить параметры поика по умолчанию', pos=7, function=self.__set_area)
        search_params_menu.add_item(caption='Вернуться в главное меню', pos=8)
        search_params_menu.add_item(caption='Искать вакансии', pos=99)
        #               'change_search_params': Menu('Укажите параметры поиска:',
        #                                             ('Указать минимальную зарплату', self.set_min_salary),
        #                                             ('Указать подстроку для поиска', self.set_search_substring),
        #                                             ('Указать максимальное число вакансий', self.set_search_limit),
        #                                             ('Указать отрасль', UserInterface.terminate),
        #                                             ('Указать профессию', UserInterface.terminate),
        #                                             ('Уточнить поиск вакансий без зарплаты',
        #                                              self.set_igore_without_salary),
        #                                             ('Установить параметры поика по умолчанию', UserInterface.terminate),
        #                                             ('Вернуться в главное меню', self.return_to_main_menu),
        #                                             ('Искать вакансии', self.find_vacancies)
        #                                             ]
        #                                            ),

        select_area_menu = Menu(name='select_area', caption='Как вы хотите указать регион?')

        select_area_menu.add_item(caption='Ввести код региона', pos=0, function=self.__type_in_area_id)
        select_area_menu.add_item(caption='Подобрать регион по подстроке', pos=1,
                                  function=self.__search_area_by_substring)
        select_area_menu.add_item(caption='Показать все регионы, сортировать в алфавитном порядке', pos=2,
                                  function=self.__set_area)
        select_area_menu.add_item(caption='Показать все регионы, сортировать по коду', pos=3,
                                  function=self.__set_area)
        select_area_menu.add_item(caption='Выводить региоры по иерхии, начиная со стран', pos=4,
                                  function=self.__set_area)
        select_area_menu.add_item(caption='Отменить выбор региона', pos=5,
                                  function=self.return_to_previous_menu)
        select_area_menu.add_item(caption='Вернуться в главное меню', pos=6)
        select_area_menu.add_item(caption='Выйти из программы.', pos=7)

        self.__menus['select_area'] = select_area_menu
        self.__menu_names = ['main_menu', 'change_search_params', 'select_search_region', 'select_area']
        self.__current_menu = self.__menus['main_menu']

        self.update_menu_handlers()

        #               'select_area': Menu('Как вы хотите указать регион?',
        #                                    ('Подобрать регион по подстроке', self.search_area_by_substring),
        #                                    ('Показать все регионы, сортировать в алфавитном порядке',
        #                                     self.show_all_regions_sorted_by_name),
        #                                    ('Показать все регионы, сортировать по коду',
        #                                     self.show_all_regions_sorted_by_code),
        #                                    ('Выводить региоры по иерхии, начиная со стран',
        #                                     self.show_regions_structured),
        #

    def show_search_parameters(self, search_params: Any) -> None:
        print('Параметры поиска')
        print(search_params)

    def show_current_menu(self, info_pane: list | str = '') -> None:
        # Отображаем текущее меню приложения
        print('\n')
        print(self.__current_menu.caption)
        print('-' * 100 + '\n')
        if info_pane:
            if isinstance(info_pane, str):
                print(info_pane)
                print('\n')
            elif isinstance(info_pane, list):
                for ind, item in enumerate(info_pane):
                    print(f'{ind + 1}. {str(item)}')
                self.show_message()

        print(self.__current_menu)

        # print(f'Сейчас найдено {len(self.vacancies)} вакансий')

    def find_vacancies(self):
        pass

    def set_current_menu(self, menu_name: str):
        if menu_name in self.__menu_names:
            self.__previous_menus.insert(0, self.__current_menu)
            self.__current_menu = self.__menus[menu_name]

    def return_to_main_menu(self):
        self.set_current_menu('main_menu')
        self.__previous_menus = []

    def return_to_previous_menu(self):
        if len(self.__previous_menus):
            self.__current_menu = self.__previous_menus[0]
            self.__previous_menus = self.__previous_menus[1:]

    def __load_vacancies_from_file(self):
        """
        показать текущую папку файлов
        запросить имя файла / имя папки файлов
        определить тип файла
        по типу файла определить файловый менеджер
        послать ему информацию о файле
        получить от него вакансии
        отобразить информацию о готовности работать дальше
        :return:
        """
        par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
        par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
        data_dir = os.path.join(par_dir, "data")
        print(f'Файл будет загружен из каталога {data_dir}')
        filename = input('Введите имя файла (введите пустую строку для отмены): ')
        if not filename:
            return
        filetype_choice = '1'

        if filename.lower().endswith('.txt'):
            filetype_choice = '1'
        elif filename.lower().endswith('.csv'):
            filetype_choice = '2'
        elif filename.lower().endswith('.json'):
            filetype_choice = '3'

        self.__user_response = {'action': 'load vacancies from file',
                                'dir': data_dir,
                                'filename': filename,
                                'filetype': filetype_choice,
                                'additional request': "check if vacancies list is not empty"}

    def __find_vacancies(self):
        self.__user_response = {'action': 'find vacancies'}

    def sort_vacancies_list(self) -> None:
        print('Еще в разработке')
        input('Нажмите Enter')

    def __type_in_area_id(self):
        self.__user_response = {'action': 'set area id',
                                'id': input('Введите код региона (113 - вся Россия): ')}

    def __search_area_by_substring(self) -> None:
        """
        Запрос у пользователя подстроки для поиска региона
        """
        search_substring = input('Введите часть наименования региона (пустую строку для отмены):').lower()
        if search_substring:
            self.__user_response = {'action': 'search area by substring', 'substring': search_substring}

    def __set_search_substring(self) -> None:
        """
        Запрос у пользователя подстроки для поиска в тексте вакансии
        """
        search_substring = input('Введите строку для поиска (пустую строку, если искать не надо):').lower()
        if search_substring:
            self.__user_response = {'action': 'search vacancies by substring', 'substring': search_substring}

            # print('1. Искать введенную строку везде')
            # print('2. Указать поле поиска')
            # user_response = input('Ваш выбор: ')
            # if user_response.isdigit():
            #     user_response = int(user_response)
            #     if user_response == 2:
            #         if not HhRef.references.get('vacancy_search_fields'):
            #             HhRef('vacancy_search_fields', 'items')

    def __filter_vacancies(self) -> None:
        """
        Командуем отфильтровать найденные вакансии по параметрам поиска
        """
        self.__user_response = {'action': 'filter vacancies'}



    def show_message(self, message: str = '', pause: bool = True) -> None:
        if message:
            print(message)
        if pause:
            input('Нажмите Enter')

    def ask_vacancies_list_not_empty_when_loading_from_file(self):
        print('Что сделать с текущим набором вакансий?')
        print('1. Оставить, загруженные из файла вакансии добавить к текущим')
        print('2. Очистить, загруженные из файла вакансии полностью заменяют текущие.')
        self.__user_response = {"clear vacancies list": input('Ваш выбор: ')=='2'}

    def ask_vacancies_list_not_empty_when_searching_anew(self):
        print('Очистить текущий список вакансий?')
        print('1. Да, очистить результаты поиска.')
        print('2. Нет, объединить новые результаты поиска с уже существующими.')
        self.__user_response = {"очистить список вакансий": input('Ваш выбор: ')=='2'}
        print('Ищем...')


    """
    self.area: int = 113  # whole Russia
    self.page_items_count: int = 100
    self.page: int = 0
    self.search_field: str = ''
    self.experience: str = ''
    self.text: str = ''
    self.employment: str = ''
    self.__area_name = ''
    self.salary: int = 0
    self.salary_max: int = 0
    self.search_limit = 0
    """


    def respond(self, user_choice: str):
        """
        Реакция приложения (пользовательского интерфейса) на действие пользователя (выбор пункта текущего меню)
        :param user_choice:
        :return:
        """
        if user_choice and user_choice.isdigit():
            try:
                user_choice = int(user_choice) - 1
                self.__current_menu.select_menu_item(user_choice)
            except IndexError:
                print('Такого пункта в меню нет.')

    def update_menu_handlers(self) -> None:
        """
        Установка обработчиков пункто меню
        """
        for caption, handler in self.__menu_handlers.items():
            for menu in self.__menus.values():
                menu.set_menu_item_handler((caption, handler))

    def __change_search_params(self) -> None:
        # self.__previous_menus.insert(0, self.__current_menu)
        self.set_current_menu('change_search_params')

    def __ask_vacancies_details(self):
        self.__user_response = {'action': 'show vacancies details'}
        print('1. Показать подробно все вакансии.')
        print('2. Показать подробно только выбранные вакансии.')
        user_response = input('Ваш выбор: ')
        if user_response != '1':
            print('Введите номера вакансий из списка найденных, которые вы хотите просмотреть.')
            print('Номера можно указывать через запятую, или тире для указания диапазона')
            print('Диапазоны также можно указывать через запятую')
            print('Введите пустую строку для отмены просмотра')
            indices_str = input('Ваш выбор: ')
            if indices_str:
                self.__user_response['indices'] = indices_str
            else:
                self.clear_user_response()
                return

    def __set_area(self) -> None:
        self.set_current_menu('select_area')

    def __set_min_salary(self) -> None:
        """
        Указываем минимальную зарплату в параметрах поиска
        """
        while True:
            new_slary = input('Введите нижний порог зарплаты в рублях (0, если порога нет): ')
            if new_slary.isdigit():
                self.__user_response = {'action': 'set min salary', 'salary': int(new_slary)}
                # self.search_params.set_property('salary', value=int(new_slary))
                break
            else:
                print('Введите целое число')

    def __save_vacancies_to_file(self) -> None:
        """
        Сохраняем найденные вакансии в файл
        показать текущую папку файлов
        запросить имя файла / имя папки файлов
        определить тип файла
        по типу файла определить файловый менеджер
        послать ему информацию о файле
        записать в него вакансии
        отобразить информацию о готовности работать дальше
        """
        par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
        par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
        data_dir = os.path.join(par_dir, "data")
        print(f'Файл будет сохранен в каталоге {data_dir}')
        filename = input('Введите имя файла с расширением (введите пустую строку для отмены): ')
        if not filename:
            return
        filetype_choice = None

        if filename.lower().endswith('.txt'):
            filetype_choice = '1'
        elif filename.lower().endswith('.csv'):
            filetype_choice = '2'
        elif filename.lower().endswith('.json'):
            filetype_choice = '3'

        if not filetype_choice:
            print('Желаемый формат для сохранения файла не определен.')
            print('Желаемый формат для сохранения файла не определен.')

        self.__user_response = {'action': 'load vacancies from file',
                                'dir': data_dir,
                                'filename': filename,
                                'filetype': filetype_choice,
                                'additional request': "check if vacancies list is not empty"}


    def delete_vacancies(self) -> None:
        print('Введите номера вакансий, которые вы хотите удалить из списка.')
        print('Номера можно указывать через запятую, или тире для указания диапазона')
        print('Диапазоны также можно указывать через запятую')
        print('Введите пустую строку для отмены удаления')
        indices_str = input('Ваш выбор: ')
        if not indices_str:
            return

        indices = sorted(get_indices(indices_str, len(self.vacancies)), reverse=True)
        for i in indices:
            del self.vacancies[i]

    def extend_main_menu(self):
        self.__menus['main_menu'].add_item('Просмотреть найденные вакансии', 2, self.ask_for_brief_vacancies_list)
        self.__menus['main_menu'].add_item('Показать вакансии детально', 3, self.__ask_vacancies_details)
        self.__menus['main_menu'].add_item('Отфильтровать найденные вакансии', 4, self.__filter_vacancies)
        self.__menus['main_menu'].add_item('Отсортировать найденные вакансии', 5)
        self.__menus['main_menu'].add_item('Удалить вакансии из результатов поиска', 6)
        self.__menus['main_menu'].add_item('Сохранить найденные вакансии в файл', 7, self.__save_vacancies_to_file)
        self.__menus['main_menu'].add_item('Топ N вакансий по зарплате', 8)
        self.update_menu_handlers()


    def shrink_main_menu(self) -> None:
        """
        Убираем пункты главного меню, когда список вакансий пуст, с ним действий нет
        """
        self.__menus['main_menu'].delete_item('Просмотреть найденные вакансии')
        self.__menus['main_menu'].delete_item('Отфильтровать найденные вакансии')
        self.__menus['main_menu'].delete_item('Отсортировать найденные вакансии')
        self.__menus['main_menu'].delete_item('Сохранить найденные вакансии в файл')
        self.__menus['main_menu'].delete_item('Топ N вакансий по зарплате')
        self.__menus['main_menu'].delete_item('Удалить вакансии из результатов поиска')


    def user_response(self):
        return self.__user_response

    def ask_for_brief_vacancies_list(self):
        self.__user_response = {'action': 'show vacancies list'}

    def clear_user_response(self):
        self.__user_response = {}
    """


    def show_top(self) -> None:
        user_response = input('Введите число вакансий в топе: ')
        while True:
            if user_response.isdigit():
                user_response = int(user_response)
                break
            print('Введите целое число')
        # top = sorted(self.vacancies, key=lambda x: x.properties['salary']['value'], reverse=True)[:user_response]
        top = sorted(self.vacancies, key=lambda x: x, reverse=True)[:user_response]
        for ind, vac in enumerate(top):
            print(f"{ind + 1}. {vac}")
        print('\n')
        input('Нажмите Enter')


    def show_details(self) -> None:
        print('1. Показать подробно все вакансии.')
        print('2. Показать подробно только выбранные вакансии.')
        user_response = input('Ваш выбор: ')
        if user_response == '1':
            indices = range(len(self.vacancies))
        else:
            print('Введите номера вакансий из списка найденных, которые вы хотите просмотреть.')
            print('Номера можно указывать через запятую, или тире для указания диапазона')
            print('Диапазоны также можно указывать через запятую')
            print('Введите пустую строку для отмены удаления')
            indices_str = input('Ваш выбор: ')
            if not indices_str:
                return

            indices = get_indices(indices_str, len(self.vacancies))

        for ind in indices:
            print(self.vacancies[ind].details())
        input('Нажмите Enter')

    def sort_vacancies_list(self) -> None:
        print('Еще в разработке')
        input('Нажмите Enter')

    def save_vacancies_to_file(self) -> None:
        while True:
            print('Выберите формат файла: ')
            print('1. TXT')
            print('2. CSV')
            print('3. JSON')
            print('4. XLSX')
            filetype_choice = input('Ваш выбор: ')
            if filetype_choice.isdigit() and int(filetype_choice.isdigit()) in range(5):
                break
            print('Такого пункта меню нет')

        filename = input('Введите имя файла (введите пустую строку для отмены): ')
        if not filename:
            return

        par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
        par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
        data_dir = os.path.join(par_dir, "data")
        print(f'Файл будет сохранен в каталоге {data_dir}')
        # full_filename = os.path.join(data_dir, filename)
        file_manager = None

        content = ''
        if filetype_choice == '1':
            file_manager = TextFileManager(storage_name=filename, working_dir=data_dir)

            for vacancy in self.vacancies:
                content += vacancy.details()
                content += '-' * 100
                content += '\n'

        elif filetype_choice == '2':
            separator = ';'
            if not filename.lower().endswith('.csv'):
                filename += '.csv'

            content = separator.join(Vacancy.headers) + '\n'
            for vacancy in self.vacancies:
                content += vacancy.as_csv(separator)
                # content += '-' * 100
                content += '\n'

        elif filetype_choice == '3':

            file_manager = JSONFileManager(storage_name=filename, working_dir=data_dir, method=Vacancy.to_dict)
            content = {"items": self.vacancies}

        if file_manager and content:
            if os.path.exists(file_manager.full_filename()):
                print('Указанный файл существует. Что нужно сделать?')
                print('1. Дозаписать данные, сохранив уже записанные.')
                print('2. Перезаписать файл полностью.')
                print('3. Отменить сохранение.')
                write_mode_choice = input('Ваш выбор :')

                if write_mode_choice == '1':
                    append = True
                elif write_mode_choice == '2':
                    append = False
                else:
                    return
            else:
                append = False

            file_manager.save(content=content, append=append)

        #         try:
        #             f.write(content)
        #         except:                 # IOError
        #             print(f'Не удалось сохранить данные в файл {filename}')
        #         else:
        #             print(f'Файл {filename} успешно сохранен.')
        print('Сохранение завершено.')
        input('Нажмите Enter')



    def find_vacancies(self) -> None:
        # Ищем вакансии по текущим параметрам
        user_response = '1'
        if len(self.vacancies):
            print('Очистить текущий список вакансий?')
            print('1. Да, очистить результаты поиска.')
            print('2. Нет, объединить новые результаты поиска с уже существующими.')
            user_response = input('Ваш выбор :')

            if user_response == '1':
                self.shrink_main_menu()
                self.vacancies = []
                self.vacancies_by_id = {}

        print('Ищем...')
        vac_data = self.search_engine.fetch(self.search_params.params(),
                                            self.search_params.properties.get('search_limit',
                                                                              {}).get('value',
                                                                                      0))
        # resetting search results
        ignore_without_salary = self.search_params.properties['ignore_without_salary']['value']
        min_salary = self.search_params.properties.get('salary', {}).get('value', 0)
        if not min_salary:
            min_salary = 0

        for item in vac_data:
            vac = Vacancy(item)
            discard = ignore_without_salary and not vac.salary_specified()
            if not discard:
                # discard = vac.salary_specified() and vac.properties['salary']['value'] < min_salary
                discard = vac < min_salary

            if discard:
                del vac
            else:
                self.vacancies.append(vac)

            # self.vacancies_by_id[vac.id] = len(self.vacancies) - 1

        if len(self.vacancies) and (user_response == '1'):
            self.extend_main_menu()

        self.return_to_main_menu()

    # ('Просмотреть найденные вакансии', self.show_vacancies_list),
    # ('Отфильтровать найденные вакансии', self.find_vacancies),
    # ('Отсортировать найденные вакансии', self.find_vacancies),
    # ('Сохранить найденные вакансии в файл', self.find_vacancies),

    def set_search_limit(self) -> None:
        valid_input = False
        search_limit = 0
        while not valid_input:
            try:
                search_limit = int(input('Введите максимальное число искомых вакансий: '))
                valid_input = True
            except ValueError:
                print('Введите целое число')
        self.search_params.properties['search_limit']['value'] = search_limit
        # self.search_params.search_limit = search_limit
        if search_limit < 100:
            self.search_params.properties['per_page']['value'] = search_limit
        #     self.search_params.page_items_count = search_limit

    def set_area_code(self):
        valid_input = False
        while not valid_input:
            try:
                area_code = input('Введите код региона (113 - вся Россия): ')
                self.search_params.set_property(property_name='area', id=area_code)
                valid_input = True
                print(f"Выбранный регион: {self.search_params.properties['area']['value']}")
            except ValueError:
                print('Введен неверный код')
        input('Нажмите Enter')
        self.return_to_previous_menu()

    def search_area_by_substring(self):
        substring = input('Введите часть наименования региона: ').lower()
        if not HhRef.references.get('areas'):
            HhRef('areas', 'areas')
        areas = HhRef.references.get('areas').all_items_dict_by_name
        area_names = sorted(areas.keys(), key=lambda x: x)
        search_results = []
        for name in area_names:
            if str(name).lower().find(substring) > -1:
                search_results.append((name, areas[name]))
        for ind, area in enumerate(search_results):
            print(f"{ind + 1}. {area[0]} --- {area[1]['id']}")
        input('Нажмите Enter')
        # getch()

    def show_all_regions_sorted_by_name(self):
        if not HhRef.references.get('areas'):
            HhRef('areas', 'areas')
        areas = HhRef.references.get('areas').all_items_dict_by_name

        area_names = sorted(areas.keys(), key=lambda x: x)
        for ind, name in enumerate(area_names):
            print(f"{ind}. {name} --- {areas[name]['id']}")

        print('Нажмите любую клавишу')
        getch()

    def show_all_regions_sorted_by_code(self):
        if not HhRef.references.get('area'):
            HhRef('area', 'areas')
        areas = [area for area in HhRef.references['area']]
        areas = sorted(areas, key=lambda x: x)
        print(areas)

    def show_regions_structured(self):
        if not HhRef.references['area']:
            HhRef('area', 'areas')
        areas = [area for area in HhRef.references['area']]
        areas = sorted(areas, key=lambda x: x)
        print(areas)

    def set_search_area(self) -> None:
        self.previous_menu = self.current_menu
        self.current_menu = self.menus['select_area']

        #
        # valid_input = False
        # user_response = 4
        # while not valid_input:
        #     try:
        #         user_response = int(input('Ваш выбор: '))
        #         valid_input = user_response in range(1, 5)
        #         if not valid_input:
        #             print('Введите 1, 2, 3 или 4')
        #             continue
        #
        #     except ValueError:
        #         print('Введите 1, 2, 3 или 4')
        #
        # if user_response == 1:
        #     valid_input = False
        #     while not valid_input:
        #         try:
        #             self.search_params.set_property(property_name='area',
        #                                             id=input('Введите код региона (113 - вся Россия): '))
        #             valid_input = True
        #         except ValueError:
        #             print('Введен неверный код')
        # if user_response == 2:
        #     if not HhRef.references['area']:
        #         HhRef('area', 'areas')
        #     print('Как выводить список регионов?')
        #     print('1. Вывести все регионы, сортировать в алфавитном порядке')
        #     print('2. Вывести все регионы, сортировать по коду')
        #     print('3. Выводить по иерхии, начиная со стран')
        #     print('4. Вернуться в прежнее меню')
        #     print('5. Отменить выбор региона')
        #     print('Выберите регион: ')
        #
        #     for area_id in HhRef.references['area'].keys():
        #         print(f"{area_id} --- {HhRef.references['area'].all_items_dict_by_id[area_id]['name']}")
        # elif user_response == 4:
        #     return

    def return_to_main_menu(self):
        self.current_menu = self.menus['main_menu']

    def return_to_previous_menu(self):
        if self.previous_menu:
            self.current_menu = self.previous_menu
        else:
            self.current_menu = self.menus['main_menu']

    def show_vacancies_list(self):
        # vac_lines = [f"{i + 1}. {vacancy}" for i, vacancy in enumerate(self.vacancies)]
        for i, vacancy in enumerate(self.vacancies):
            print(f"{i + 1}. {vacancy}")

        print('\n')
        input('Нажмите Enter')

    def set_search_substring(self) -> None:
        search_substring = input('Введите строку для поиска (пустую строку, если искать не надо):')
        self.search_params.set_property('text', value=search_substring)
        # if search_substring:
        #     print('1. Искать введенную строку везде')
        #     print('2. Указать поле поиска')
        #     user_response = input('Ваш выбор: ')
        #     if user_response.isdigit():
        #         user_response = int(user_response)
        #         if user_response == 2:
        #             if not HhRef.references.get('vacancy_search_fields'):
        #                 HhRef('vacancy_search_fields', 'items')

    def set_igore_without_salary(self):
        print('1. Игнорировать вакансии без зарплаты')
        print('2. Показывать вакансии без зарплаты')
        user_response = input('Ваш выбор: ')
        self.search_params.set_property('ignore_without_salary', value=(user_response == '1'))

    def set_min_salary(self):
        while True:
            new_slary = input('Введите нижний порог зарплаты в рублях (0, если порога нет): ')
            if new_slary.isdigit():
                self.search_params.set_property('salary', value=int(new_slary))
                break
            else:
                print('Введите целое число')

    def load_vacancies_from_file(self):
        filename = input('Введите имя файла (введите пустую строку для отмены): ')
        if not filename:
            return
        filetype_choice = '1'

        if filename.lower().endswith('.txt'):
            filetype_choice = '1'
        elif filename.lower().endswith('.csv'):
            filetype_choice = '2'
        elif filename.lower().endswith('.json'):
            filetype_choice = '3'

        par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
        par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
        data_dir = os.path.join(par_dir, "data")
        print(f'Файл будет загружен из каталога {data_dir}')

        file_manager = None

        content = ''
        if filetype_choice == '1':
            file_manager = TextFileManager(storage_name=filename, working_dir=data_dir)

            # for vacancy in self.vacancies:
            #     content += vacancy.details()
            #     content += '-' * 100
            #     content += '\n'

        elif filetype_choice == '2':
            separator = ';'
            # if not filename.lower().endswith('.csv'):
            #     filename += '.csv'
            #
            # content = separator.join(Vacancy.headers)+'\n'
            # for vacancy in self.vacancies:
            #     content += vacancy.as_csv(separator)
            #     # content += '-' * 100
            #     content += '\n'

        elif filetype_choice == '3':

            file_manager = JSONFileManager(storage_name=filename, working_dir=data_dir, method=Vacancy.to_dict)
            try:
                new_vacancies = file_manager.load()
            except FileNotFoundError:
                print('Указанный файл не найден')
                return
            if new_vacancies:
                if len(self.vacancies):
                    print('Что сделать с текущим набором вакансий?')
                    print('1. Оставить, загруженные из файла вакансии добавить к текущим')
                    print('2. Очистить, загруженные из файла вакансии полностью заменяют текущие.')
                    user_response = input('Ваш выбор: ')

                    if user_response == '1':
                        self.vacancies.append(new_vacancies)
                    else:
                        self.shrink_main_menu()
                        self.vacancies = new_vacancies
                else:
                    self.vacancies = new_vacancies

        if len(self.vacancies):
            self.extend_main_menu()

        print('Загрузка завершена.')
        input('Нажмите Enter')

          self.area: int = 113  # whole Russia
          self.page_items_count: int = 100
          self.page: int = 0
          self.search_field: str = ''
          self.experience: str = ''
          self.text: str = ''
          self.employment: str = ''
          self.__area_name = ''
          self.salary: int = 0
          self.salary_max: int = 0
          self.search_limit = 0

        self.current_menu = self.menus['main_menu']

    # def insert_menu_item(self, menu_name: str, item_name: str, pos: int, function: callable):
    #     if self.menus.get(menu_name):
    #         self.menus[menu_name].add_item(item_name, pos, function)

    def run(self) -> None:
        self.search_params.set_property(property_name='area', id='113')
        # self.search_params.area = 11
        # from src.professions_reference_class import ProfessionsReference
        # ProfessionsReference.init()

        while not UserInterface.work_is_over:
            self.show_current_menu()
            while True:
                user_response = input('Ваш выбор: ')
                try:
                    user_response = int(user_response) - 1
                    self.current_menu.items[user_response][1]()
                    break
                except IndexError:
                    print('Такого пункта в меню нет.')

    # def sort_vacancies(self):
    #     for sort_param in self.sort_parameters:
    #         pass
    
"""


