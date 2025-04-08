from src.vacancy_class import Vacancy


def test___init__(class_vacancy_fixture: Vacancy) -> None:
    vacancy = class_vacancy_fixture
    fields = vacancy.fields()
    assert (
        fields["id"] == "118765012" and (not fields["premium"]) and fields["name"]
    ) == "Руководитель организации (строительство)"


def test___str__(class_vacancy_fixture: Vacancy) -> None:
    vacancy = class_vacancy_fixture
    s = str(vacancy)
    print(s)
    assert (
        s
        == "Вакансия: Руководитель организации (строительство); Зарплата от: 400000 руб. на руки; "
        + "Регион: Иваново (Ивановская область); "
        + "Работодатель: ОПОРА; Требуемый опыт: Более 6 лет; Ссылка: https://hh.ru/vacancy/118765012; "
    )


def test_to_dict(class_vacancy_fixture: Vacancy) -> None:
    vacancy = class_vacancy_fixture
    to_dict = vacancy.to_dict()
    data = to_dict.get("_Vacancy__fields")
    fields = vacancy.fields()
    assert data == fields


def test_salary_specified(class_vacancy_fixture: Vacancy) -> None:
    vacancy = class_vacancy_fixture
    assert vacancy.salary_specified()


def test___eq__(class_vacancy_fixture: Vacancy) -> None:
    vacancy = class_vacancy_fixture
    assert int(vacancy) == 400000


def test___ne__(class_vacancy_fixture: Vacancy) -> None:
    vacancy = class_vacancy_fixture
    assert int(vacancy) != 0


def test___gt__(class_vacancy_fixture: Vacancy) -> None:
    vacancy = class_vacancy_fixture
    assert int(vacancy) > 0  # type: ignore[operator]


def test___ge__(class_vacancy_fixture: Vacancy) -> None:
    vacancy = class_vacancy_fixture
    assert int(vacancy) >= 400000  # type: ignore[operator]


def test___lt__(class_vacancy_fixture: Vacancy) -> None:
    vacancy = class_vacancy_fixture
    assert int(vacancy) < 500000  # type: ignore[operator]


def test___le__(class_vacancy_fixture: Vacancy) -> None:
    vacancy = class_vacancy_fixture
    assert int(vacancy) < 500000  # type: ignore[operator]


def test___int__(class_vacancy_fixture: Vacancy) -> None:
    vacancy = class_vacancy_fixture
    assert int(vacancy) == 400000


def test_details(class_vacancy_fixture: Vacancy) -> None:
    vacancy = class_vacancy_fixture
    d = vacancy.details()
    assert (
        d
        == """id: 118765012
Ссылка: https://hh.ru/vacancy/118765012
Вакансия: Руководитель организации (строительство)
Зарплата от: 400000
Валюта зарплаты: руб.
Работодатель: ОПОРА
Требуемый опыт: Более 6 лет
Требования: Опыт работы в строительной компании в должности Генерального директора не менее 5 лет.
Обязанности: Выстраивание эффективной структуры Компании . Опыт работы с Госзаказами (обязательно).
Занятость: Полная
Регион: Иваново (Ивановская область)
Адрес: Иваново, Лежневская улица, 55
Дата публикации: 25 March 2025
Вид работы: На месте работодателя
Профессия: Руководитель строительного проекта\n"""
    )


def test_fields(class_vacancy_fixture: Vacancy) -> None:
    vacancy = class_vacancy_fixture
    fields = vacancy.fields()
    assert (
        fields["id"] == "118765012" and (not fields["premium"]) and fields["name"]
    ) == "Руководитель организации (строительство)"


def test_default(class_vacancy_fixture: Vacancy) -> None:
    vacancy1 = class_vacancy_fixture
    vacancy2 = class_vacancy_fixture
    to_dict = vacancy1.to_dict()
    default = vacancy1.default(vacancy2)
    assert to_dict == default


def test_gross(class_vacancy_gross_salary_fixture: Vacancy) -> None:
    assert (
        class_vacancy_gross_salary_fixture.properties.get("salary", {}).get(
            "suffix", ""
        )
        == "до вычета"
    )


# def test_no_salary(class_vacancy_no_salary_fixture) -> None:
#     assert True
