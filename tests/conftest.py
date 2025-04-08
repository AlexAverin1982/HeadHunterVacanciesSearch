import pytest

from src.user_interface_class import UserInterface
from src.vacancy_class import Vacancy

data = {
    "id": "118765012",
    "premium": False,
    "name": "Руководитель организации (строительство)",
    "department": None,
    "has_test": False,
    "response_letter_required": False,
    "area": {
        "id": "32",
        "name": "Иваново (Ивановская область)",
        "url": "https://api.hh.ru/areas/32",
    },
    "salary": {"from": 400000, "to": None, "currency": "RUR", "gross": False},
    "salary_range": {
        "from": 400000,
        "to": None,
        "currency": "RUR",
        "gross": False,
        "mode": {"id": "MONTH", "name": "За месяц"},
        "frequency": {"id": "TWICE_PER_MONTH", "name": "Два раза в месяц"},
    },
    "type": {"id": "open", "name": "Открытая"},
    "address": {
        "city": "Иваново",
        "street": "Лежневская улица",
        "building": "55",
        "lat": 56.983019,
        "lng": 40.982149,
        "description": None,
        "raw": "Иваново, Лежневская улица, 55",
        "metro": None,
        "metro_stations": [],
        "id": "6542581",
    },
    "response_url": None,
    "sort_point_distance": None,
    "published_at": "2025-03-25T13:20:22+0300",
    "created_at": "2025-03-25T13:20:22+0300",
    "archived": False,
    "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=118765012",
    "insider_interview": None,
    "url": "https://api.hh.ru/vacancies/118765012?host=hh.ru",
    "alternate_url": "https://hh.ru/vacancy/118765012",
    "relations": [],
    "employer": {
        "id": "4083024",
        "name": "ОПОРА",
        "url": "https://api.hh.ru/employers/4083024",
        "alternate_url": "https://hh.ru/employer/4083024",
        "logo_urls": None,
        "vacancies_url": "https://api.hh.ru/vacancies?employer_id=4083024",
        "accredited_it_employer": False,
        "employer_rating": {"total_rating": "4.9", "reviews_count": 4},
        "trusted": True,
    },
    "snippet": {
        "requirement": "Опыт работы в строительной компании в должности Генерального директора не менее 5 лет.",
        "responsibility": "Выстраивание эффективной структуры Компании . Опыт работы с Госзаказами (обязательно).",
    },
    "show_contacts": False,
    "contacts": None,
    "schedule": {"id": "fullDay", "name": "Полный день"},
    "working_days": [],
    "working_time_intervals": [],
    "working_time_modes": [],
    "accept_temporary": False,
    "fly_in_fly_out_duration": [],
    "work_format": [{"id": "ON_SITE", "name": "На месте работодателя"}],
    "working_hours": [{"id": "HOURS_8", "name": "8 часов"}],
    "work_schedule_by_days": [{"id": "FIVE_ON_TWO_OFF", "name": "5/2"}],
    "night_shifts": False,
    "professional_roles": [{"id": "108", "name": "Руководитель строительного проекта"}],
    "accept_incomplete_resumes": False,
    "experience": {"id": "moreThan6", "name": "Более 6 лет"},
    "employment": {"id": "full", "name": "Полная занятость"},
    "employment_form": {"id": "FULL", "name": "Полная"},
    "internship": False,
    "adv_response_url": None,
    "is_adv_vacancy": False,
    "adv_context": None,
}

data_gross_true = {
    "id": "118765012",
    "premium": False,
    "name": "Руководитель организации (строительство)",
    "department": None,
    "has_test": False,
    "response_letter_required": False,
    "area": {
        "id": "32",
        "name": "Иваново (Ивановская область)",
        "url": "https://api.hh.ru/areas/32",
    },
    "salary": {"from": 400000, "to": None, "currency": "RUR", "gross": True},
}

data_no_salary_no_address = {
    "id": "118765012",
    "premium": False,
    "name": "Руководитель организации (строительство)",
    "department": None,
    "has_test": False,
    "response_letter_required": False,
    "area": {
        "id": "32",
        "name": "Иваново (Ивановская область)",
        "url": "https://api.hh.ru/areas/32",
    },
}


@pytest.fixture()
def class_vacancy_fixture() -> Vacancy:
    return Vacancy(data)


@pytest.fixture()
def class_vacancy_gross_salary_fixture() -> Vacancy:
    return Vacancy(data_gross_true)


@pytest.fixture()
def class_vacancy_no_salary_fixture() -> Vacancy:
    return Vacancy(data_no_salary_no_address)


@pytest.fixture()
def class_user_interface_fixture() -> UserInterface:
    return UserInterface()


# @pytest.fixture()
# def class_search_parameters_fixture() ->

"""
from src.classes import Category, LawnGrass, Order, Product, Smartphone


@pytest.fixture()
def class_product_fixture() -> Product:
    return Product(
        name="test_product", description="test_description", price=10.5, quantity=10
    )


@pytest.fixture()
def class_category_fixture() -> Category:
    return Category(name="test_category", description="test_description")


@pytest.fixture()
def three_products() -> list[Product]:
    prod1 = Product(name="prod1", quantity=10, price=100.0)
    prod2 = Product(name="prod2", quantity=10, price=100.0)
    prod3 = Product(name="prod3", quantity=10, price=100.0)
    return [prod1, prod2, prod3]


@pytest.fixture()
def class_smartphone_fixture() -> Smartphone:
    return Smartphone(
        name="test_smartphone",
        description="test_description",
        price=10.5,
        quantity=10,
        efficiency=1000.0,
        model="Iphone999",
        memory=9,
        color="black",
    )


@pytest.fixture()
def three_smartphones() -> list[Smartphone]:
    smartphone1 = Smartphone(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
        95.5,
        "S23 Ultra",
        256,
        "Серый",
    )
    smartphone2 = Smartphone(
        "Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space"
    )
    smartphone3 = Smartphone(
        "Xiaomi Redmi Note 11",
        "1024GB, Синий",
        31000.0,
        14,
        90.3,
        "Note 11",
        1024,
        "Синий",
    )
    return [smartphone1, smartphone2, smartphone3]


@pytest.fixture()
def grass_fixture() -> list[LawnGrass]:
    grass1 = LawnGrass(
        "Газонная трава",
        "Элитная трава для газона",
        500.0,
        20,
        "Россия",
        "7 дней",
        "Зеленый",
    )
    grass2 = LawnGrass(
        "Газонная трава 2",
        "Выносливая трава",
        450.0,
        15,
        "США",
        "5 дней",
        "Темно-зеленый",
    )
    return [grass1, grass2]


@pytest.fixture()
def class_lawngrass_fixture() -> LawnGrass:
    return LawnGrass(
        name="test_lawngrass",
        description="test_description",
        price=10.5,
        quantity=10,
        country="Россия",
        germination_period="1 год",
        color="black",
    )


@pytest.fixture()
def class_order_fixture(class_product_fixture: Product) -> Order:
    return Order(class_product_fixture, count=1)
"""
