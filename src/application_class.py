import json
import os.path

from src.db_manager_class import DBManager
from src.hh_reference_class import HeadHunterReference as HhRef
from src.json_file_manager import JSONFileManager
from src.misc_tools import get_indices, vacancy_complies
from src.search_engine_class import VacanciesSearchEngine
from src.search_parameters_class import SearchParameters
from src.text_file_manager_class import TextFileManager
from src.user_interface_class import UserInterface
from src.vacancy_class import Vacancy

from copy import deepcopy


class Application:
    """
    Центральный класс приложения, хранящий данные для работы, инструменты для их обработки
    и средства для взаимодействия с пользователем
    """

    work_is_over: bool = False  # флаг завершения работы приложения

    @classmethod
    def terminate(cls) -> None:
        """
        Завершение работы приложения
        """
        cls.work_is_over = True

    def __init__(self):  # type: ignore

        self.search_params = SearchParameters()
        self.search_engine = VacanciesSearchEngine()
        self.vacancies = []
        self.db_manager = DBManager()

        # self.vacancies_by_id = {}

        """
                                                    ('Указать отрасль', Application.terminate),
                                                    ('Указать профессию', Application.terminate),
                                                    # ('Указать поле для поиска подстроки', Application.terminate),
                                                    ('Установить параметры поика по умолчанию', Application.terminate),
        """

        menu_handlers = {
            "Выйти из программы.": Application.terminate,
            "vacancies_count": self.vacancies_count,
            "db_status": self.db_connection_status,
        }

        self.user_interface = UserInterface(menu_handlers)

    def vacancies_count(self) -> str:
        """
        количество вакансий для строки статуса
        """
        return f"Сейчас найдено {len(self.vacancies)} вакансий"

    def db_connection_status(self) -> str:
        """
        статусная строка для работы с базами данных
        """
        return str(self.db_manager.connection_status())

    def db_connection_settings(self) -> str:
        """
        статусная строка для работы с базами данных
        """
        result = str(self.db_manager)
        if result == "":
            result = "Подключение к серверу баз данных не настроено\n"
        return result

    def filter_found_vacancies(self) -> None:
        """
        фильтрация найденных вакансий с использованием измененных параметров поиска
        :return:
        """
        key_words = str(
            self.search_params.properties.get("text", {}).get("value")
        ).lower()
        if len(key_words):  # ищем по ключевым словам
            key_words = key_words.split(",")  # type: ignore[assignment]
        vacancies_to_delete = []
        min_salary = self.search_params.properties.get("salary", {}).get("value", 0)
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

    def show_details(self, indices_str: str = "") -> None:
        """
        Готовим информацию для детального представления вакансий
        :param indices_str: строка, содержащая номера нужных вакансий
        """
        if not indices_str:
            indices = range(len(self.vacancies))  # показываем все
        else:
            indices = get_indices(indices_str, len(self.vacancies))  # выбранные        # type: ignore[assignment]

        details = [self.vacancies[ind].details() for ind in indices]
        self.user_interface.show_current_menu(
            info_pane=details, show_info_pane_once=True
        )

    def connect_to_db(self) -> None:
        self.db_manager.connect()
        if self.db_manager.error_message:
            self.user_interface.show_message(self.db_manager.error_message)
        else:
            self.user_interface.extend_db_menu(
                vacancies_present=(len(self.vacancies) > 0)
            )
            self.user_interface.show_current_menu(info_pane=str(self.db_manager))

    def load_db_connection_settings_from_file(self, filename: str, dir: str) -> None:
        fullname = os.path.join(dir, filename)
        if os.path.exists(fullname):
            with open(fullname, "r", encoding="utf-8") as f:
                self.db_manager.connection_settings = json.load(f)
        else:
            self.user_interface.show_message(
                f"Файл {fullname} не найден. Подлкючение не установлено."
            )

    def load_employers_data(self) -> None:
        """
        Загружаем данные о работодателях с сайта в справочник в сохраняем в базу данных
        """
        if not HhRef.references.get("employers"):
            prompt = "Загружать работодателей без вакансий?\n1. Да\n2. Нет"
            add_without_vacancies = self.user_interface.input_request(prompt) == "1"
            HhRef.add_reference(
                "employers", allow_without_vacancies=add_without_vacancies
            )
        if not HhRef.references.get("employers"):
            self.user_interface.show_message(
                "Данные о работодателях не удалось загрузить с сайта"
            )
        else:
            employers_data = HhRef.references.get("employers").items_by_id.items()      # type: ignore[union-attr]
            data = []
            for employer_id, employer_data in employers_data:
                employer_data.update({"id": employer_id})
                data.append(employer_data)

            if self.db_manager.connected():
                self.db_manager.insert_employer_data(data)
                self.db_manager.show_employers()

        #         if not self.db_manager.connection_settings:
        #             self.user_interface.request_db_connection_settings()
        #         self.db_manager.connect()
        #         if self.db_manager.error_message:
        #             self.user_interface.show_message(self.db_manager.error_message)
        #             self.db_manager.show_employers()
        #             return
        #
        #     self.db_manager.insert_employer_data(data)
        # self.db_manager.show_employers()

    def save_vacancies_to_file(
            self,
            data_dir: str,
            filename: str,
            filetype: str,
            append: bool,
            encoding: str = "utf-8",
    ) -> None:
        """
        сохранение вакансий в файл
        :param data_dir:   каталог для сохранения
        :param filename:    имя файла
        :param filetype:    тип файла
        :param append:      перезапись / дозапись (True)
        :param encoding:    кодировка
        """
        file_manager = None
        content = ""
        if filetype == "1":
            file_manager = TextFileManager(storage_name=filename, working_dir=data_dir)

            for vacancy in self.vacancies:
                content += vacancy.details()
                content += "-" * 100
                content += "\n"

            file_manager.save(content, append, encoding=encoding)
        #
        # elif filetype == '2':
        #     separator = ';'
        #     if not filename.lower().endswith('.csv'):
        #         filename += '.csv'
        #
        #     content = separator.join(Vacancy.headers) + '\n'
        #     for vacancy in self.vacancies:
        #         content += vacancy.as_csv(separator)
        #         # content += '-' * 100
        #         content += '\n'
        #
        # elif filetype == '3':
        if filetype == "3":
            file_manager = JSONFileManager(  # type: ignore[assignment]
                storage_name=filename, working_dir=data_dir, method=Vacancy.to_dict
            )
            content = {"items": deepcopy(self.vacancies)}  # type: ignore[assignment]

        if file_manager and content:
            file_manager.save(content=content, append=append)

            #         try:
            #             f.write(content)
            #         except:                 # IOError
            #             print(f'Не удалось сохранить данные в файл {filename}')
            #         else:
            #             print(f'Файл {filename} успешно сохранен.')
            self.user_interface.show_message("Сохранение завершено.")

    def find_vacancies(self, clear_previous_results: bool) -> None:
        """
        Ищем вакансии по текущим параметрам
        :param clear_previous_results - если False - новые результаты добавляются к текущим, иначе старые стираются
        """
        if clear_previous_results:
            self.user_interface.shrink_main_menu()
            self.vacancies = []
            # self.vacancies_by_id = {}

        vac_data = self.search_engine.fetch(
            self.search_params.params(),
            self.search_params.properties.get("search_limit", {}).get("value", 0),
        )
        # resetting search results
        # ignore_without_salary = self.search_params.properties['ignore_without_salary']['value']
        min_salary = self.search_params.properties.get("salary", {}).get("value", 0)
        if not min_salary:
            min_salary = 0

        search_limit = self.search_params.properties["search_limit"].get("value")
        # if search_limit:
        #     if search_limit < 100:
        #         self.search_params.properties['per_page']['value'] = search_limit

        for item in vac_data:
            vac = Vacancy(item)
            discard = False
            if vac.salary_specified():
                discard = int(vac) < min_salary
            # else:
            #     discard = ignore_without_salary

            if discard:
                del vac
            else:
                self.vacancies.append(vac)
                if search_limit and len(self.vacancies) == search_limit:
                    break

        if len(self.vacancies):
            self.user_interface.extend_main_menu()
            self.user_interface.return_to_main_menu()
            if self.db_manager.connected():
                self.user_interface.extend_db_menu(vacancies_present=True)

    def search_area_by_substring(self, substring: str) -> None:
        """
        Ищем регион по подстроке и посылаем на вывод список подходящих названий
        :param substring: подстрока в названии региона
        """
        if not HhRef.references.get("areas"):
            HhRef.add_reference("areas")
        areas = HhRef.references.get("areas").items_by_name  # type: ignore[union-attr]
        area_names = sorted(areas.keys(), key=lambda x: x)
        search_results = []
        for name in area_names:
            if name is None:
                continue
            if str(name).lower().find(substring) > -1:
                # if str(name).find(substring) > -1:
                if areas.get(name):
                    search_results.append((name, areas.get(name)))
        # areas = [f"{ind + 1}. {area[0]} --- {area[1]['id']}" for ind, area in enumerate(search_results)]
        areas = [f"{area[0]} --- {area[1]['id']}" for area in search_results]
        self.user_interface.show_current_menu(info_pane=areas, show_info_pane_once=True)

    def show_subareas(self, parent: str) -> None:
        """
        Показать список регионов из состава указанной области
        :param parent: составная область
        """
        if not HhRef.references.get("areas"):
            HhRef.add_reference("areas")
        if not HhRef.references["areas"].item_code_is_valid(parent):
            self.user_interface.show_message(f"Регион с кодом {parent} не найден.")
            return
        child_area_ids = HhRef.references.get("areas").items_by_id[parent].get("areas")  # type: ignore[union-attr]
        if child_area_ids:
            areas = []

            for child_id in child_area_ids:
                child_area = HhRef.references.get("areas", {}).items_by_id.get(child_id)
                if child_area:
                    child_area_name = child_area.get("name")
                    if child_area_name:
                        areas.append(f"{child_area_name} --- {child_id}")
            area_names = sorted(areas, key=lambda x: x)
            self.user_interface.show_current_menu(
                info_pane=area_names, show_info_pane_once=False, pause=False
            )
        else:
            self.user_interface.show_message(
                f"Регион с кодом {parent} не содержит составных частей.", pause=True
            )

    def show_all_regions_sorted_by_name(self) -> None:
        """
        Показать список всех регионов, упорядоченных в алфавитном порядке
        """
        if not HhRef.references.get("areas"):
            HhRef.add_reference("areas")
        areas = HhRef.references.get("areas").items_by_name  # type: ignore[union-attr]
        areas = [f"{name} --- {areas[name]['id']}" for name in areas.keys()]
        area_names = sorted(areas, key=lambda x: x)
        self.user_interface.show_current_menu(
            info_pane=area_names, show_info_pane_once=True
        )

    def show_all_regions_sorted_by_code(self) -> None:
        """
        Показать список всех регионов, упорядоченных по коду
        """
        if not HhRef.references.get("areas"):
            HhRef.add_reference("areas")
        areas = HhRef.references.get("areas").items_by_id  # type: ignore[union-attr]
        areas = [f"{id} --- {areas[id]['name']}" for id in areas.keys()]
        area_names = sorted(areas, key=lambda x: int(x.split(" ")[0]))
        self.user_interface.show_current_menu(
            info_pane=area_names, enumerate_list=False, show_info_pane_once=True
        )

    def show_regions_structured(self) -> None:
        """
        Показать список регионов по иерархии, начиная со стран
        """
        if not HhRef.references["areas"]:
            HhRef.add_reference("areas")
        areas = HhRef.references["areas"]
        areas_list = []
        for area, area_data in areas.items_by_name.items():
            areas_list.append(f"{area} --- {area_data.get('id', '')}")
        self.user_interface.show_current_menu(
            info_pane=areas_list, pause=False, show_info_pane_once=False
        )
        # areas = sorted(areas, key=lambda x: x)

    # def show_all_professions_names(self) -> None:
    #     """
    #     Показать все отрасли / профессии
    #     """
    #     profs = HhRef.references.get("professional_roles")
    #     if not profs:
    #         HhRef("professional_roles", ["categories", "roles"])
    #     profs = HhRef.references.get("professional_roles")
    #     if profs:
    #         prof_names = [
    #             f"{name} --- {prof_data.get('id', '')}"
    #             for name, prof_data in profs.items_by_name.items()
    #         ]
    #         self.user_interface.show_current_menu(
    #             info_pane=prof_names, show_info_pane_once=True
    #         )

    def load_vacancies_from_file(
            self,
            data_dir: str,
            filename: str,
            filetype: str,
            conditions: str = "",
            fails_if_none: bool = True,
    ) -> None:
        """
        Загрузить вакансии из файла
        :param data_dir:    каталог загрузки
        :param filename:    имя файла
        :param filetype:    тип файла
        :param conditions:  условия для фильтрации данных вакансий в файле
        :param fails_if_none: если False и данные по условиям отсутствуют в вакансии, она считается подходящей условиям
        """
        file_manager = None
        # content = ""
        new_vacancies = []
        self.user_interface.shrink_main_menu()
        if filetype == "1":
            file_manager = TextFileManager(storage_name=filename, working_dir=data_dir)

            try:
                vacancies_data = file_manager.load(
                    conditions, fails_if_none, encoding="utf-8"
                )
                if vacancies_data:
                    vacancies_data = [
                        Vacancy.validate_fields(raw_item) for raw_item in vacancies_data
                    ]
                    if vacancies_data:
                        new_vacancies = [
                            Vacancy(item_data) for item_data in vacancies_data
                        ]
            except FileNotFoundError:
                self.user_interface.show_message("Указанный файл не найден")
                return
        elif filetype == "2":
            pass
            # separator = ";"
            # if not filename.lower().endswith('.csv'):
            #     filename += '.csv'
            #
            # content = separator.join(Vacancy.headers)+'\n'
            # for vacancy in self.vacancies:
            #     content += vacancy.as_csv(separator)
            #     # content += '-' * 100
            #     content += '\n'

        elif filetype == "3":
            file_manager = JSONFileManager(  # type: ignore[assignment]
                storage_name=filename, working_dir=data_dir, method=Vacancy.to_dict
            )
            file_manager.filter_method = vacancy_complies  # type: ignore[union-attr]
            try:
                new_vacancies = file_manager.load(conditions, fails_if_none)  # type: ignore[assignment, union-attr]
            except FileNotFoundError:
                self.user_interface.show_message("Указанный файл не найден")
                return

        if new_vacancies:
            if len(self.vacancies):
                self.user_interface.ask_vacancies_list_not_empty_when_loading_from_file()

                if self.user_interface.user_response().get(
                        "clear vacancies list", False
                ):
                    self.vacancies = new_vacancies
                else:
                    self.vacancies.extend(new_vacancies)
            else:
                self.vacancies = new_vacancies

        if len(self.vacancies):
            self.user_interface.extend_main_menu()

        self.user_interface.show_message("Загрузка завершена.")

    def save_vacancies_to_db(self) -> None:
        """
        Сохраняем вакансии и, если нужно, работодателей в базу данных
        """
        vac_data_list = []
        employers_data = []
        if not HhRef.references.get("employers"):
            HhRef.add_reference("employers")
        employers_ref = HhRef.references.get("employers")
        if not employers_ref:
            self.user_interface.show_message(
                "Не удалось получить данные о работотдателях с сайта"
            )
            return

        for vacancy in self.vacancies:
            vacancy_fields = vacancy.fields()

            emp_id = vacancy_fields.get("employer", {}).get("id")
            # набираем идентификаторы о работодателях, которые должны быть (записаны) в базе данных
            if emp_id:
                employer_data = employers_ref.get_by_id(emp_id)
                employer_data["id"] = emp_id
                employers_data.append(employer_data)
                vac_data_list.append(vacancy_fields)
        self.db_manager.insert_employer_data(
            employers_data, allow_without_vacancies=True
        )
        self.db_manager.insert_vacancies_data(vac_data_list)

    def check_out_user_response(self) -> None:
        """
        анализ пользовательского ввода - выполнение выбранных пользователем команд
        """
        user_response = self.user_interface.user_response()
        if user_response:
            action = user_response.get("action")
            # additional_request = user_response.get('additional request')
            # -----------------------------------------------------------------------------------------------------
            if action == "load vacancies from file":
                data_dir = user_response.get("dir")
                filename = user_response.get("filename")
                filetype = user_response.get("filetype")
                if user_response.get("filter"):
                    conditions = self.search_params.fields()
                else:
                    conditions = ""
                fails_if_none = user_response.get("fails if none", False)
                all_data_set = data_dir and filename and filetype
                if all_data_set:
                    self.load_vacancies_from_file(
                        data_dir, filename, filetype, conditions, fails_if_none
                    )
                # else:
                #     self.user_interface.show_message('Введенных данных не достаточно для продолжения этой операции')
                #     self.user_interface.return_to_main_menu()

            # -----------------------------------------------------------------------------------------------------
            elif action == "show vacancies list":
                self.user_interface.show_current_menu(
                    info_pane=self.vacancies, show_info_pane_once=True
                )
            # -----------------------------------------------------------------------------------------------------
            elif action == "show vacancies details":
                indices_str = user_response.get("indices")
                self.show_details(indices_str)
            # -----------------------------------------------------------------------------------------------------
            elif action == "set area id":
                area_id = user_response.get("id", "")
                try:
                    self.search_params.set_property(property_name="area", id=area_id)
                except ValueError:
                    self.user_interface.show_message("Введен неверный код")
                else:
                    self.user_interface.default_info_pane = str(self.search_params)
                    self.user_interface.return_to_previous_menu(info_pane="default")
            # -----------------------------------------------------------------------------------------------------
            elif action == "find vacancies":
                if len(self.vacancies):
                    self.user_interface.ask_vacancies_list_not_empty_when_searching_anew()
                self.user_interface.show_message("Ищем...", pause=False)
                self.find_vacancies(user_response.get("clear vacancies list", True))

            # -----------------------------------------------------------------------------------------------------
            elif action == "search area by substring":
                substring = user_response.get("substring")
                if substring:
                    self.search_area_by_substring(substring)
            # -----------------------------------------------------------------------------------------------------
            elif action == "search vacancies by substring":
                search_substring = user_response.get("substring")
                if search_substring:
                    self.search_params.set_property("text", value=search_substring)
                    self.user_interface.show_current_menu(
                        info_pane=str(self.search_params)
                    )
                    # if search_substring:
                    #     print('1. Искать введенную строку везде')
                    #     print('2. Указать поле поиска')
                    #     user_response = input('Ваш выбор: ')
                    #     if user_response.isdigit():
                    #         user_response = int(user_response)
                    #         if user_response == 2:
                    #             if not HhRef.references.get('vacancy_search_fields'):
                    #                 HhRef('vacancy_search_fields', 'items')
            # -----------------------------------------------------------------------------------------------------
            elif action == "filter vacancies":
                self.filter_found_vacancies()
            # -----------------------------------------------------------------------------------------------------
            elif action == "set min salary":
                min_salary = user_response.get("salary")
                if min_salary is not None:
                    if min_salary == 0:
                        self.search_params.set_property("salary", value="")
                    else:
                        self.search_params.set_property("salary", value=min_salary)
                    self.user_interface.default_info_pane = str(self.search_params)
                    self.user_interface.show_current_menu(info_pane="default")
            # -----------------------------------------------------------------------------------------------------
            elif action == "show all regions sorted by name":
                self.show_all_regions_sorted_by_name()
            # -----------------------------------------------------------------------------------------------------
            elif action == "show all regions sorted by code":
                self.show_all_regions_sorted_by_code()
            # -----------------------------------------------------------------------------------------------------
            elif action == "show area ierarchy":
                self.show_regions_structured()
            # -----------------------------------------------------------------------------------------------------
            elif action == "show subareas":
                parent_code = user_response.get("parent")
                if parent_code:
                    self.show_subareas(parent_code)
            # -----------------------------------------------------------------------------------------------------
            elif action == "set vacancies list limit":
                limit = user_response.get("limit")
                if limit:
                    self.search_params.set_property("search_limit", value=limit)
                    self.user_interface.default_info_pane = str(self.search_params)
                    self.user_interface.show_current_menu(info_pane="default")
            # -----------------------------------------------------------------------------------------------------
            elif action == "delete vacancies":
                indices_str = user_response.get("indices")
                indices = sorted(
                    get_indices(indices_str, len(self.vacancies)), reverse=True
                )
                for i in indices:
                    del self.vacancies[i]
                # self.user_interface.default_info_pane = str(self.search_params)
                # self.user_interface.show_current_menu(info_pane='default')
            # -----------------------------------------------------------------------------------------------------
            elif action == "save vacancies to file":
                data_dir = user_response.get("dir")
                filename = user_response.get("filename")
                filetype = user_response.get("filetype")
                append = user_response.get("append", True)
                if data_dir and filename and filetype:
                    self.save_vacancies_to_file(data_dir, filename, filetype, append)
            # -----------------------------------------------------------------------------------------------------
            elif action == "set search without salary param":
                self.search_params.set_property(
                    "only_with_salary", value=user_response.get("value", True)
                )
                self.user_interface.default_info_pane = str(self.search_params)
                self.user_interface.show_current_menu(info_pane="default")
            # -----------------------------------------------------------------------------------------------------
            elif action == "show top":
                count = user_response.get("count")
                if count:
                    top = sorted(self.vacancies, key=lambda x: x, reverse=True)[
                          : count + 1
                          ]
                    self.user_interface.show_current_menu(
                        info_pane=top, show_info_pane_once=True
                    )
            # -----------------------------------------------------------------------------------------------------
            elif action == "sort vacancies":
                sort_mode = user_response.get("sort_mode")
                if sort_mode:
                    self.sort_vacancies(sort_mode)
            # -----------------------------------------------------------------------------------------------------
            elif action == "set prof id":
                pass
                # prof_id = user_response.get("Prof_id")
            # -----------------------------------------------------------------------------------------------------
            # elif action == "show all professions sorted by name":
            #     self.show_all_professions_names()
            # -----------------------------------------------------------------------------------------------------
            elif action == "reset search parameters":
                del self.search_params
                self.search_params = SearchParameters()
                # self.search_params.reset()
                self.user_interface.default_info_pane = str(self.search_params)
                self.user_interface.show_current_menu(info_pane="default")
            # -----------------------------------------------------------------------------------------------------
            elif action == "work with db connection":
                self.user_interface.set_current_menu("db_menu")
                # self.db_manager.connect()
                self.user_interface.show_current_menu(
                    info_pane=self.db_connection_settings()
                )
            # -----------------------------------------------------------------------------------------------------
            elif action == "connect to db":
                dbname = user_response.get("dbname")
                self.db_manager.connection_settings = {
                    "host": user_response.get("host"),
                    "port": user_response.get("port"),
                    "user": user_response.get("user"),
                    "password": user_response.get("password"),
                    "dbname": dbname,
                }
                self.connect_to_db()
                #     self.user_interface.show_current_menu(info_pane=str(self.db_manager))
                # except psycopg2.OperationalError:
                #     self.user_interface.show_message('Подключиться к базе данных не удалось. ' +
                #                                      'Возможно, она не существует.')
                #     self.user_interface.shrink_db_menu()
                # else:
                #     if self.db_manager.connected():
                #         self.user_interface.extend_db_menu(len(self.vacancies) > 0)
            # -----------------------------------------------------------------------------------------------------
            elif action == "create db":
                self.db_manager.connection_settings = {
                    "host": user_response.get("host"),
                    "port": user_response.get("port"),
                    "user": user_response.get("user"),
                    "dbname": user_response.get("dbname"),
                    "password": user_response.get("password"),
                    "rootpass": user_response.get("rootpass"),
                }
                self.db_manager.create_db()
                if self.db_manager.error_message:
                    self.user_interface.show_message(self.db_manager.error_message)
                else:
                    self.user_interface.extend_db_menu(len(self.vacancies) > 0)
                    self.user_interface.show_current_menu(
                        info_pane=str(self.db_manager)
                    )
            # -----------------------------------------------------------------------------------------------------
            elif action == "get employers data":
                self.load_employers_data()
            # -----------------------------------------------------------------------------------------------------
            elif action == "show employers and vacancies count":
                employers_data = self.db_manager.get_companies_and_vacancies_count()
                self.user_interface.show_current_menu(
                    info_pane=employers_data, show_info_pane_once=True
                )
            # -----------------------------------------------------------------------------------------------------
            elif action == "save vacancies to db":
                self.save_vacancies_to_db()
            # -----------------------------------------------------------------------------------------------------
            elif action == "save connection settings to file":
                filename = user_response.get("filename")
                dir = user_response.get("dir")
                with open(os.path.join(dir, filename), "w", encoding="utf-8") as f:
                    json.dump(self.db_manager.connection_settings, f)
            # -----------------------------------------------------------------------------------------------------
            elif action == "load connection settings from file":
                self.load_db_connection_settings_from_file(
                    user_response.get("filename"), user_response.get("dir")
                )
                self.connect_to_db()
            # -----------------------------------------------------------------------------------------------------
            elif action == "show all vacancies":
                vacancies_from_db = self.db_manager.get_all_vacancies()
                if len(vacancies_from_db):
                    self.user_interface.show_current_menu(
                        info_pane=vacancies_from_db, show_info_pane_once=True
                    )
            # -----------------------------------------------------------------------------------------------------
            elif action == "show average salary in db":
                average_salary = self.db_manager.get_avg_salary()
                self.user_interface.show_message(f"Средняя зарплата: {average_salary}")
            # -----------------------------------------------------------------------------------------------------
            elif action == "show vacancies with salary higher than average":
                vacancies_from_db = self.db_manager.get_vacancies_with_higher_salary()
                if len(vacancies_from_db):
                    self.user_interface.show_current_menu(
                        info_pane=vacancies_from_db, show_info_pane_once=True
                    )
            # -----------------------------------------------------------------------------------------------------
            elif action == "show vacancies with keywords":
                keywords_str = user_response.get("keywords")
                separator = user_response.get("separator")
                if keywords_str:
                    vacancies_from_db = self.db_manager.get_vacancies_with_keyword(
                        keywords_str, separator
                    )
                    if len(vacancies_from_db):
                        self.user_interface.show_current_menu(
                            info_pane=vacancies_from_db, show_info_pane_once=True
                        )
            # -----------------------------------------------------------------------------------------------------

        self.user_interface.clear_user_response()

    def run(self) -> None:
        """
        Основной цикл работы приложения -
        ожидание действий пользователя,
        выполнение команд пользователя
        обновление пользовательского интерфейса
        отображение данных
        """
        self.search_params.set_property(property_name="area", id="113")
        self.user_interface.default_info_pane = str(self.search_params)
        self.user_interface.show_current_menu(
            info_pane="default", show_info_pane_once=False
        )

        while not Application.work_is_over:
            # self.user_interface.show_current_menu(info_pane=str(self.search_params))
            user_choice = self.user_interface.input_request("Ваш выбор: ")
            self.user_interface.respond(user_choice)
            self.check_out_user_response()
            self.user_interface.show_current_menu()

    def sort_vacancies(self, sort_mode: int) -> None:
        """
        Сортировка найденных вакансий
        :param sort_mode: режим сортировки
        """
        reverse_order = False
        property_name = "name"
        value_name = "value"
        if sort_mode == 1:  # По зарплате по убыванию
            property_name = "salary"
            reverse_order = True
        elif sort_mode == 2:  # По зарплате по возрастанию
            property_name = "salary"
            reverse_order = False
        elif sort_mode == 3:  # По должности в алфавитном порядке
            property_name = "name"
        elif sort_mode == 4:  # По региону в алфавитном порядке
            property_name = "area"
        elif sort_mode == 5:  # По работодателю в алфавитном порядке
            property_name = "employer"
        elif sort_mode == 6:  # По адресу в алфавитном порядке
            property_name = "address"
        elif sort_mode == 7:  # По дате публикации: сначала новые
            property_name = "published_at"
        elif sort_mode == 8:  # По дате публикации: сначала старые
            property_name = "published_at"
            reverse_order = True

        if sort_mode < 3:
            self.vacancies = sorted(self.vacancies, key=int, reverse=reverse_order)
        else:
            tried_to_fix_none_values = False
            while True:
                try:
                    self.vacancies = sorted(
                        self.vacancies,
                        key=lambda x: x.properties.get(property_name, {}).get(
                            value_name, ""
                        ),
                        reverse=reverse_order,
                    )
                except TypeError:
                    if tried_to_fix_none_values:
                        break
                    else:
                        tried_to_fix_none_values = True
                        for vac in self.vacancies:
                            val = vac.properties.get(property_name)
                            if not val:
                                vac.set_property(property_name, "")
                            else:
                                target_val = val.get(value_name)
                                if not target_val:
                                    val[value_name] = ""
                else:
                    break

        self.user_interface.show_current_menu(
            info_pane=self.vacancies, show_info_pane_once=True
        )
