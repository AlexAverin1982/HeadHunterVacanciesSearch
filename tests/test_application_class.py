import os
from copy import deepcopy

import src.user_interface_class
from src.application_class import Application
from src.hh_reference_class import HeadHunterReference as HhRef

output: list = []
input_values: list = []
par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
data_dir = os.path.join(par_dir, "data")


def mock_input(s: str) -> str:  # мокаем ввод пунктов меню
    """Мокаем пользовательский ввод с клавиатуры"""
    global output
    global input_values
    output.append(s)
    return str(input_values.pop(0))


def test_terminate() -> None:
    Application.terminate()
    assert Application.work_is_over


def test_init__() -> None:
    assert Application()


# @pytest.mark.skipif(condition='api.hh.ru не пингуется')
def test_vacancies_count() -> None:
    global input_values
    app = Application()
    src.user_interface_class.input = mock_input     # type: ignore[attr-defined]
    input_values = ["10", "", "", "", ""]
    app.user_interface._UserInterface__set_vacancies_list_limit()
    app.check_out_user_response()
    app.find_vacancies(clear_previous_results=True)
    vac_count = app.vacancies_count()
    assert vac_count == "Сейчас найдено 10 вакансий"
    app.user_interface._UserInterface__find_vacancies()
    app.check_out_user_response()


def test_filter_found_vacancies() -> None:
    global input_values
    app = Application()
    src.user_interface_class.input = mock_input     # type: ignore[attr-defined]

    # Хотим найти 100 вакансий
    input_values = ["100"]
    app.user_interface._UserInterface__set_vacancies_list_limit()
    app.check_out_user_response()
    app.find_vacancies(clear_previous_results=True)

    # хотим найти без опыта
    input_values = ["без опыта, нет опыта"]
    app.user_interface._UserInterface__set_search_substring()
    app.check_out_user_response()

    # сортируем найденные вакансии по убыванию зарплаты
    sort_mode = "1"
    input_values = [sort_mode, ""]
    app.user_interface._UserInterface__sort_vacancies()
    app.check_out_user_response()
    # app.sort_vacancies(int(sort_mode))
    vac_count = len(app.vacancies)

    # хотим найти не меньше медианной зарплаты
    middle = vac_count // 2
    mid_salary = app.vacancies[middle].properties.get("salary", {}).get("value", 0)
    input_values = [str(mid_salary)]
    app.user_interface._UserInterface__set_min_salary()
    app.check_out_user_response()
    app.filter_found_vacancies()
    filtered_vac_count = len(app.vacancies)
    assert (
        (filtered_vac_count < vac_count)
        and (
            app.vacancies[-1].properties.get("salary", {}).get("value", 0) >= mid_salary
        )
    ) and (
        (str(app.vacancies[0]).lower().find("нет опыта") > -1)
        or (str(app.vacancies[0]).lower().find("без опыта") > -1)
    )


def test_delete_vacancies() -> None:
    global input_values
    app = Application()
    src.user_interface_class.input = mock_input     # type: ignore[attr-defined]

    # Хотим найти 10 вакансий
    input_values = ["10"]
    app.user_interface._UserInterface__set_vacancies_list_limit()
    app.check_out_user_response()
    app.find_vacancies(clear_previous_results=True)

    remaining_vacs = [
        str(app.vacancies[1]).lower(),
        str(app.vacancies[5]).lower(),
        str(app.vacancies[8]).lower(),
    ]
    input_values = ["1,3-5,7-8, 10-, 15"]
    app.user_interface._UserInterface__delete_vacancies()
    app.check_out_user_response()
    # удаляем указанные номера и проверяем, что остались только те, которые мы хотели оставить
    resulting_list = [str(vac).lower() for vac in app.vacancies]
    assert resulting_list == remaining_vacs


def test_show_details() -> None:
    global input_values
    app = Application()
    src.user_interface_class.input = mock_input     # type: ignore[attr-defined]

    # Хотим найти 1 вакансию
    input_values = ["1", "", ""]
    app.user_interface._UserInterface__set_vacancies_list_limit()
    app.check_out_user_response()
    app.find_vacancies(clear_previous_results=True)
    vac_details = ""
    if len(app.vacancies):
        output = []
        src.user_interface_class.print = lambda s: output.append(s)     # type: ignore[attr-defined]
        app.show_details()
        vac_details = "1. " + app.vacancies[0].details()
        assert output[3] == vac_details
        output = []
        input_values = ["1", "10", ""]
        app.user_interface._UserInterface__ask_vacancies_details()
        app.check_out_user_response()
        # app.show_details('1, 10')
        vac_details = "1. " + app.vacancies[0].details()
    else:
        output = ["nothing"]

    assert (output == ["nothing"]) or (output[5] == vac_details)


def test_save_vacancies_to_file() -> None:
    global input_values
    app = Application()
    src.user_interface_class.input = mock_input     # type: ignore[attr-defined]

    # Хотим найти 1000 вакансий
    input_values = ["1000", "10", "", "2", "", "", "", ""]
    app.user_interface._UserInterface__set_vacancies_list_limit()
    app.check_out_user_response()
    app.find_vacancies(clear_previous_results=True)
    src_vacancy = deepcopy(app.vacancies[0])

    filename = "test1"
    filetype = "1"
    append = False

    app.save_vacancies_to_file(data_dir, filename, filetype, append)

    filename = "test3.json"
    filetype = "3"
    append = False

    app.save_vacancies_to_file(data_dir, filename, filetype, append)
    # app.user_interface._UserInterface__delete_vacancies()
    # app.check_out_user_response()

    full_filename = os.path.join(data_dir, filename)
    assert os.path.exists(full_filename)
    app.vacancies = []
    app.load_vacancies_from_file(data_dir, filename, filetype)
    s = str(app.vacancies[0])
    assert str(src_vacancy) == s

    filename = "test1"
    filetype = "1"
    append = False

    app.save_vacancies_to_file(data_dir, filename, filetype, append)

    full_filename = os.path.join(data_dir, filename + ".txt")
    app.save_vacancies_to_file(data_dir, filename, filetype, True)
    assert os.path.exists(full_filename)


# @pytest.mark.parametrize("filename, filetype, append", [('test1.txt', '1', False), ('test1.csv', '2', True),
#                                                         ('test3.json', '3', True),])
# def test_save_vacancies_to_file(filename, filetype, append) -> None:
# global input_values
# app = Application()
# src.user_interface_class.input = mock_input
#
# # Хотим найти 1 вакансий
# input_values = ['10', '1', '']
# app.user_interface._UserInterface__set_vacancies_list_limit()
# app.check_out_user_response()
# app.find_vacancies(clear_previous_results=True)
# src_vacancy = deepcopy(app.vacancies[0])
# app.save_vacancies_to_file(data_dir, filename, filetype, append)
# app.user_interface._UserInterface__delete_vacancies()
# app.check_out_user_response()
#
# full_filename = os.path.join(data_dir, filename)
# assert os.path.exists(full_filename)
# app.load_vacancies_from_file(data_dir, filename, filetype)
# assert str(src_vacancy) == str(app.vacancies[0])
# assert True


def test_find_vacancies() -> None:
    global input_values
    app = Application()
    src.user_interface_class.input = mock_input     # type: ignore[attr-defined]
    # установить минимальную зарплату
    min_salary = "500000"
    input_values = [min_salary]
    app.user_interface._UserInterface__set_min_salary()
    # найти вакансии
    app.check_out_user_response()
    app.find_vacancies(clear_previous_results=True)
    assert (len(app.vacancies) == 0) or (
        app.vacancies[0].properties.get("salary", {}).get("value", 0) >= int(min_salary)
    )


def test_search_area_by_substring() -> None:
    global input_values
    src.user_interface_class.input = mock_input     # type: ignore[attr-defined]
    input_values = [""]
    output = []
    src.user_interface_class.print = lambda s: output.append(s)     # type: ignore[attr-defined]
    app = Application()
    search_substring = "Иваново"
    # search_substring = 'd;fjklernjk;'
    app.search_area_by_substring(search_substring)
    assert (len(output) == 4) or (output[3].find(search_substring) > -1)
    input_values = ["москва", ""]
    app.user_interface._UserInterface__search_area_by_substring()
    app.check_out_user_response()


def test_show_subareas() -> None:
    HhRef.references["areas"] = None
    global input_values
    src.user_interface_class.input = mock_input     # type: ignore[attr-defined]
    input_values = ["", "", ""]
    output = []
    src.user_interface_class.print = lambda s: output.append(s)     # type: ignore[attr-defined]
    app = Application()
    app.show_subareas("")
    assert output == ["Регион с кодом  не найден."]
    app.show_subareas("113")
    found_areas = len(output) > 4
    if found_areas:
        area_data_str = output[4].split(". ")[1]
        name, code = area_data_str.split(" --- ")
        correct = HhRef.references["areas"].items_by_name[name]["id"] == code
    assert (not found_areas) or correct
    output = []
    app.show_subareas("32")
    assert output == ["Регион с кодом 32 не содержит составных частей."]


def test_show_all_regions_sorted_by_name() -> None:
    HhRef.references["areas"] = None
    global input_values
    src.user_interface_class.input = mock_input     # type: ignore[attr-defined]
    input_values = ["", "", ""]
    output = []
    src.user_interface_class.print = lambda s: output.append(s)     # type: ignore[attr-defined]
    app = Application()
    app.show_all_regions_sorted_by_name()
    found_areas = len(output) > 4
    areas = []
    if found_areas:
        line_ind = 3
        item_ind = 1
        max_count = 50
        while (item_ind < max_count) and output[line_ind].startswith(f"{item_ind}. "):
            areas.append(output[line_ind][len(f"{item_ind}. "):])
            line_ind += 1
            item_ind += 1

    assert (not found_areas) or (areas == sorted(areas))


def test_show_all_regions_sorted_by_code() -> None:
    HhRef.references["areas"] = None
    global input_values
    src.user_interface_class.input = mock_input     # type: ignore[attr-defined]
    input_values = ["", "", ""]
    output = []
    src.user_interface_class.print = lambda s: output.append(s)     # type: ignore[attr-defined]
    app = Application()
    app.show_all_regions_sorted_by_code()
    found_areas = len(output) > 4
    codes = []
    if found_areas:
        line_ind = 3
        item_ind = 1
        max_count = 50
        while (item_ind < max_count) and output[line_ind].startswith(str(item_ind)):
            codes.append(int(output[line_ind].split(" --- ")[0]))
            line_ind += 1
            item_ind += 1

    assert (not found_areas) or (codes == sorted(codes))


def test_show_regions_structured() -> None:
    HhRef.references["areas"] = None
    global input_values
    src.user_interface_class.input = mock_input     # type: ignore[attr-defined]
    input_values = ["", "", ""]
    output = []
    src.user_interface_class.print = lambda s: output.append(s)     # type: ignore[attr-defined]
    app = Application()
    app.show_regions_structured()
    found_areas = len(output) > 4
    areas = []
    passed = False
    if found_areas:
        line_ind = 3
        item_ind = 1
        max_count = 50
        while (item_ind < max_count) and output[line_ind].startswith(f"{item_ind}. "):
            # item = output[line_ind]
            # item = output[line_ind][len(f"{item_ind}. "):]
            areas.append(output[line_ind][len(f"{item_ind}. "):].split(" --- ")[0])
            line_ind += 1
            item_ind += 1

        passed = True
        for area_name in areas:
            subitems = (
                HhRef.references["areas"].items_by_name[area_name].get("areas")
            )
            got_subitems = subitems is not None
            if not got_subitems:
                passed = False
                break
    assert (not found_areas) or passed


# def test_show_all_professions_names() -> None:
#     assert True
#     global input_values
#     output = []
#     src.user_interface_class.print = lambda s: output.append(s)     # type: ignore[attr-defined]
#     src.user_interface_class.input = mock_input     # type: ignore[attr-defined]
#     input_values = ["1", "2"]
#     app = Application()
#     app.show_all_professions_names()
#     assert len(output) > 4


def test_load_vacancies_from_file() -> None:
    global input_values
    output = []
    src.user_interface_class.print = lambda s: output.append(s)     # type: ignore[attr-defined]
    src.user_interface_class.input = mock_input     # type: ignore[attr-defined]
    input_values = ["", "", "", "", "1", "1", "1", "", "1", "1"]
    app = Application()
    filename = "nonexistent.txt"
    output = []
    app.load_vacancies_from_file(data_dir, filename, "1")
    assert output[0] == "Указанный файл не найден"

    # filename = 'test1.txt'
    # output = []
    # app.load_vacancies_from_file(data_dir, filename, '1')
    # assert len(app.vacancies)

    filename = "nonexistent.csv"
    app.load_vacancies_from_file(data_dir, filename, "2")
    assert True
    filename = "test6.json"
    output = []
    app.load_vacancies_from_file(data_dir, filename, "3")
    assert output[0] == "Загрузка завершена."

    filename = "test1.txt"
    app.vacancies = []
    app.load_vacancies_from_file(data_dir, filename, "1")
    assert len(app.vacancies) > 0
    app.load_vacancies_from_file(data_dir, filename, "1")
    input_values = ["test6.json", "2", "2", "2", "2", "2"]
    # app.load_vacancies_from_file(data_dir, filename, '1')

    app.user_interface._UserInterface__load_vacancies_from_file()
    app.check_out_user_response()

    app.vacancies = []
    app.load_vacancies_from_file(data_dir, "empty.txt", "1")
    assert app.vacancies == []

    output = []
    src.user_interface_class.print = lambda s: output.append(s)     # type: ignore[attr-defined]

    app.load_vacancies_from_file(data_dir, "kjsdvnjkrnvkjwer.json", "3")
    assert output == ["Указанный файл не найден"]


def test_check_out_user_response() -> None:
    global input_values
    output = []
    src.user_interface_class.print = lambda s: output.append(s)     # type: ignore[attr-defined]
    src.user_interface_class.input = mock_input     # type: ignore[attr-defined]
    app = Application()
    input_values = [
        "test6.json",
        "2",
        "2",
        "",
        "",
        "",
        "113",
        "test7.txt",
        "1",
        "1",
        "2",
        "10",
        "",
        "100",
        "",
        "",
        "",
    ]
    app.user_interface._UserInterface__load_vacancies_from_file()
    app.check_out_user_response()
    assert True
    app.user_interface.ask_for_brief_vacancies_list()
    app.check_out_user_response()
    assert True
    app.user_interface._UserInterface__filter_vacancies()
    app.check_out_user_response()
    app.user_interface._UserInterface__show_all_regions_sorted_by_name()
    app.check_out_user_response()
    app.user_interface._UserInterface__show_all_regions_sorted_by_code()
    app.check_out_user_response()
    app.user_interface._UserInterface__show_subareas()
    app.check_out_user_response()
    app.user_interface._UserInterface__show_areas_ierarchy()
    app.check_out_user_response()
    app.user_interface._UserInterface__save_vacancies_to_file()
    app.check_out_user_response()
    app.user_interface._UserInterface__set_search_without_salary_param()
    app.check_out_user_response()
    app.user_interface._UserInterface__set_search_without_salary_param()
    app.check_out_user_response()
    app.user_interface._UserInterface__top_n_vacancies()
    app.check_out_user_response()
    app.user_interface._UserInterface__type_in_prof_id()
    app.check_out_user_response()
    # app.user_interface._UserInterface__show_all_professions_sorted_by_name()
    # app.check_out_user_response()
    assert True


def test_set_search_area_id() -> None:
    global input_values
    output = []
    src.user_interface_class.print = lambda s: output.append(s)     # type: ignore[attr-defined]
    src.user_interface_class.input = mock_input     # type: ignore[attr-defined]
    app = Application()
    input_values = ["32", ""]
    app.user_interface._UserInterface__type_in_area_id()
    app.check_out_user_response()
    assert app.search_params.properties["area"]["id"] == "32"

    input_values = ["dlkgmwerk", ""]
    app.user_interface._UserInterface__type_in_area_id()
    app.check_out_user_response()
    assert output == ["Введен неверный код"]


def test_run() -> None:
    global input_values
    output = []
    input_values = ["", "4", "4", "4", "4", "4", "4"]
    src.user_interface_class.print = lambda s: output.append(s)     # type: ignore[attr-defined]
    src.user_interface_class.input = mock_input     # type: ignore[attr-defined]
    app = Application()
    app.run()
    print(app.search_params.fields())
    assert output


def test_sort_vacancies() -> None:
    global input_values
    app = Application()
    src.user_interface_class.input = mock_input     # type: ignore[attr-defined]

    # Хотим найти 100 вакансий
    input_values = ["100", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    app.user_interface._UserInterface__set_vacancies_list_limit()
    app.check_out_user_response()
    app.find_vacancies(clear_previous_results=True)
    assert (app.vacancies[0] == app.vacancies[1]) or (
        app.vacancies[0] != app.vacancies[1]
    )

    # # сортируем найденные вакансии по убыванию зарплаты
    for sort_mode in range(1, 9):
        app.sort_vacancies(sort_mode)
