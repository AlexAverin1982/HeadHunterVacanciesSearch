import os

import pytest

from src.json_file_manager import JSONFileManager
from src.misc_tools import get_indices, vacancy_complies
from src.text_file_manager_class import TextFileManager
from src.vacancy_class import Vacancy


@pytest.mark.parametrize(
    "indices_str, items_count, expected_list",
    [
        ("-2, 5", 10, [0, 1, 4]),
        ("dfverbvebe", 0, []),
        ("dfverbvebe-", 10, []),
        ("-dfverbvebe-", 0, []),
    ],
)
def test_get_indices(indices_str: str, items_count: int, expected_list: list) -> None:
    """
    Функция возвращает список индексов как расшифровка строки, где через запятую и тире указаны нужные номера
    :param indices_str: строка, где указаны номера (не индексы, первый номер равен 1!) через запятую и тире
    :param items_count: количество элементов индексируемой коллекции для контроля границ
    """
    result = get_indices(indices_str, items_count)
    assert result == expected_list


@pytest.mark.parametrize(
    "filename, conditions, expected_result",
    [
        (
            "test1.txt",
            {"page": 10, "per_page": 10, "text": {"value": "^1"}},
            [True, True],
        ),
        ("test1.txt", {"text": {"value": "djkvnwerjvnwer"}}, []),
        ("test1.txt", {"text": {"value": "Краснодар"}}, [False]),
        ("test1.txt", {"some_key": {"value": "nomatter"}}, []),
        ("test6.json", {"area": {"id": "+++"}}, [False]),
        ("test6.json", {"salary": {"from": 100000}}, [True, True]),
    ],
)
def test_vacancy_complies(
    filename: str, conditions: dict, expected_result: list[bool]
) -> None:
    """
    Соответствие вакансии условиям
    param vac_data: свойства вакансии
    param conditions: условия для анализа
    param fail_if_none: True: если свойство условия в вакансии не указано, вакансия считается неподходящей
    :return: True - вакансия соответствует условиям или лучше
    """
    par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
    data_dir = os.path.join(par_dir, "data")

    fails_if_none = True
    vacancies_data: list = []
    result: list = []

    if filename.endswith(".txt"):
        file_manager = TextFileManager(storage_name=filename, working_dir=data_dir)

        # conditions = {"page": 10, "per_page": 10, "text":{"value": "^1"}}
        vacancies_data = file_manager.load(conditions, fails_if_none)  # type: ignore[assignment]
        if vacancies_data:
            vacancies_data = [
                Vacancy.validate_fields(raw_item) for raw_item in vacancies_data
            ][: len(expected_result)]
    elif filename.endswith(".json"):
        file_manager = JSONFileManager(  # type: ignore[assignment]
            storage_name=filename, working_dir=data_dir, method=Vacancy.to_dict
        )
        file_manager.filter_method = vacancy_complies  # type: ignore[attr-defined]
        vacancies = file_manager.load(conditions, fails_if_none)

        # vacancies_data = []
        # for vac in vacancies:
        #     vacancies_data.append(vac.fields())

        vacancies_data = [vac.fields() for vac in vacancies][: len(expected_result)]  # type: ignore[union-attr]
    #
    #
    if vacancies_data:
        result = [
            vacancy_complies(vac_data, conditions, False) for vac_data in vacancies_data
        ]

    assert (not result) or (result == expected_result)
