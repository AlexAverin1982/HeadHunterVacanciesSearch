# import getpass    глючная хрень
import os

from src.menu_class import Menu

par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
data_dir = os.path.join(par_dir, "data")
settings_dir = os.path.join(par_dir, "settings")


class UserInterface:
    """
    Пользовательский интерфейс с меню
    """

    def __init__(self, menu_handlers: dict | None = None):  # type: ignore
        """
        Конструктор интерфейса
        :param menu_handlers: исходный набор обработчиков для пуктов меню, который может использоваться повторно
        """

        self.__info_pane: str | list = []
        self.default_info_pane: str | list = []
        self.__menus: dict = {}
        self.__menu_names: list = []
        # self.__vacancies: list = []
        self.__current_menu: Menu | None = None
        # self.__previous_menu: Menu | None = None
        self.__user_response: dict = {}
        self.__menu_handlers = menu_handlers
        self.__previous_menus: list = []
        self.__init_menus()
        # self.__menu_items_handlers: dict[str: Callable] = {}

        # self.__previous_menu: Menu | None = None
        # self.display_options = DisplayOptions()

    def __init_menus(self) -> None:
        """
        Инициализация меню
        """

        def init_main_menu():
            main_menu.add_item(
                caption="Изменить параметры поиска",
                pos=0,
                function=self.__change_search_params,
            )
            main_menu.add_item(caption="Искать вакансии", pos=1)

            main_menu.add_item(
                caption="Работать с базой данных",
                pos=95,
                function=self.__work_with_db_connection,
            )

            main_menu.add_item(
                caption="Загрузить вакансии из файла",
                pos=98,
                function=self.__load_vacancies_from_file,
            )

            main_menu.add_item(caption="Выйти из программы.", pos=99)

        def init_search_params_menu():
            search_params_menu.add_item(
                caption="Указать регион", pos=0, function=self.__set_area
            )
            search_params_menu.add_item(
                caption="Указать минимальную зарплату",
                pos=1,
                function=self.__set_min_salary,
            )
            search_params_menu.add_item(
                caption="Указать подстроку для поиска",
                pos=2,
                function=self.__set_search_substring,
            )
            # search_params_menu.add_item(
            #     caption="Указать профессию", pos=3, function=self.__set_profession
            # )
            # search_params_menu.add_item(
            #     caption="Указать опыт", pos=20, function=self.__set_area
            # )
            search_params_menu.add_item(
                caption="Указать максимальное число вакансий",
                pos=30,
                function=self.__set_vacancies_list_limit,
            )
            search_params_menu.add_item(
                caption="Уточнить поиск вакансий без зарплаты",
                pos=96,
                function=self.__set_search_without_salary_param,
            )
            search_params_menu.add_item(
                caption="Установить параметры поиcка по умолчанию",
                pos=97,
                function=self.__reset_search_params,
            )
            search_params_menu.add_item(caption="Вернуться в главное меню", pos=98)
            search_params_menu.add_item(caption="Искать вакансии", pos=99)

        def init_select_area_menu():
            select_area_menu.add_item(
                caption="Ввести код региона", pos=0, function=self.__type_in_area_id
            )
            select_area_menu.add_item(
                caption="Подобрать регион по подстроке",
                pos=1,
                function=self.__search_area_by_substring,
            )
            select_area_menu.add_item(
                caption="Показать все регионы, сортировать в алфавитном порядке",
                pos=2,
                function=self.__show_all_regions_sorted_by_name,
            )
            select_area_menu.add_item(
                caption="Показать все регионы, сортировать по коду",
                pos=3,
                function=self.__show_all_regions_sorted_by_code,
            )
            select_area_menu.add_item(
                caption="Выводить региоры по иерархии, начиная со стран",
                pos=4,
                function=self.__show_areas_ierarchy,
            )
            select_area_menu.add_item(
                caption="Вернуться в предыдущее меню",
                pos=5,
                function=self.return_to_previous_menu,
            )
            select_area_menu.add_item(caption="Вернуться в главное меню", pos=6)
            select_area_menu.add_item(caption="Выйти из программы.", pos=7)
            select_area_menu.add_item(caption="Искать вакансии", pos=99)

        def init_area_ierarchy_menu():
            area_ierarchy_menu.add_item(
                caption="Указать код региона для поиска",
                pos=0,
                function=self.__type_in_area_id,
            )
            area_ierarchy_menu.add_item(
                caption="Указать код региона для просмотра его состава",
                pos=1,
                function=self.__show_subareas,
            )
            area_ierarchy_menu.add_item(
                caption="Вернуться на предыдущий уровень",
                pos=2,
                function=self.return_to_previous_menu,
            )
            area_ierarchy_menu.add_item(
                caption="Вернуться в меню параметров поиска",
                pos=3,
                function=self.return_two_menus_up,
            )
            area_ierarchy_menu.add_item(
                caption="Вернуться в главное меню", pos=4, function=self.return_to_main_menu
            )

        def init_db_menu():
            db_menu.add_item(caption="Создать базу данных", pos=0, function=self.__create_db)
            db_menu.add_item(caption="Подключиться к базе данных", pos=1, function=self.__connect_to_db_server)
            db_menu.add_item(caption="Загрузить подключение из файла и подключиться", pos=2,
                             function=self.__connect_to_db_server_from_file)
            db_menu.add_item(caption="Вернуться в главное меню", pos=99, function=self.return_to_main_menu)

        if not self.__menu_handlers:
            self.__menu_handlers = {}

        self.__menu_handlers["Искать вакансии"] = self.__find_vacancies
        self.__menu_handlers["Вернуться в главное меню"] = self.return_to_main_menu

        main_menu = Menu(name="main_menu",
                         caption="Добро пожаловать в приложение для поиска вакансий с сайта HeadHunter.ru",
                         status_bar=self.__menu_handlers.get("vacancies_count"))
        self.__menus["main_menu"] = main_menu
        init_main_menu()

        # --------------------------------------------------------------------------------------------------------
        search_params_menu = Menu(
            name="change_search_params",
            caption="Укажите параметры поиска:",
            status_bar=self.__menu_handlers.get("vacancies_count"),
        )
        self.__menus["change_search_params"] = search_params_menu
        init_search_params_menu()
        #                           ('Указать отрасль', UserInterface.terminate),
        #                           ('Указать профессию', UserInterface.terminate),
        #                           ('Установить параметры поика по умолчанию', UserInterface.terminate),

        select_area_menu = Menu(name="select_area", caption="Как вы хотите указать регион?")
        self.__menus["select_area"] = select_area_menu
        init_select_area_menu()

        area_ierarchy_menu = Menu("area_ierarchy_menu",
                                  "Регионы верхнего уровня", show_search_params=False)
        self.__menus["area_ierarchy_menu"] = area_ierarchy_menu
        init_area_ierarchy_menu()

        db_menu = Menu(name="db_menu", caption="Работа с базой данных",
                       status_bar=self.__menu_handlers.get("db_status"))
        self.__menus["db_menu"] = db_menu
        init_db_menu()

        # profession_menu = Menu(name="profession_menu", caption="Выбор профессии")
        # self.__menus["profession_menu"] = profession_menu
        #
        # profession_menu.add_item(
        #     caption="Указать код профессии", pos=0, function=self.__type_in_prof_id
        # )
        # profession_menu.add_item(
        #     caption="Вывести все профессии в алфавитном порядке",
        #     pos=1,
        #     function=self.__show_all_professions_sorted_by_name,
        # )
        # profession_menu.add_item(
        #     caption="Вывести все профессии, сортировать по коду", pos=2
        # )
        # profession_menu.add_item(
        #     caption="Вернуться в меню параметров поиска",
        #     pos=98,
        #     function=self.return_to_previous_menu,
        # )
        # profession_menu.add_item(
        #     caption="Вернуться в главное меню",
        #     pos=99,
        #     function=self.return_to_main_menu,
        # )

        self.__menu_names = [
            "main_menu",
            "change_search_params",
            "select_search_region",
            "select_area",
            "area_ierarchy_menu",
            "db_menu"
            # "profession_menu",
        ]
        self.__current_menu = self.__menus["main_menu"]

        """
                                                    ('Указать отрасль', Application.terminate),
                                                    ('Указать профессию', Application.terminate),
                                                    ('Установить параметры поика по умолчанию', Application.terminate),
        """
        self.update_menu_handlers()

    def input_request(self, prompt: str) -> str:
        """
        Запрос выбора пользователя - прокладка
        :param prompt: подсказка
        :return: выбор пользователя
        """
        return input(prompt)

    def extend_main_menu(self) -> None:
        """
        Увеличение (функционала) пунктов меню, когда есть данные, с которым можно работать
        """
        self.__menus["main_menu"].add_item(
            "Просмотреть найденные вакансии", 2, self.ask_for_brief_vacancies_list
        )
        self.__menus["main_menu"].add_item(
            "Показать вакансии детально", 3, self.__ask_vacancies_details
        )
        self.__menus["main_menu"].add_item(
            "Отфильтровать найденные вакансии", 4, self.__filter_vacancies
        )
        self.__menus["main_menu"].add_item(
            "Отсортировать найденные вакансии", 5, self.__sort_vacancies
        )
        self.__menus["main_menu"].add_item(
            "Удалить вакансии из результатов поиска", 6, self.__delete_vacancies
        )
        self.__menus["main_menu"].add_item(
            "Сохранить найденные вакансии в файл", 7, self.__save_vacancies_to_file
        )
        self.__menus["main_menu"].add_item(
            "Топ N вакансий по зарплате", 8, self.__top_n_vacancies
        )
        self.update_menu_handlers()

    def show_current_menu(
            self,
            info_pane: list | str = "current",
            show_info_pane_once: bool = False,
            enumerate_list: bool = True,
            pause: bool = True,
    ) -> None:
        """
        Отображаем текущее меню приложения
        :param info_pane: информационное окно
        :param show_info_pane_once - если True, информационное окно отображается только в этот вызов
        :param enumerate_list: если True - выводимый список в информационном окне нумеруется автоматически
        :param pause: после вывода всей информации ожидать нажатия клавиши Enter
        """

        print("\n")
        print(self.__current_menu.caption)  # type: ignore[union-attr]
        print("-" * 100 + "\n")
        if info_pane:
            if isinstance(info_pane, str):
                if info_pane == "default":
                    print(self.default_info_pane)
                    if not show_info_pane_once:
                        self.__info_pane = self.default_info_pane
                elif info_pane == "current":
                    print(self.__info_pane)
                else:
                    print(info_pane)
                    if not show_info_pane_once:
                        self.__info_pane = info_pane
                print("\n")
                # self.__info_pane = info_pane
            elif isinstance(info_pane, list):
                if not show_info_pane_once:
                    self.__info_pane = ""
                for ind, item in enumerate(info_pane):
                    if enumerate_list:
                        line = f"{ind + 1}. {str(item)}"
                    else:
                        line = f"{str(item)}"
                    print(line)
                    if not show_info_pane_once:
                        self.__info_pane += line + "\n"  # type: ignore[operator]
                print("\n")
                self.show_message(pause=pause)

        print(self.__current_menu)

        # print(f'Сейчас найдено {len(self.vacancies)} вакансий')

    def set_current_menu(self, menu_name: str) -> None:
        """
        Установка текущего меню с сохранением истории ноавигации
        :param menu_name: имя устанавливаемого меню
        """
        if menu_name in self.__menus.keys():
            self.__previous_menus.append(self.__menus[self.__current_menu.menu_name()])  # type: ignore[union-attr]
            self.__current_menu = self.__menus[menu_name]

    def return_to_main_menu(self) -> None:
        """
        Возврат в главное меню и сброс истории навигации
        """
        self.set_current_menu("main_menu")
        self.__previous_menus = []

    def return_to_previous_menu(self, info_pane: list | str = "current") -> None:
        """
        Возврат в предыдущее меню
        :param info_pane: выводимая информация
        """
        if len(self.__previous_menus):
            self.__current_menu = self.__previous_menus.pop()
            self.__previous_menus = self.__previous_menus[1:]
            if isinstance(info_pane, str):
                if info_pane == "default":
                    self.__info_pane = self.default_info_pane
                elif info_pane != "current":
                    self.__info_pane = info_pane

    def return_two_menus_up(self, info_pane: list | str = "current") -> None:
        """
        возврат назад через два меню в истории
        :param info_pane: выводимая информация
        """
        if len(self.__previous_menus) > 2:
            self.__current_menu = self.__previous_menus[1]
            self.__previous_menus = self.__previous_menus[2:]
            if isinstance(info_pane, str):
                if info_pane == "default":
                    self.__info_pane = self.default_info_pane
                elif info_pane != "current":
                    self.__info_pane = info_pane

    def __sort_vacancies(self) -> None:
        """
        Вывод меню для выбора режима сортировки
        """
        while True:
            print("Выберите вид сортировки:")
            print("1. По зарплате по убыванию")
            print("2. По зарплате по возрастанию")
            print("3. По должности в алфавитном порядке")
            print("4. По региону в алфавитном порядке")
            print("5. По работодателю в алфавитном порядке")
            print("6. По адресу в алфавитном порядке")
            print("7. По дате публикации: сначала новые")
            print("8. По дате публикации: сначала старые")
            sort_mode = input("Ваш выбор (пустая строка для отмены):")
            if sort_mode:
                if sort_mode.isdigit() and (int(sort_mode) in range(1, 9)):
                    self.__user_response = {
                        "action": "sort vacancies",
                        "sort_mode": int(sort_mode),
                    }
                    break
                else:
                    print("Введите целое число 1-8")
            else:
                break

    def __load_vacancies_from_file(self) -> None:
        """
        Сбор информации для загрузки файла
        Показать текущую папку файлов
        запросить имя файла / имя папки файлов
        определить тип файла
        по типу файла определить файловый менеджер
        послать ему информацию о файле
        получить от него вакансии
        отобразить информацию о готовности работать дальше
        :return:
        """
        print(f"Файл будет загружен из каталога {data_dir}")
        filename = input("Введите имя файла (введите пустую строку для отмены): ")
        if not filename:
            return
        filetype_choice = "1"

        print("Использовать текущие условия поиска, чтобы фильтровать данные из файла?")
        print("1. Да")
        print("2. Нет, считать файл полностью")
        user_response = input("Ваш выбор: ")
        filter_when_load = user_response == "1"
        fails_if_none = False
        if filter_when_load:
            print(
                "Если свойство, указанное в условиях, отсутствует в описании вакансии:"
            )
            print("1. Считать, что вакансия не подходит")
            print("2. Считать, что вакансия подходит")
            user_response = input("Ваш выбор: ")
            fails_if_none = user_response == "1"
        if filename.lower().endswith(".txt"):
            filetype_choice = "1"
        elif filename.lower().endswith(".csv"):
            filetype_choice = "2"
        elif filename.lower().endswith(".json"):
            filetype_choice = "3"

        self.__user_response = {
            "action": "load vacancies from file",
            "dir": data_dir,
            "filename": filename,
            "filetype": filetype_choice,
            "filter": filter_when_load,
            "fails if none": fails_if_none,
        }
        # 'additional request': "check if vacancies list is not empty"}

    def __find_vacancies(self) -> None:
        """
        Команда для поиска вакансий
        """
        self.__user_response = {"action": "find vacancies"}

    def __type_in_area_id(self) -> None:
        """
        Ввод кода региона
        """
        self.__user_response = {
            "action": "set area id",
            "id": input("Введите код региона (113 - вся Россия): "),
        }

    def __type_in_prof_id(self) -> None:
        """
        Ввод кода профессии
        """
        prof_id = input("Введите код региона (пустая строка для отмены: ")
        if prof_id:
            self.__user_response = {"action": "set prof id", "prof_id": prof_id}

    def __search_area_by_substring(self) -> None:
        """
        Запрос у пользователя подстроки для поиска региона
        """
        search_substring = input(
            "Введите часть наименования региона (пустую строку для отмены):"
        ).lower()
        if search_substring:
            self.__user_response = {
                "action": "search area by substring",
                "substring": search_substring,
            }

    def __show_all_regions_sorted_by_name(self) -> None:
        """
        Запрос у приложения списка всех регионов, отсортированных в алфавитном порядке
        """
        self.__user_response = {"action": "show all regions sorted by name"}

    def __show_all_regions_sorted_by_code(self) -> None:
        """
        Запрос у приложения списка всех регионов, отсортированных по коду
        """
        self.__user_response = {"action": "show all regions sorted by code"}

    def __set_search_substring(self) -> None:
        """
        Запрос у пользователя подстроки для поиска в тексте вакансии
        """
        search_substring = input(
            "Введите строку для поиска (пустую строку, если искать не надо):"
        ).lower()
        if search_substring:
            self.__user_response = {
                "action": "search vacancies by substring",
                "substring": search_substring,
            }

            # print('1. Искать введенную строку везде')
            # print('2. Указать поле поиска')
            # user_response = input('Ваш выбор: ')
            # if user_response.isdigit():
            #     user_response = int(user_response)
            #     if user_response == 2:
            #         if not HhRef.references.get('vacancy_search_fields'):
            #             HhRef('vacancy_search_fields', 'items')

    def __set_profession(self) -> None:
        """
        Выбор искомой профессии
        """
        self.set_current_menu("profession_menu")

    def __set_vacancies_list_limit(self) -> None:
        """
        Ограничение числа искомых вакансий
        """
        limit = None
        while True:
            try:
                user_input = input(
                    "Введите максимальное число вакансий в результатах поиска (пустая строка для отмены):"
                )
                if user_input:
                    limit = int(user_input)
                    break
                else:
                    break
            except ValueError:
                print("Введите целое число или пустую строку для отмены")
        if limit:
            self.__user_response = {
                "action": "set vacancies list limit",
                "limit": limit,
            }

    def __filter_vacancies(self) -> None:
        """
        Командуем отфильтровать найденные вакансии по параметрам поиска
        """
        self.__user_response = {"action": "filter vacancies"}

    def show_message(self, message: str = "", pause: bool = True) -> None:
        """
        Отображение сообщения пользователю с опциональной паузой
        :param message: сообщение
        :param pause: если True - ожидает нажатия Enter после вывода сообщения
        """
        if message:
            print(message)
        if pause:
            input("Нажмите Enter")

    def ask_vacancies_list_not_empty_when_loading_from_file(self) -> None:
        """
        Уточнение действий пользователя при загрузке данных, когда результаты поиска уже присутствуют в памяти
        """
        print("Что сделать с текущим набором вакансий?")
        print("1. Оставить, загруженные из файла вакансии добавить к текущим")
        print("2. Очистить, загруженные из файла вакансии полностью заменяют текущие.")
        resp = input("Ваш выбор: ")
        self.__user_response = {"clear vacancies list": resp == "2"}

    def ask_vacancies_list_not_empty_when_searching_anew(self) -> None:
        """
        Уточнение действий пользователя при повторном поиске, когда результаты поиска уже присутствуют в памяти
        """
        print("Очистить текущий список вакансий?")
        print("1. Да, очистить результаты поиска.")
        print("2. Нет, объединить новые результаты поиска с уже существующими.")
        self.__user_response = {"очистить список вакансий": input("Ваш выбор: ") == "2"}
        print("Ищем...")

    def respond(self, user_choice: str) -> None:
        """
        Реакция приложения (пользовательского интерфейса) на действие пользователя (выбор пункта текущего меню)
        :param user_choice: пункт меню, выбранный пользователем
        """
        if user_choice and user_choice.isdigit():
            try:
                user_choice = int(user_choice) - 1  # type: ignore[assignment]
                self.__current_menu.select_menu_item(user_choice)  # type: ignore[union-attr, arg-type]
            except IndexError:
                print("Такого пункта в меню нет.")

    def update_menu_handlers(self) -> None:
        """
        Установка (повторная) обработчиков пунктов меню
        """
        for caption, handler in self.__menu_handlers.items():  # type: ignore[union-attr]
            for menu in self.__menus.values():
                menu.set_menu_item_handler((caption, handler))

    def __change_search_params(self) -> None:
        """
        Изменение параметров поиска
        """
        # self.__previous_menus.insert(0, self.__current_menu)
        self.set_current_menu("change_search_params")

    def __ask_vacancies_details(self) -> None:
        """
        Запрос на отображение подробной информации по вакансиям
        """
        self.__user_response = {"action": "show vacancies details"}
        print("1. Показать подробно все вакансии.")
        print("2. Показать подробно только выбранные вакансии.")
        user_response = input("Ваш выбор: ")
        if user_response != "1":
            print(
                "Введите номера вакансий из списка найденных, которые вы хотите просмотреть."
            )
            print(
                "Номера можно указывать через запятую, или тире для указания диапазона"
            )
            print("Диапазоны также можно указывать через запятую")
            print("Введите пустую строку для отмены просмотра")
            indices_str = input("Ваш выбор: ")
            if indices_str:
                self.__user_response["indices"] = indices_str
            else:
                self.clear_user_response()
                return

    def __set_area(self) -> None:
        """
        Запрос на указания региона для поиска
        """
        self.set_current_menu("select_area")

    def __show_areas_ierarchy(self) -> None:
        """
        Запрос выбора региона в иерархическом порядке
        """
        self.set_current_menu("area_ierarchy_menu")
        self.__user_response = {"action": "show area ierarchy"}

    def __show_subareas(self) -> None:
        """
        Запрос на просмотр состава региона
        """
        user_response = input(
            "Введите код региона для просмотра его состава (пустая строка для отмены): "
        )
        if user_response:
            self.__user_response = {"action": "show subareas", "parent": user_response}

    def __set_min_salary(self) -> None:
        """
        Указываем минимальную зарплату в параметрах поиска
        """
        while True:
            new_slary = input(
                "Введите нижний порог зарплаты в рублях (0, если порога нет): "
            )
            if new_slary.isdigit():
                self.__user_response = {
                    "action": "set min salary",
                    "salary": int(new_slary),
                }
                # self.search_params.set_property('salary', value=int(new_slary))
                break
            else:
                print("Введите целое число")

    def __set_search_without_salary_param(self) -> None:
        """
        Уточняем, искать ли вакансии без указанной зарплаты
        """
        print("Показывать вакансии, в которых не указана зарплата?")
        print("1. Нет")
        print("2. Да")
        user_response = input("Ваш выбор :")
        self.__user_response = {
            "action": "set search without salary param",
            "value": user_response == "1",
        }

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
        print(f"Файл будет сохранен в каталоге {data_dir}")
        while True:
            filename = input(
                "Введите имя файла с расширением (введите пустую строку для отмены): "
            )
            if not filename:
                return
            filetype_choice = None

            if filename.lower().endswith(".txt"):
                filetype_choice = "1"
            elif filename.lower().endswith(".csv"):
                filetype_choice = "2"
            elif filename.lower().endswith(".json"):
                filetype_choice = "3"

            if filetype_choice:
                break
            else:
                print("Желаемый формат для сохранения файла не определен.")
                print("Укажите имя файла с расширением через точку")

        if os.path.exists(os.path.join(data_dir, filename)):
            print("Указанный файл существует. Что нужно сделать?")
            print("1. Дозаписать данные, сохранив уже записанные.")
            print("2. Перезаписать файл полностью.")
            print("3. Отменить сохранение.")
            write_mode_choice = input("Ваш выбор :")

            if write_mode_choice == "1":
                append = True
            elif write_mode_choice == "2":
                append = False
            else:
                self.__user_response = {}
                return
        else:
            append = False

        self.__user_response = {
            "action": "save vacancies to file",
            "dir": data_dir,
            "filename": filename,
            "filetype": filetype_choice,
            "append": append,
        }

    def __delete_vacancies(self) -> None:
        """
        Удалить вакансии из результатов поиска по номерам в списке
        """
        print("Введите номера вакансий, которые вы хотите удалить из списка.")
        print("Номера можно указывать через запятую, или тире для указания диапазона")
        print("Диапазоны также можно указывать через запятую")
        print("Введите пустую строку для отмены удаления")
        indices_str = input("Ваш выбор: ")
        if indices_str:
            self.__user_response = {
                "action": "delete vacancies",
                "indices": indices_str,
            }

    def __top_n_vacancies(self) -> None:
        """
        Запрос на показ топа вакансий по зарплате
        """
        while True:
            user_response = input("Введите число вакансий в топе: ")
            if user_response.isdigit():
                user_response = int(user_response)  # type: ignore[assignment]
                break
            print("Введите целое число")
        self.__user_response = {"action": "show top", "count": user_response}

    def __show_all_professions_sorted_by_name(self) -> None:
        """
        Отображение списка профессий, отсортированного в алфавитном порядке
        """
        self.__user_response = {"action": "show all professions sorted by name"}

    def __reset_search_params(self) -> None:
        """
        Сброс параметров поиска
        """
        self.__user_response = {"action": "reset search parameters"}

    def __work_with_db_connection(self):
        self.__user_response = {'action': 'work with db connection'}

    def request_db_connection_settings(self, request_sa_password: bool = False):
        """
        Запрос настроек для подключения к базе данных
        """
        self.__user_response = {}
        host = port = dbname = user = password = rootpass = ''
        host = input('Введите сетевое имя сервера баз данных(по умолчанию localhost): ')
        if not host:
            host = 'localhost'
        port = input('Введите номер порта сервера баз данных (по умолчанию 5432): ')
        if not port:
            port = '5432'

        dbname = input('Введите имя базы данных: ')
        if dbname:
            if request_sa_password:
                # rootpass = getpass.getpass("Введите пароль администратора базы данных: ")
                rootpass = input("Введите пароль администратора базы данных: ")

            user = input('Введите имя пользователя (по умолчанию postgres): ')
            if not user:
                user = 'postgres'
            if user:
                # password = getpass.getpass("Введите пароль: ")
                password = input("Введите пароль: ")
                if not password:
                    return
        if host and port and dbname and user and password:
            self.__user_response = {'action': 'connect to db',
                                    'host': host,
                                    'port': port,
                                    'dbname': dbname,
                                    'user': user,
                                    'password': password}
            if rootpass:
                self.__user_response['rootpass'] = rootpass

    def __connect_to_db_server(self) -> None:
        """
        Подключиться к серверу баз данных
        """
        self.__user_response = {}
        self.request_db_connection_settings()
        self.__user_response['action'] = 'connect to db'

    def __create_db(self):
        # self.__user_response = {'action': 'create db',
        #                         'host': 'localhost',
        #                         'port': '5432',
        #                         'user': 'user',
        #                         'password': 'password',
        #                         'dbname': 'dbname',
        #                         'rootpass': 'rootpass'}

        self.request_db_connection_settings(request_sa_password=True)
        if self.__user_response:
            self.__user_response['action'] = 'create db'

    def __get_employers_data(self):
        self.__user_response = {'action': 'get employers data'}

    def __show_employers_and_vacancies_count(self):
        self.__user_response = {'action': 'show employers and vacancies count'}

    def __save_vacancies_to_db(self) -> None:
        self.__user_response = {'action': 'save vacancies to db'}

    def __save_connection_settings_to_file(self) -> None:
        """
        Сохраняем настройки подключения к базе данных в файл
        """
        self.__user_response = {'action': 'save connection settings to file',
                                'dir': settings_dir,
                                'filename': input('Введите имя файла: ')}
        if not self.__user_response['filename']:
            self.__user_response = {}

    def __connect_to_db_server_from_file(self) -> None:
        """
        Загружаем настройки подключения к базе данных из файла и подключаемся
        """
        self.__user_response = {'action': 'load connection settings from file',
                                'dir': settings_dir,
                                'filename': input('Введите имя файла: ')}
        if not self.__user_response['filename']:
            self.__user_response['filename'] = 'hh.json'

    def __show_all_vacancies(self) -> None:
        """
        Показываем все вакансии из базы данных
        """
        self.__user_response = {'action': 'show all vacancies'}

    def __show_average_salary_in_db(self) -> None:
        """
        Показываем среднюю зарплату по всем вакансиям в базе данных
        """
        self.__user_response = {'action': 'show average salary in db'}

    def __show_vacancies_higher_than_avg(self) -> None:
        """
        Показываем вакансии с зарплатой выше средней
        """
        self.__user_response = {'action': 'show vacancies with salary higher than average'}

    def __show_vacancies_with_keywords(self) -> None:
        """
        Показываем вакансии, содержащие в названии ключевые слова
        """
        keywords = []
        while True:
            keyword = input('Введите ключевое слово (пустую строку, чтобы закончить ввод): ')
            if keyword:
                keywords.append(keyword)
            else:
                break

        separator = input('Введите разделитель (запятая по умолчанию): ')
        if not separator:
            separator = ','
        keywords_str = separator.join(keywords)

        self.__user_response = {'action': 'show vacancies with keywords',
                                'keywords': keywords_str,
                                'separator': separator}

    def shrink_main_menu(self) -> None:
        """
        Убираем пункты главного меню, когда список вакансий пуст, с ним действий нет
        """
        self.__menus["main_menu"].delete_item("Просмотреть найденные вакансии")
        self.__menus["main_menu"].delete_item("Показать вакансии детально")
        self.__menus["main_menu"].delete_item("Отфильтровать найденные вакансии")
        self.__menus["main_menu"].delete_item("Отсортировать найденные вакансии")
        self.__menus["main_menu"].delete_item("Сохранить найденные вакансии в файл")
        self.__menus["main_menu"].delete_item("Топ N вакансий по зарплате")
        self.__menus["main_menu"].delete_item("Удалить вакансии из результатов поиска")

    def shrink_db_menu(self) -> None:
        """
        Удаляем часть пунктов меню работы с базами данных, если подключения к серверу бд нет
        """
        self.__menus["db_menu"].delete_item("Загрузить информацию о работодателях")
        self.__menus["db_menu"].delete_item("Показать работодателей и количество их вакансий")
        self.__menus["db_menu"].delete_item("Сохранить вакансии в базу данных")
        self.__menus["db_menu"].delete_item("Сохранить настройки подключения в файл")
        self.__menus["db_menu"].delete_item("Показать все вакансии из базы данных")
        self.__menus["db_menu"].delete_item("Показать среднюю зарплату по базе данных")
        self.__menus["db_menu"].delete_item("Показать вакансии с зарплатой выше средней")
        self.__menus["db_menu"].delete_item("Показать вакансии, содержащие ключевые слова")

    def extend_db_menu(self, vacancies_present: bool) -> None:
        """
        Добавляем пункты меню работы с базами данных, когда подключение к серверу бд установлено
        """

        self.__menus["db_menu"].add_item(caption="Загрузить информацию о работодателях",
                                         pos=97, function=self.__get_employers_data)

        self.__menus["db_menu"].add_item(caption="Показать все вакансии из базы данных",
                                         pos=2, function=self.__show_all_vacancies)

        self.__menus["db_menu"].add_item(caption="Показать среднюю зарплату по базе данных",
                                         pos=3, function=self.__show_average_salary_in_db)

        self.__menus["db_menu"].add_item(caption="Показать вакансии с зарплатой выше средней",
                                         pos=4, function=self.__show_vacancies_higher_than_avg)

        self.__menus["db_menu"].add_item(caption="Показать вакансии, содержащие ключевые слова",
                                         pos=5, function=self.__show_vacancies_with_keywords)

        self.__menus["db_menu"].add_item(caption="Показать работодателей и количество их вакансий",
                                         pos=10, function=self.__show_employers_and_vacancies_count)

        self.__menus["db_menu"].add_item(caption="Сохранить настройки подключения в файл",
                                         pos=99, function=self.__save_connection_settings_to_file)

        if vacancies_present:
            self.__menus["db_menu"].add_item(caption="Сохранить вакансии в базу данных",
                                             pos=98, function=self.__save_vacancies_to_db)

    def user_response(self) -> dict:
        """
        Возрват приложению информации о действиях пользователя
        :return:
        """
        return self.__user_response

    def ask_for_brief_vacancies_list(self) -> None:
        """
        Вызов краткой информации о найденных вакансиях
        :return:
        """
        self.__user_response = {"action": "show vacancies list"}

    def clear_user_response(self) -> None:
        """
        Очищение информации о действиях пользователя
        """
        self.__user_response = {}
