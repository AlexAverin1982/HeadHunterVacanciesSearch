import os

import src.menu_class
import src.user_interface_class
from src.user_interface_class import UserInterface

output: list = []
input_values: list = []


def test_init__(class_user_interface_fixture: UserInterface) -> None:
    ui = class_user_interface_fixture
    assert set(ui._UserInterface__menus.keys()) == {  # type: ignore[attr-defined]
        'area_ierarchy_menu',
        'change_search_params',
        'db_menu',
        'main_menu',
        'select_area'
    }


def test_extend_main_menu() -> None:
    ui = UserInterface()
    ui.extend_main_menu()
    main_menu = ui._UserInterface__menus["main_menu"]  # type: ignore[attr-defined]
    items = str(main_menu).split("\n")
    assert items == ['1. Изменить параметры поиска',
                     '2. Искать вакансии',
                     '3. Просмотреть найденные вакансии',
                     '4. Показать вакансии детально',
                     '5. Отфильтровать найденные вакансии',
                     '6. Отсортировать найденные вакансии',
                     '7. Удалить вакансии из результатов поиска',
                     '8. Сохранить найденные вакансии в файл',
                     '9. Топ N вакансий по зарплате',
                     '10. Работать с базой данных',
                     '11. Загрузить вакансии из файла',
                     '12. Выйти из программы.',
                     '',
                     '']


def test_show_current_menu() -> None:
    output: list = []
    ui = UserInterface()
    src.user_interface_class.print = lambda s: output.append(  # type: ignore[attr-defined]
        s
    )  # если надо, можем посмотреть, что выводилось в консоль
    ui.set_current_menu("main_menu")
    ui.show_current_menu()
    assert (
            output[1]
            == "Добро пожаловать в приложение для поиска вакансий с сайта HeadHunter.ru"
    )


def test_show_current_menu2() -> None:
    output = []
    ui = UserInterface()
    src.user_interface_class.print = lambda s: output.append(  # type: ignore[attr-defined]
        s
    )  # если надо, можем посмотреть, что выводилось в консоль
    ui.set_current_menu("main_menu")
    ui.show_current_menu(info_pane="default")
    assert (
            output[1]
            == "Добро пожаловать в приложение для поиска вакансий с сайта HeadHunter.ru"
    )


def test_show_current_menu_with_info_pane() -> None:
    output = []
    ui = UserInterface()
    src.user_interface_class.print = lambda s: output.append(  # type: ignore[attr-defined]
        s
    )  # если надо, можем посмотреть, что выводилось в консоль
    ui.set_current_menu("main_menu")
    ui.show_current_menu(info_pane="test info", show_info_pane_once=True)
    assert output[3] == "test info"
    output = []
    ui.show_current_menu()
    assert output[3] != "test info"
    output = []
    ui.show_current_menu(info_pane="test info", show_info_pane_once=False)
    assert output[3] == "test info"
    output = []
    ui.show_current_menu()
    assert output[3] == "test info"
    output = []
    ui.show_current_menu(
        info_pane=["info1", "info2"], show_info_pane_once=False, pause=False
    )
    assert (output[3] == "1. info1") and (output[4] == "2. info2")
    output = []
    ui.show_current_menu(
        info_pane=["info1", "info2"], pause=False, enumerate_list=False
    )
    assert (output[3] == "info1") and (output[4] == "info2")


def test_return_to_main_menu() -> None:
    output = []
    ui = UserInterface()
    src.user_interface_class.print = lambda s: output.append(  # type: ignore[attr-defined]
        s
    )  # если надо, можем посмотреть, что выводилось в консоль

    ui.set_current_menu("change_search_params")
    ui.show_current_menu()
    passed = output[1] == "Укажите параметры поиска:"
    assert passed
    output = []
    ui.return_to_main_menu()
    ui.show_current_menu()
    assert (
            output[1]
            == "Добро пожаловать в приложение для поиска вакансий с сайта HeadHunter.ru"
    )


def test_return_to_previous_menu() -> None:
    output = []
    ui = UserInterface()
    src.user_interface_class.print = lambda s: output.append(  # type: ignore[attr-defined]
        s
    )  # если надо, можем посмотреть, что выводилось в консоль

    ui.set_current_menu("change_search_params")
    ui.show_current_menu()
    assert output[1] == "Укажите параметры поиска:"
    output = []
    # ui.set_current_menu('change_search_params')
    ui.return_to_previous_menu()
    ui.show_current_menu()
    assert (
            output[1]
            == "Добро пожаловать в приложение для поиска вакансий с сайта HeadHunter.ru"
    )
    ui.set_current_menu("change_search_params")
    ui.return_to_previous_menu(info_pane="default")
    output = []
    ui.show_current_menu()
    assert (
            output[1]
            == "Добро пожаловать в приложение для поиска вакансий с сайта HeadHunter.ru"
    )
    ui.set_current_menu("change_search_params")
    ui.return_to_previous_menu(info_pane="default1")
    output = []
    ui.show_current_menu()
    assert (
            output[1]
            == "Добро пожаловать в приложение для поиска вакансий с сайта HeadHunter.ru"
    )


def test_return_two_menus_up() -> None:
    output = []
    ui = UserInterface()
    src.user_interface_class.print = lambda s: output.append(  # type: ignore[attr-defined]
        s
    )  # если надо, можем посмотреть, что выводилось в консоль

    ui.set_current_menu("change_search_params")
    ui.show_current_menu()
    assert output[1] == "Укажите параметры поиска:"
    ui.set_current_menu("select_area")
    ui.set_current_menu("area_ierarchy_menu")
    output = []
    ui.return_two_menus_up(info_pane="default")
    ui.show_current_menu()
    assert output[1] == "Укажите параметры поиска:"

    ui.set_current_menu("change_search_params")
    ui.set_current_menu("select_area")
    ui.set_current_menu("area_ierarchy_menu")
    output = []
    ui.return_two_menus_up(info_pane="default1")
    ui.show_current_menu()
    assert output[1] == "Укажите параметры поиска:"


def mock_input(s: str) -> str:  # мокаем ввод пунктов меню
    """Мокаем пользовательский ввод с клавиатуры"""
    global output
    global input_values
    output.append(s)
    return str(input_values.pop(0))


def test_sort_vacancies() -> None:
    global input_values
    global output

    ui = UserInterface()

    src.user_interface_class.input = mock_input  # type: ignore[attr-defined]
    # input_values = [str(user_response) for user_response in range(1,10)]
    # input_values = []
    for user_response in range(1, 9):
        input_values = [str(user_response)]
        ui._UserInterface__sort_vacancies()  # type: ignore[attr-defined]
        assert ui.user_response() == {
            "action": "sort vacancies",
            "sort_mode": user_response,
        }

    input_values = ["9", ""]
    ui._UserInterface__sort_vacancies()  # type: ignore[attr-defined]
    assert ui.user_response() == {"action": "sort vacancies", "sort_mode": 8}


def test_load_vacancies_from_file() -> None:
    global input_values
    global output
    par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
    data_dir = os.path.join(par_dir, "data")

    ui = UserInterface()
    src.user_interface_class.input = mock_input  # type: ignore[attr-defined]
    input_values = [
        "test6.json",
        "2",
    ]
    ui._UserInterface__load_vacancies_from_file()  # type: ignore[attr-defined]
    assert ui.user_response() == {
        "action": "load vacancies from file",
        "dir": data_dir,
        "filename": "test6.json",
        "filetype": "3",
        "filter": False,
        "fails if none": False,
    }
    input_values = [""]
    ui.clear_user_response()
    ui._UserInterface__load_vacancies_from_file()  # type: ignore[attr-defined]
    assert ui.user_response() == {}
    input_values = ["test6.txt", "1", "1"]
    ui._UserInterface__load_vacancies_from_file()  # type: ignore[attr-defined]
    assert ui.user_response() == {
        "action": "load vacancies from file",
        "dir": data_dir,
        "filename": "test6.txt",
        "filetype": "1",
        "filter": True,
        "fails if none": True,
    }
    input_values = ["test6.csv", "1", "2"]
    ui._UserInterface__load_vacancies_from_file()  # type: ignore[attr-defined]
    assert ui.user_response() == {
        "action": "load vacancies from file",
        "dir": data_dir,
        "filename": "test6.csv",
        "filetype": "2",
        "filter": True,
        "fails if none": False,
    }


def test_find_vacancies() -> None:
    ui = UserInterface()
    ui._UserInterface__find_vacancies()  # type: ignore[attr-defined]
    assert ui.user_response() == {"action": "find vacancies"}


def test_type_in_area_id() -> None:
    global input_values
    ui = UserInterface()
    src.user_interface_class.input = mock_input  # type: ignore[attr-defined]
    input_values = ["113"]
    ui._UserInterface__type_in_area_id()  # type: ignore[attr-defined]
    assert ui.user_response() == {"action": "set area id", "id": "113"}


def test_type_in_prof_id() -> None:
    global input_values
    ui = UserInterface()
    src.user_interface_class.input = mock_input  # type: ignore[attr-defined]
    input_values = ["1"]
    ui._UserInterface__type_in_prof_id()  # type: ignore[attr-defined]
    assert ui.user_response() == {"action": "set prof id", "prof_id": "1"}


def test_search_area_by_substring() -> None:
    global input_values
    ui = UserInterface()
    src.user_interface_class.input = mock_input  # type: ignore[attr-defined]
    input_values = ["Тамбов"]
    ui._UserInterface__search_area_by_substring()  # type: ignore[attr-defined]
    assert ui.user_response() == {
        "action": "search area by substring",
        "substring": "тамбов",
    }


def test_show_all_regions_sorted_by_name() -> None:
    ui = UserInterface()
    ui._UserInterface__show_all_regions_sorted_by_name()  # type: ignore[attr-defined]
    assert ui.user_response() == {"action": "show all regions sorted by name"}


def test_show_all_regions_sorted_by_code() -> None:
    ui = UserInterface()
    ui._UserInterface__show_all_regions_sorted_by_code()  # type: ignore[attr-defined]
    assert ui.user_response() == {"action": "show all regions sorted by code"}


def test_set_search_substring() -> None:
    global input_values
    ui = UserInterface()
    src.user_interface_class.input = mock_input  # type: ignore[attr-defined]
    input_values = ["Тамбов"]
    ui._UserInterface__set_search_substring()  # type: ignore[attr-defined]
    assert ui.user_response() == {
        "action": "search vacancies by substring",
        "substring": "тамбов",
    }


# def test_set_profession() -> None:
#     ui = UserInterface()
#     output: list = []
#     src.user_interface_class.print = lambda s: output.append(s)  # type: ignore[attr-defined]
#     ui._UserInterface__set_profession()  # type: ignore[attr-defined]
#     ui.show_current_menu()
#     assert output[1] == "Выбор профессии"


def test_set_vacancies_list_limit() -> None:
    global input_values
    ui = UserInterface()
    src.user_interface_class.input = mock_input  # type: ignore[attr-defined]
    input_values = ["1"]
    ui._UserInterface__set_vacancies_list_limit()  # type: ignore[attr-defined]
    assert ui.user_response() == {"action": "set vacancies list limit", "limit": 1}
    input_values = [""]
    ui.clear_user_response()
    ui._UserInterface__set_vacancies_list_limit()  # type: ignore[attr-defined]
    assert ui.user_response() == {}
    input_values = ["fnbrtntn", ""]
    output = []
    src.user_interface_class.print = lambda s: output.append(s)  # type: ignore[attr-defined]
    ui._UserInterface__set_vacancies_list_limit()  # type: ignore[attr-defined]
    assert output[0] == "Введите целое число или пустую строку для отмены"


def test_filter_vacancies() -> None:
    ui = UserInterface()
    ui._UserInterface__filter_vacancies()  # type: ignore[attr-defined]
    assert ui.user_response() == {"action": "filter vacancies"}


def test_show_message() -> None:
    global input_values
    global output
    ui = UserInterface()
    output = []
    src.user_interface_class.print = lambda s: output.append(s)  # type: ignore[attr-defined]
    ui.show_message("test", pause=False)
    ui.show_current_menu()
    assert output[0] == "test"
    input_values = ["\n"]
    src.user_interface_class.input = mock_input  # type: ignore[attr-defined]
    output = []
    ui.show_message("test", pause=True)
    assert (output[0] == "test") and (output[1] == "Нажмите Enter")


def test_ask_vacancies_list_not_empty_when_loading_from_file() -> None:
    global input_values
    ui = UserInterface()
    src.user_interface_class.input = mock_input  # type: ignore[attr-defined]
    input_values = ["1"]
    ui.ask_vacancies_list_not_empty_when_loading_from_file()
    assert ui.user_response() == {"clear vacancies list": False}


def test_ask_vacancies_list_not_empty_when_searching_anew() -> None:
    global input_values
    ui = UserInterface()
    src.user_interface_class.input = mock_input  # type: ignore[attr-defined]
    input_values = ["1"]
    ui.ask_vacancies_list_not_empty_when_searching_anew()
    assert ui.user_response() == {"очистить список вакансий": False}


def test_respond() -> None:
    ui = UserInterface()
    output = []
    src.user_interface_class.print = lambda s: output.append(s)  # type: ignore[attr-defined]
    ui.return_to_main_menu()
    ui.respond("1")
    assert ui._UserInterface__current_menu.caption == "Укажите параметры поиска:"  # type: ignore[attr-defined]
    ui.clear_user_response()
    ui.respond("1111")
    assert output == ["Такого пункта в меню нет."]


def test_update_menu_handlers() -> None:
    def say_hi() -> None:
        print("hi!")

    output: list = []
    print = lambda s: output.append(s)  # type: ignore[attr-defined]
    menu_handlers = {"Изменить параметры поиска": say_hi}
    ui = UserInterface(menu_handlers)
    ui.update_menu_handlers()
    ui.return_to_main_menu()
    ui.respond("1")
    assert output[0] == "hi!"


def test_change_search_params() -> None:
    ui = UserInterface()
    ui.return_to_main_menu()
    output: list = []
    src.user_interface_class.print = lambda s: output.append(s)  # type: ignore[attr-defined]
    ui._UserInterface__change_search_params()  # type: ignore[attr-defined]
    ui.show_current_menu()
    assert output[1] == "Укажите параметры поиска:"


def test_ask_vacancies_details() -> None:
    global input_values
    ui = UserInterface()
    src.user_interface_class.input = mock_input  # type: ignore[attr-defined]
    input_values = ["2", "1-10"]
    ui._UserInterface__ask_vacancies_details()  # type: ignore[attr-defined]
    assert ui.user_response() == {"action": "show vacancies details", "indices": "1-10"}
    input_values = ["2", ""]
    ui._UserInterface__ask_vacancies_details()  # type: ignore[attr-defined]
    assert ui.user_response() == {}


def test_set_area() -> None:
    ui = UserInterface()
    ui._UserInterface__set_area()  # type: ignore[attr-defined]
    assert ui._UserInterface__current_menu.caption == "Как вы хотите указать регион?"  # type: ignore[attr-defined]


def test_show_areas_ierarchy() -> None:
    ui = UserInterface()
    ui._UserInterface__show_areas_ierarchy()  # type: ignore[attr-defined]
    assert ui.user_response() == {"action": "show area ierarchy"}


def test_show_subareas() -> None:
    global input_values
    ui = UserInterface()
    src.user_interface_class.input = mock_input  # type: ignore[attr-defined]
    input_values = ["32"]
    ui._UserInterface__show_subareas()  # type: ignore[attr-defined]
    assert ui.user_response() == {"action": "show subareas", "parent": "32"}


def test_set_min_salary() -> None:
    global input_values
    global output
    output = []
    ui = UserInterface()
    src.user_interface_class.input = mock_input  # type: ignore[attr-defined]
    src.user_interface_class.print = lambda s: output.append(s)  # type: ignore[attr-defined]
    input_values = ["wg3wgr", "1000"]
    ui._UserInterface__set_min_salary()  # type: ignore[attr-defined]
    assert ui.user_response() == {"action": "set min salary", "salary": 1000} and (
            output[1] == "Введите целое число"
    )


def test_set_search_without_salary_param() -> None:
    global input_values
    ui = UserInterface()
    src.user_interface_class.input = mock_input  # type: ignore[attr-defined]
    input_values = ["1"]
    ui._UserInterface__set_search_without_salary_param()  # type: ignore[attr-defined]
    assert ui.user_response() == {
        "action": "set search without salary param",
        "value": True,
    }


def test_save_vacancies_to_file() -> None:
    par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
    data_dir = os.path.join(par_dir, "data")
    global input_values
    ui = UserInterface()
    src.user_interface_class.input = mock_input  # type: ignore[attr-defined]
    input_values = ["test6.json", "1"]
    ui._UserInterface__save_vacancies_to_file()  # type: ignore[attr-defined]
    assert ui.user_response() == {
        "action": "save vacancies to file",
        "dir": data_dir,
        "filename": "test6.json",
        "filetype": "3",
        "append": True,
    }
    ui.clear_user_response()
    input_values = [""]
    ui._UserInterface__save_vacancies_to_file()  # type: ignore[attr-defined]
    assert ui.user_response() == {}
    input_values = ["test6.csv", "2"]
    ui._UserInterface__save_vacancies_to_file()  # type: ignore[attr-defined]
    assert ui.user_response() == {
        "action": "save vacancies to file",
        "dir": data_dir,
        "filename": "test6.csv",
        "filetype": "2",
        "append": False,
    }
    ui.clear_user_response()
    output: list = []
    input_values = ["test.txt", "2"]
    ui._UserInterface__save_vacancies_to_file()  # type: ignore[attr-defined]
    assert ui.user_response() == {
        "action": "save vacancies to file",
        "dir": data_dir,
        "filename": "test.txt",
        "filetype": "1",
        "append": False,
    }
    ui.clear_user_response()
    output = []
    src.user_interface_class.print = lambda s: output.append(s)  # type: ignore[attr-defined]
    input_values = ["test6", "sh.csv", "3"]
    ui._UserInterface__save_vacancies_to_file()  # type: ignore[attr-defined]
    assert (
                   (output[1] == "Желаемый формат для сохранения файла не определен.")
                   and (output[2] == "Укажите имя файла с расширением через точку")
           ) and (ui.user_response() == {})


def test_delete_vacancies() -> None:
    global input_values
    ui = UserInterface()
    src.user_interface_class.input = mock_input  # type: ignore[attr-defined]
    input_values = ["1"]
    ui._UserInterface__delete_vacancies()  # type: ignore[attr-defined]
    assert ui.user_response() == {"action": "delete vacancies", "indices": "1"}


def test_top_n_vacancies() -> None:
    global input_values
    ui = UserInterface()
    output = []
    src.user_interface_class.input = mock_input  # type: ignore[attr-defined]
    src.user_interface_class.print = lambda s: output.append(s)  # type: ignore[attr-defined]
    input_values = ["erehg4", "10"]
    ui._UserInterface__top_n_vacancies()  # type: ignore[attr-defined]
    assert (ui.user_response() == {"action": "show top", "count": 10}) and (
            output == ["Введите целое число"]
    )


def test_show_all_professions_sorted_by_name() -> None:
    ui = UserInterface()
    ui._UserInterface__show_all_professions_sorted_by_name()  # type: ignore[attr-defined]
    assert ui.user_response() == {"action": "show all professions sorted by name"}


def test_shrink_main_menu() -> None:
    ui = UserInterface()
    ui.extend_main_menu()
    ui.shrink_main_menu()
    main_menu = ui._UserInterface__menus["main_menu"]  # type: ignore[attr-defined]
    items = str(main_menu).split("\n")
    assert items == ['1. Изменить параметры поиска',
                     '2. Искать вакансии',
                     '3. Работать с базой данных',
                     '4. Загрузить вакансии из файла',
                     '5. Выйти из программы.',
                     '',
                     '']


def test_ask_for_brief_vacancies_list() -> None:
    ui = UserInterface()
    ui.ask_for_brief_vacancies_list()
    assert ui.user_response() == {"action": "show vacancies list"}


def test_clear_user_response() -> None:
    ui = UserInterface()
    ui.clear_user_response()
    assert ui.user_response() == {}
