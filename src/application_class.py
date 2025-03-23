# from src.dictionary_class import Dictionary
import os
from msvcrt import getch
import json

from typing_extensions import Self

from src.display_options_class import DisplayOptions
from src.menu_class import Menu
from src.search_engine_class import VacanciesSearchEngine
from src.search_parameters_class import SearchParameters
from src.sort_parameters_class import SortParameter
from src.text_file_manager_class import TextFileManager
from src.user_interface_class import UserInterface
from src.vacancy_class import Vacancy
from src.hh_reference_class import HeadHunterReference as HhRef
from src.misc_tools import get_indices
from src.json_file_manager import JSONFileManager


class Application:
    work_is_over: bool = False

    @classmethod
    def terminate(cls) -> None:
        cls.work_is_over = True

    def __init__(self):

        self.search_params = SearchParameters()
        self.search_engine = VacanciesSearchEngine()
        self.vacancies = []
        self.vacancies_by_id = {}

        self.sort_parameters = [SortParameter(SortParameter.SALARY_MIN)]

        # self.menus: dict = {}
        # self.current_menu: Menu | None = None
        # self.previous_menu: Menu | None = None
        self.display_options = DisplayOptions()

        """
        self.menus = {'main_menu': Menu('Добро пожаловать в приложение для поиска вакансий с сайта HeadHunter.ru',
                                        [('Изменить параметры поиска', self.change_search_params),
                                         ('Найти вакансии', self.find_vacancies),
                                         # ('Просмотреть найденные вакансии', self.show_vacancies_list),
                                         # ('Отфильтровать найденные вакансии', self.find_vacancies),
                                         # ('Отсортировать найденные вакансии', self.find_vacancies),
                                         # ('Сохранить найденные вакансии в файл', self.find_vacancies),
                                         ('Загрузить вакансии из файла', self.load_vacancies_from_file),
                                         ('Выйти из программы.', Application.terminate),
                                         ]
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

        menu_handlers = {
            'Выйти из программы.': Application.terminate,
            'vacancies_count': self.vacancies_count,
            # 'Найти вакансии': self.find_vacancies,

            # 'Загрузить вакансии из файла': self.load_vacancies_from_file,
            # 'Просмотреть найденные вакансии': self.show_vacancies_list,
            # 'Показать вакансии детально': self.show_details,
            # 'Отфильтровать найденные вакансии': self.filter_found_vacancies,
            # 'Отсортировать найденные вакансии': self.sort_vacancies_list,
            # 'Удалить вакансии из результатов поиска': self.delete_vacancies,
            # 'Сохранить найденные вакансии в файл': self.save_vacancies_to_file,
            # 'Топ N вакансий по зарплате': self.show_top,
        }

        self.user_interface = UserInterface(menu_handlers)

    def vacancies_count(self) -> str:
        return f'Сейчас найдено {len(self.vacancies)} вакансий'

    def filter_found_vacancies(self) -> None:
        key_words = str(self.search_params.properties.get('text', {}).get('value')).lower()
        if len(key_words):  # ищем по ключевым словам
            key_words = key_words.split(',')
        vacancies_to_delete = []
        min_salary = self.search_params.properties.get('salary', {}).get('value', 0)
        for vac_ind, vacancy in enumerate(self.vacancies):
            # ищем по ключевым словам
            analyze_on = True
            if key_words:
                vacancy_info = str(vacancy).lower()
                found = False
                for key_word in key_words:
                    found = vacancy_info.find(key_word) > -1
                    if found:
                        break
                else:
                    vacancies_to_delete.append(vac_ind)
                    analyze_on = False
            if analyze_on and min_salary and (min_salary > 0):
                # salary = vacancy.properties.get('salary', {}).get('value', 0)
                # if not isinstance(salary, int):
                #     salary = 0
                # if salary < min_salary:
                if vacancy < min_salary:
                    vacancies_to_delete.append(vac_ind)
                    analyze_on = False

        vacancies_to_delete.sort(reverse=True)

        for ind in vacancies_to_delete:
            del self.vacancies[ind]

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

    def show_details(self, indices_str: str) -> None:
        """
        Готовим информацию для детального представления вакансий
        :param indices_str: строка, содержащая номера нужных вакансий
        """
        if not indices_str:
            indices = range(len(self.vacancies))  # показываем все
        else:
            indices = get_indices(indices_str, len(self.vacancies))  # выбранные

        details = [self.vacancies[ind].details() for ind in indices]
        self.user_interface.show_current_menu(info_pane=details)

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

    def find_vacancies(self, clear_previous_results: bool) -> None:
        """
        Ищем вакансии по текущим параметрам
        """

        if clear_previous_results:
            self.user_interface.shrink_main_menu()
            self.vacancies = []
            self.vacancies_by_id = {}

        vac_data = self.search_engine.fetch(self.search_params.params(),
                                            self.search_params.properties.get('search_limit', {}).get('value', 0))
        # resetting search results
        ignore_without_salary = self.search_params.properties['ignore_without_salary']['value']
        min_salary = self.search_params.properties.get('salary', {}).get('value', 0)
        if not min_salary:
            min_salary = 0

        search_limit = self.search_params.properties['search_limit'].get('value')
        # if search_limit:
        #     if search_limit < 100:
        #         self.search_params.properties['per_page']['value'] = search_limit

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
                if search_limit and len(self.vacancies) == search_limit:
                    break

        if len(self.vacancies):
            self.user_interface.extend_main_menu()
            self.user_interface.return_to_main_menu()

    def search_area_by_substring(self, substring: str) -> None:
        """
        Ищем регион по подстроке и посылаем на вывод список подходящих названий
        :param substring: подстрока в названии региона
        """
        if not HhRef.references.get('areas'):
            HhRef('areas', 'areas')
        areas = HhRef.references.get('areas').all_items_dict_by_name
        area_names = sorted(areas.keys(), key=lambda x: x)
        search_results = []
        for name in area_names:
            if str(name).lower().find(substring) > -1:
                search_results.append((name, areas[name]))
        # areas = [f"{ind + 1}. {area[0]} --- {area[1]['id']}" for ind, area in enumerate(search_results)]
        areas = [f"{area[0]} --- {area[1]['id']}" for area in search_results]
        self.user_interface.show_current_menu(info_pane=areas)

    def show_all_regions_sorted_by_name(self) -> None:
        if not HhRef.references.get('areas'):
            HhRef('areas', 'areas')
        areas = HhRef.references.get('areas').all_items_dict_by_name
        areas = [f"{name} --- {areas[name]['id']}" for name in areas.keys()]
        area_names = sorted(areas, key=lambda x: x)
        self.user_interface.show_current_menu(info_pane=area_names)

    def show_all_regions_sorted_by_code(self) -> None:
        if not HhRef.references.get('area'):
            HhRef('area', 'areas')
        areas = HhRef.references.get('areas').all_items_dict_by_id
        areas = [f"{id} --- {areas[id]['name']}" for id in areas.keys()]
        area_names = sorted(areas, key=lambda x: int(x.split(' ')[0]))
        self.user_interface.show_current_menu(info_pane=area_names, enumerate_list=False)

    def show_regions_structured(self) -> None:
        if not HhRef.references['area']:
            HhRef('area', 'areas')
        areas = [area for area in HhRef.references['area']]
        areas = sorted(areas, key=lambda x: x)
        print(areas)

    #     # if user_response == 2:
    #     #     if not HhRef.references['area']:
    #     #         HhRef('area', 'areas')
    #     #     print('Как выводить список регионов?')
    #     #     print('1. Вывести все регионы, сортировать в алфавитном порядке')
    #     #     print('2. Вывести все регионы, сортировать по коду')
    #     #     print('3. Выводить по иерхии, начиная со стран')
    #     #     print('4. Вернуться в прежнее меню')
    #     #     print('5. Отменить выбор региона')
    #     #     print('Выберите регион: ')
    #     #
    #     #     for area_id in HhRef.references['area'].keys():
    #     #         print(f"{area_id} --- {HhRef.references['area'].all_items_dict_by_id[area_id]['name']}")
    #     # elif user_response == 4:
    #     #     return
    #

    def set_igore_without_salary(self):
        print('1. Игнорировать вакансии без зарплаты')
        print('2. Показывать вакансии без зарплаты')
        user_response = input('Ваш выбор: ')
        self.search_params.set_property('ignore_without_salary', value=(user_response == '1'))

    # def set_min_salary(self):
    #     while True:
    #         new_slary = input('Введите нижний порог зарплаты в рублях (0, если порога нет): ')
    #         if new_slary.isdigit():
    #             self.search_params.set_property('salary', value=int(new_slary))
    #             break
    #         else:
    #             print('Введите целое число')

    def load_vacancies_from_file(self, data_dir, filename, filetype):

        file_manager = None
        content = ''
        new_vacancies = []
        if filetype == '1':
            file_manager = TextFileManager(storage_name=filename, working_dir=data_dir)

            # for vacancy in self.vacancies:
            #     content += vacancy.details()
            #     content += '-' * 100
            #     content += '\n'

        elif filetype == '2':
            separator = ';'
            # if not filename.lower().endswith('.csv'):
            #     filename += '.csv'
            #
            # content = separator.join(Vacancy.headers)+'\n'
            # for vacancy in self.vacancies:
            #     content += vacancy.as_csv(separator)
            #     # content += '-' * 100
            #     content += '\n'

        elif filetype == '3':
            file_manager = JSONFileManager(storage_name=filename, working_dir=data_dir, method=Vacancy.to_dict)
            try:
                new_vacancies = file_manager.load()
            except FileNotFoundError:
                self.user_interface.show_message('Указанный файл не найден')
                return

        if new_vacancies:
            if len(self.vacancies):
                self.user_interface.ask_vacancies_list_not_empty_when_loading_from_file()

                if self.user_interface.user_response().get('очистить список вакансий', False):
                    self.vacancies = new_vacancies
                else:
                    self.vacancies.extend(new_vacancies)
            else:
                self.vacancies = new_vacancies

        if len(self.vacancies):
            self.user_interface.extend_main_menu()

        self.user_interface.show_message('Загрузка завершена.')

        # def init_menus(self) -> None:
        #     self.menus = {'main_menu': Menu('Добро пожаловать в приложение для поиска вакансий с сайта HeadHunter.ru',
        #                                     [('Изменить параметры поиска', self.change_search_params),
        #                                      ('Найти вакансии', self.find_vacancies),
        #                                      # ('Просмотреть найденные вакансии', self.show_vacancies_list),
        #                                      # ('Отфильтровать найденные вакансии', self.find_vacancies),
        #                                      # ('Отсортировать найденные вакансии', self.find_vacancies),
        #                                      # ('Сохранить найденные вакансии в файл', self.find_vacancies),
        #                                      ('Загрузить вакансии из файла', self.load_vacancies_from_file),
        #                                      ('Выйти из программы.', Application.terminate),
        #                                      ]
        #                                     ),
        #                   'change_search_params': Menu('Укажите параметры поиска:',
        #                                                [('Указать регион', self.set_search_area),
        #                                                 ('Указать минимальную зарплату', self.set_min_salary),
        #                                                 ('Указать подстроку для поиска', self.set_search_substring),
        #                                                 # ('Указать максимальную зарплату', Application.terminate),
        #                                                 ('Указать максимальное число вакансий', self.set_search_limit),
        #                                                 ('Указать отрасль', Application.terminate),
        #                                                 ('Указать профессию', Application.terminate),
        #                                                 ('Уточнить поиск вакансий без зарплаты',
        #                                                  self.set_igore_without_salary),
        #                                                 # ('Указать поле для поиска подстроки', Application.terminate),
        #                                                 ('Установить параметры поика по умолчанию', Application.terminate),
        #                                                 ('Вернуться в главное меню', self.return_to_main_menu),
        #                                                 ('Искать вакансии', self.find_vacancies)
        #                                                 ]
        #                                                ),
        #                   'select_area': Menu('Как вы хотите указать регион?',
        #                                       [('Ввести код региона', self.set_area_code),
        #                                        ('Подобрать регион по подстроке', self.search_area_by_substring),
        #                                        ('Показать все регионы, сортировать в алфавитном порядке',
        #                                         self.show_all_regions_sorted_by_name),
        #                                        ('Показать все регионы, сортировать по коду',
        #                                         self.show_all_regions_sorted_by_code),
        #                                        ('Выводить региоры по иерхии, начиная со стран',
        #                                         self.show_regions_structured),
        #                                        ('Вернуться в прежнее меню', self.return_to_previous_menu),
        #                                        ('Отменить выбор региона', self.change_search_params),
        #                                        ('Вернуться в главное меню', self.return_to_main_menu),
        #                                        ('Вернуться в предыдущее меню', self.return_to_previous_menu),
        #                                        ('Выйти из программы', Application.terminate)
        #                                        ])
        #
        #                   # print('3. Подобрать регион по подстроке\n')
        #                   }
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

    def check_out_user_response(self):
        user_response = self.user_interface.user_response()
        if user_response:
            action = user_response.get('action')
            # additional_request = user_response.get('additional request')
            if action == 'load vacancies from file':
                data_dir = user_response.get('dir')
                filename = user_response.get('filename')
                filetype = user_response.get('filetype')
                all_data_set = dir and filename and filetype
                if all_data_set:
                    self.load_vacancies_from_file(data_dir, filename, filetype)
                else:
                    self.user_interface.show_message('Введенных данных не достаточно для продолжения этой операции')
                    self.user_interface.return_to_main_menu()
            elif action == 'show vacancies list':
                self.user_interface.show_current_menu(info_pane=self.vacancies)
            elif action == 'show vacancies details':
                indices_str = user_response.get('indices')
                self.show_details(indices_str)
            elif action == 'set area id':
                area_id = user_response.get('id', '')
                try:
                    self.search_params.set_property(property_name='area', id=area_id)
                except ValueError:
                    self.user_interface.show_message('Введен неверный код')
                else:
                    self.user_interface.return_to_previous_menu()
            elif action == 'find vacancies':
                if len(self.vacancies):
                    self.user_interface.ask_vacancies_list_not_empty_when_searching_anew()
                self.user_interface.show_message('Ищем...', pause=False)
                self.find_vacancies(user_response.get('clear vacancies list', True))
            elif action == 'search area by substring':
                substring = user_response.get('substring')
                if substring:
                    self.search_area_by_substring(substring)
            elif action == 'search area by substring':
                substring = user_response.get('search vacancies by substring')
                if substring:
                    self.search_area_by_substring(substring)
            elif action == 'search vacancies by substring':
                search_substring = user_response.get('substring')
                if search_substring:
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
            elif action == 'filter vacancies':
                self.filter_found_vacancies()
            elif action == 'set min salary':
                min_salary = user_response.get('salary')
                if min_salary:
                    self.search_params.set_property('salary', value=min_salary)
            elif action == 'show all regions sorted by name':
                self.show_all_regions_sorted_by_name()
            elif action == 'show all regions sorted by code':
                self.show_all_regions_sorted_by_code()
            elif action == 'set vacancies list limit':
                limit = user_response.get('limit')
                if limit:
                    self.search_params.set_property('search_limit', value=limit)
            elif action == 'delete vacancies':
                indices_str = user_response.get('indices')
                indices = sorted(get_indices(indices_str, len(self.vacancies)), reverse=True)
                for i in indices:
                    del self.vacancies[i]

        self.user_interface.clear_user_response()

    def run(self) -> None:
        self.search_params.set_property(property_name='area', id='113')
        # self.search_params.area = 11
        # from src.professions_reference_class import ProfessionsReference
        # ProfessionsReference.init()

        while not Application.work_is_over:
            self.user_interface.show_current_menu(str(self.search_params))
            self.user_interface.respond(input('Ваш выбор: '))
            self.check_out_user_response()

    # def sort_vacancies(self):
    #     for sort_param in self.sort_parameters:
    #         pass
