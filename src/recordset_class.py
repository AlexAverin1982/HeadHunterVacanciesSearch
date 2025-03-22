from typing import Any
from src.hh_reference_class import HeadHunterReference as HhRef


class RecordSet:
    """
    Структурированный набор свойств для работы со справочниками и вакансиями hh
    """

    def __init__(self):
        self.properties: dict = {'area': {'id': '113',
                                          'value': 'вся Россия',
                                          'representation': 'Регион поиска вакансий',
                                          'ref_name': 'areas',
                                          'subitems_name': 'areas'},
                                 'professional_role': {'id': '',
                                          'value': '',
                                          'representation': 'Искомая должность',
                                          'ref_name': 'professional_roles'},
                                 'salary': {'id': '',
                                          'value': '',
                                          'representation': 'Минимальная зарплата'},
                                 'salary_max': {'id': '',
                                          'value': '',
                                          'representation': 'Максимальная зарплата'},
                                 'experience': {'id': '',
                                          'value': '',
                                          'representation': 'Требуемый опыт'},
                                 'employer': {'id': '',
                                              'value': '',
                                              'representation': 'Работодатель'}}


    def __str__(self):
        result = ""

        for property_name in self.properties.keys():
            if self.properties[property_name].get('representation'):
                result += f"{self.properties[property_name]['representation']}: "
                val = str(self.properties[property_name].get('value', 'значение не указано'))
                if val == '':
                    val = 'значение не указано'
                result += val.replace('True', 'да').replace('False', 'нет')
                result += '\n'

        return result


    def set_property(self, property_name:str, id: str = '', value: Any | str = ''):
        if property_name in self.properties.keys():

            prop = self.properties[property_name]
            ref_name = prop.get('ref_name', property_name)
            if not HhRef.references.get(ref_name):
                HhRef(ref_name, prop.get('subitems_name', 'items'))
            if id:
                if HhRef.references[ref_name].item_code_is_valid(new_item_code=id):
                    prop['id'] = id
                    prop['value'] = HhRef.references[ref_name].all_items_dict_by_id[id]['name']
                else:
                    raise ValueError
            else:
                prop['value'] = value
                if value:
                    if HhRef.references.get(ref_name):
                        detected_id = HhRef.references[ref_name].all_items_dict_by_name.get(value, {}).get('id')
                        if detected_id:
                            prop['id'] = detected_id
