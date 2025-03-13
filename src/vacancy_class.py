from typing_extensions import Self

from src.recordset_class import RecordSet


class Vacancy(RecordSet):
    def __init__(self, fields: dict):
        super().__init__()

        salary = ''
        salary_max = ''
        salary_desc = ''

        salary_data = fields.get('salary', {})
        if salary_data:
            if isinstance(salary_data, dict):
                salary = salary_data.get('from', '')
                salary_desc = salary_data.get('gross', True)
                if salary_desc:
                    salary_desc = 'до вычета'
                salary_max = salary_data.get('to', '')
            else:
                print(salary_data)

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


        snippet = fields.get('snippet', {})
        contacts = fields.get('contacts', {})
        professional_roles = fields.get('professional_roles')
        if professional_roles:
            professional_role = professional_roles[0]
        else:
            professional_role = {}
        # print(salary)

        address = fields.get('address', {})
        if isinstance(address, dict):
            address = address.get('raw', '')
        else:
            address = ''

        self.properties.update({'id': {'value': fields.get('id', '')},
                                'area': {'id': fields.get('area', {}).get('id', ''),
                                         'value': fields.get('area', {}).get('name', ''),
                                         'representation': 'Регион'},
                                'name': {'value': fields.get('name', ''),
                                         'representation': 'Вакансия'},
                                'has_test': {'value': fields.get('has_test', False),
                                             'representation': 'Наличие испытательного срока'},
                                'url': {'value': fields.get('alternate_url', ''),
                                        'representation': 'Ссылка'},
                                'address': {'value': address,
                                            'representation': 'Адрес'},
                                'salary': {'value': salary,
                                               'representation': 'Зарплата от',
                                               'suffix': salary_desc},
                                'salary_max': {'value': salary_max,
                                               'representation': 'до',},
                                'published_at': {'value': fields.get('published_at', ''),
                                                 'representation': 'Дата публикации'},
                                'archived': {'value': fields.get('archived', False),
                                             'representation': 'Находится в архиве'},
                                'employer': {'id': fields.get('employer', {}).get('id', ''),
                                             'value': fields.get('employer', {}).get('name', ''),
                                             'representation': 'Работодатель'},
                                'requirement': {'value': snippet.get('requirement', ''),
                                                'representation': 'Требования'},
                                'responsibility': {'value': snippet.get('responsibility', ''),
                                                   'representation': 'Обязанности'},
                                # 'schedule': {'value', fields.get('schedule', {}).get('name', ''),
                                #              'representation': ''},
                                # 'work_format': {'value': fields.get('work_format', {}).get('name', '')},
                                # 'working_hours': {'value': fields.get('working_hours', {}).get('name', '')},
                                # 'working_schedule_by_days': {
                                #     'value': fields.get('working_schedule_by_days', {}).get('name', '')},
                                # 'employment_form': {'value': fields.get('employment_form', {}).get('name', '')},
                                'experience': {'value': fields.get('experience', {}).get('name', ''),
                                               'representation': 'Требуемый опыт'},
                                # 'professional_role': professional_role.get('name', '')
                                })

        self.display_props = ['name', 'salary', 'employer', 'experience', 'url']
        # if isinstance(fields, dict):
        # self.id: str = fields.get('id', '')
        # self.name: str = fields.get('name', '')
        # self.has_test: bool = fields.get('has_test', False)
        # self.url = fields.get('alternate_url', '')

        # area = fields.get('area', {})
        # self.area: str = area.get('name', 'не указано')
        """
        self.salary = fields.get('salary', {})
        self.publish_date: str = fields.get('published_at')
        snippet = fields.get('snippet', {})
        self.description = snippet.get('requirement')
        self.duty = snippet.get('responsibility')
        schedule = fields.get('schedule', {})
        self.job_type = schedule.get('name', {})
        self.experience = fields.get('experience', {}).get('name', 'не имеет значения').lower()
        self.employer = fields.get('employer', {}).get('name', 'не указан')
        """
    def __str__(self):
        result = ""

        for property_name in self.display_props:
            if property_name not in self.properties.keys():
                continue
            prop = self.properties[property_name]
            val = str(prop.get('value', ''))
            if val == '':
                continue
            if prop.get('representation'):
                result += f"{prop['representation']}: "
                # val = str(prop.get('value', 'значение не указано'))
                    # val = 'значение не указано'
                result += val
                result += f" {prop.get('suffix', '')}; "

        return result.replace(' ; ', '; ')

    def salary_specified(self) -> bool:
        # return self.properties.get('salary', {}).get('value', '') != ''
        return self != 0

    def __eq__(self, other: Self | int) -> bool:
        self_salary = self.properties.get('salary', {}).get('value', 0)
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
        if isinstance(other, Vacancy):
            other_salary = other.properties.get('salary', {}).get('value', 0)
        elif isinstance(other, int):
            other_salary = other
        else:
            other_salary = -1
        return self_salary <= other_salary

    def __le__(self, other: Self) -> bool:
        return self.__eq__(other) or self.__lt__(other)
