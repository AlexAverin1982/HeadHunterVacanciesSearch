from datetime import datetime as datetime
from typing_extensions import Self, Any
from src.recordset_class import RecordSet
from copy import deepcopy

from json import JSONEncoder

class Vacancy(RecordSet):
    headers: list[str] = []

    def __init__(self, fields: dict):
        super().__init__()

        salary = ''
        salary_max = ''
        salary_desc = ''
        load_from_file_mode = False
        self.__fields: dict = deepcopy(fields)

        salary_data = self.__fields.get('salary', {})
        currency = 'руб.'
        if salary_data:
            if isinstance(salary_data, dict):
                if salary_data.get('from'):
                    salary = salary_data.get('from', 0)
                    salary_desc = salary_data.get('gross', True)
                    if salary_desc:
                        salary_desc = 'до вычета'
                    salary_max = salary_data.get('to', 0)
                    currency = salary_data.get('currency', 'руб.').replace('RUR', 'руб.')
                elif salary_data.get('addendum') and salary_data.get('representation'):
                    load_from_file_mode = True
            else:
                print(salary_data)

        if load_from_file_mode:
            self.properties.update(self.__fields)
        else:
            if (salary == 0) or (salary is None):
                salary = ''
            if (salary_max == 0) or (salary is None):
                salary_max = ''
            if (salary_desc is not None) and (str(salary) + str(salary_max)):
                if isinstance(salary_desc, bool):
                    if salary_desc:
                        salary_desc = 'до вычета'
                    else:
                        salary_desc = 'на руки'
                else:
                    salary_desc = ''
            else:
                salary_desc = ''

            snippet = self.__fields.get('snippet', {})
            contacts = self.__fields.get('contacts', {})
            professional_roles = self.__fields.get('professional_roles')
            if professional_roles:
                professional_role = professional_roles[0]
            else:
                professional_role = {}
            # print(salary)

            address = self.__fields.get('address', {})
            if isinstance(address, dict):
                address = address.get('raw', '')
            else:
                address = ''

            work_format = self.__fields.get('work_format')
            if work_format:
                if isinstance(work_format, list):
                    formats = [item['name'].replace('\xa0', ' ') for item in work_format]
                    work_format = {'name': ' или '.join(formats)}
                elif isinstance(work_format, dict):
                    pass
                    # if work_format.get('name'):
                    #     work_format = {'name': work_format['name']}
                else:
                    print(work_format)
            else:
                work_format = {}

            published_at = self.__fields.get('published_at', '')
            if published_at:
                try:
                    if isinstance(published_at, str):
                        p = published_at.find('T')
                        if p > 0:
                            published_at = {
                                'value': datetime.strftime(datetime.strptime(published_at[:p], '%Y-%m-%d'), '%d %B %Y')}
                        else:
                            print(published_at)
                    elif isinstance(published_at, dict):
                        pass
                    else:
                        print(published_at)
                except ValueError:
                    published_at = {}
            else:
                published_at = {}

            self.properties.update({'id': {'value': self.__fields.get('id', ''), 'display_order': 0},
                                    'area': {'id': self.__fields.get('area', {}).get('id', ''),
                                             'value': self.__fields.get('area', {}).get('name', ''),
                                             'representation': 'Регион'},
                                    'name': {'value': self.__fields.get('name', ''),
                                             'representation': 'Вакансия', 'display_order': 2},
                                    'has_test': {'value': self.__fields.get('has_test', False),
                                                 'representation': 'Наличие испытательного срока'},
                                    'url': {'value': self.__fields.get('alternate_url', ''),
                                            'representation': 'Ссылка', 'display_order': 1},
                                    'address': {'value': address,
                                                'representation': 'Адрес'},
                                    'salary': {'value': salary,
                                               'representation': 'Зарплата от',
                                               'addendum': 'currency',
                                               'suffix': salary_desc, 'display_order': 3},
                                    'salary_max': {'value': salary_max,
                                                   'representation': 'до',
                                                   'addendum': 'currency',
                                                   'display_order': 4},
                                    'currency': {'value': currency, 'representation': 'Валюта зарплаты',
                                                 'display_order': 4},
                                    'published_at': {'value': published_at.get('value', ''),
                                                     'representation': 'Дата публикации'},
                                    'archived': {'value': self.__fields.get('archived', False),
                                                 'representation': 'Находится в архиве'},
                                    'employer': {'id': self.__fields.get('employer', {}).get('id', ''),
                                                 'value': self.__fields.get('employer', {}).get('name', ''),
                                                 'representation': 'Работодатель', 'display_order': 5},
                                    'requirement': {'value': snippet.get('requirement', ''),
                                                    'representation': 'Требования',
                                                    'display_order': 7},
                                    'responsibility': {'value': snippet.get('responsibility', ''),
                                                       'representation': 'Обязанности',
                                                       'display_order': 8},
                                    # 'schedule': {'value', self.__fields.get('schedule', {}).get('name', ''),
                                    #              'representation': ''},
                                    'work_format': {'value': work_format.get('name', ''),
                                                    'representation': 'Вид работы'},
                                    # 'working_hours': {'value': self.__fields.get('working_hours', {}).get('name', '')},
                                    # 'working_schedule_by_days': {
                                    #     'value': self.__fields.get('working_schedule_by_days', {}).get('name', '')},
                                    'employment_form': {'value': self.__fields.get('employment_form', {}).get('name', ''),
                                                        'representation': 'Занятость',
                                                        'display_order': 9
                                                        },
                                    'experience': {'value': self.__fields.get('experience', {}).get('name', ''),
                                                   'representation': 'Требуемый опыт',
                                                   'display_order': 6},
                                    'professional_role': {'value': professional_role.get('name', ''),
                                                          'id': professional_role.get('id', ''),
                                                          'representation': 'Профессия'}
                                    })

        prop_names = self.properties.keys()
        prop_names = sorted(prop_names, key=lambda x: self.properties[x].get('display_order', 999))
        if len(prop_names) > len(Vacancy.headers):
            Vacancy.headers = prop_names

        self.display_props = ['name', 'salary', 'employer', 'experience', 'url']
        # if isinstance(self.__fields, dict):
        # self.id: str = self.__fields.get('id', '')
        # self.name: str = self.__fields.get('name', '')
        # self.has_test: bool = self.__fields.get('has_test', False)
        # self.url = self.__fields.get('alternate_url', '')

        # area = self.__fields.get('area', {})
        # self.area: str = area.get('name', 'не указано')
        """
        self.salary = self.__fields.get('salary', {})
        self.publish_date: str = self.__fields.get('published_at')
        snippet = self.__fields.get('snippet', {})
        self.description = snippet.get('requirement')
        self.duty = snippet.get('responsibility')
        schedule = self.__fields.get('schedule', {})
        self.job_type = schedule.get('name', {})
        self.experience = self.__fields.get('experience', {}).get('name', 'не имеет значения').lower()
        self.employer = self.__fields.get('employer', {}).get('name', 'не указан')
        """

    def __str__(self):

        result = ""

        for property_name in self.display_props:
            if property_name not in self.properties.keys():
                continue
            prop = self.properties[property_name]
            val = str(prop.get('value', ''))
            addendum = prop.get('addendum')
            if addendum:
                addendum = ' ' + str(self.properties[addendum].get('value', ''))
            if val == '':
                continue
            if prop.get('representation'):
                result += f"{prop['representation']}: "
                # val = str(prop.get('value', 'значение не указано'))
                # val = 'значение не указано'
                result += val
                if addendum:
                    result += addendum
                result += f" {prop.get('suffix', '')}; "

        return result.replace(' ; ', '; ')

    def to_dict(self) -> Any:
        all_dict = self.__dict__
        del all_dict['properties']
        del all_dict['display_props']
        return all_dict

    def salary_specified(self) -> bool:
        # return self.properties.get('salary', {}).get('value', '') != ''
        return self != 0

    def __eq__(self, other: Self | int) -> bool:
        self_salary = self.properties.get('salary', {}).get('value', 0)
        if self_salary == '':
            self_salary = 0
        if isinstance(other, Vacancy):
            other_salary = other.properties.get('salary', {}).get('value', 0)
        elif isinstance(other, int):
            other_salary = other
        else:
            other_salary = -1
        return self_salary == other_salary

    def __ne__(self, other: Self) -> bool:
        return not self.__eq__(other)

    def __gt__(self, other: Self) -> bool:
        self_salary = self.properties.get('salary', {}).get('value', 0)
        if isinstance(other, Vacancy):
            other_salary = other.properties.get('salary', {}).get('value', 0)
        elif isinstance(other, int):
            other_salary = other
        else:
            other_salary = -1
        return self_salary >= other_salary

    def __ge__(self, other: Self) -> bool:
        return self.__eq__(other) or self.__gt__(other)

    def __lt__(self, other) -> bool:
        self_salary = self.properties.get('salary', {}).get('value', 0)
        if (self_salary == '') or (self_salary == 0):
            return True
        if isinstance(other, Vacancy):
            other_salary = other.properties.get('salary', {}).get('value', 0)
        elif isinstance(other, int):
            other_salary = other
        else:
            other_salary = -1
        return self_salary <= other_salary

    def __le__(self, other: Self) -> bool:
        return self.__eq__(other) or self.__lt__(other)

    def __int__(self) -> int:
        result = self.properties.get('salary', {}).get('value', 0)
        if isinstance(result, int):
            return result
        else:
            return 0

    def details(self) -> str:
        result = ''
        prop_names = self.properties.keys()
        prop_names = sorted(prop_names, key=lambda x: self.properties[x].get('display_order', 999))
        for name in prop_names:
            representation = self.properties[name].get('representation')
            value = self.properties[name].get('value')
            if not value:
                continue
            if representation:
                result += f"{representation}: {value}\n"
            else:
                result += f"{name}: {value}\n"
        return result

    def fields(self) -> dict:
        return self.__fields

    def default(self, o):
        return o.__dict__
    # def as_xml(self) -> str:
    #     result = ''
    #     return result
    #
    # def as_json(self) -> str:
    #     result = ''
    #     return result
    #
    # def as_csv(self, separator: str = ';') -> str:
    #     result = []
    #     if Vacancy.headers:
    #         for prop_name in Vacancy.headers:
    #             result.append(str(self.properties.get(prop_name, {}).get('value', '')))
    #         result = separator.join(result)
    #     else:
    #         return ''
    #     return result

