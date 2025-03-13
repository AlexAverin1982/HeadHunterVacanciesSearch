from typing import Any
from src.hh_reference_class import HeadHunterReference as HhRef
from src.recordset_class import RecordSet


class SearchParameters(RecordSet):
    """
    Параметры поиска вакансий
    """

    # def reset(self) -> None:
    # self.__area: int = 113  # whole Russia регион поиска
    # self.page_items_count: int = 100  # количество результатов поиска на странице
    # self.page: int = 0  # номер страницы для просмотра
    # self.search_field: str = ''  # поле поиска ключевого слова
    # self.experience: str = ''  # требуемый опыт работы
    # self.text: str = ''  # ключевое слово для поиска
    # self.employment: str = ''  # тип занятости
    # self.search_limit = 0  # количество вакасний, которые надо найти

    def __init__(self):
        super().__init__()

        self.references_names = ['areas', 'professional_roles']

        self.properties.update({'page': {'value': 0},
                                'per_page': {'value': 100},
                                'text': {'id': '',
                                         'value': '',
                                         'representation': 'Искать по подстроке'},
                                'search_field': {'id': '',
                                                 'value': '',
                                                 'representation': 'Искать подстроку в поле'},
                                'search_limit': {'value': 0,
                                                 'representation': 'Количество вакансий',
                                                 'do_not_use_in_search': 'uhuh'},
                                'ignore_without_salary': {'value': True,
                                                          'representation': 'Игнорировать вакансии без зарплаты',
                                                          'do_not_use_in_search': 'uhuh'},
                                'auto_convert_to_rur': {'value': False,
                                                        'representation':
                                                            'Конвертировать зарплату в рубли автоматически',
                                                        'do_not_use_in_search': 'uhuh'}
                                })

        del self.properties['salary_max']

    def params(self) -> dict:
        result = {}
        for property_name in self.properties.keys():
            prop = self.properties[property_name]
            if prop.get('id'):
                result[property_name] = prop.get('id')
            else:
                val = prop.get('value')
                if val or (val == 0):
                    if not prop.get('do_not_use_in_search'):
                        result[property_name] = val
        # if self.properties['ignore_without_salary']['value']:
        #     result['only_with_salary'] = 'true'
        # if self.text:
        #     result['text'] = self.text
        # if self.search_field:
        #     result['search_field'] = self.search_field
        # if self.experience:
        #     result['experience'] = self.experience
        return result

    # def set_property(self, property_name:str, id: str = '', value: str = ''):
    #     if property_name in self.properties.keys():
    #
    #         prop = self.properties[property_name]
    #         ref_name = prop.get('ref_name', property_name)
    #         if not HhRef.references.get(ref_name):
    #             HhRef(ref_name, prop.get('subitems_name', 'items'))
    #         if id and HhRef.references[ref_name].item_code_is_valid(new_item_code=id):
    #             prop['id'] = id
    #             prop['value'] = HhRef.references[ref_name].all_items_dict_by_id[id]['name']
    #         else:
    #             prop['value'] = value
    #             if value:
    #                 detected_id = HhRef.references[ref_name].all_items_dict_by_name.get(value, {}).get('id')
    #                 if detected_id:
    #                     prop['id'] = detected_id


"""
    # def show(self):
    #     print(self.params())

    # def set_key_words(self, key_words: list[str]):
    #     words = ', '.join(key_words)

    # @area.setter
    # def area(self, new_area_code: str):
    #     # from src.hh_dictionaries_class import HeadHunterApiDictionaries
    #     # from src.areas_reference_class import AreaReference
    #
    #     # AreaReference.init()
    #     # if AreaReference.area_code_is_valid(new_area_code):
    #     #     self.__area = new_area_code
    #     #     self.__area_name = AreaReference.all_areas_dict_by_id.get(str(new_area_code), {}).get('name',
    #     #                                                                                           'определить не удалось')
    #     # else:
    #     #     raise ValueError
    #     if not HeadHunterReference.references.get('areas'):
    #         HeadHunterReference('areas', 'areas')
    #
    #     areas = HeadHunterReference.references.get('areas')
    #     if areas:
    #         if areas.item_code_is_valid(new_area_code):
    #             self.properties['area']['id'] = str(new_area_code)
    #             self.properties['area']['value'] = areas.all_items_dict_by_id.get(new_area_code, {}).get('name',
    #                                                                                           'определить не удалось')
    #         else:
    #             raise ValueError('Указанный код региона не существует')
    #
    #     else:
    #         raise ValueError('Не загрузить справочник регионов')
"""
