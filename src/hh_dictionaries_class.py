from src.dictionary_class import Dictionary


class HeadHunterApiDictionaries:
    __dictionaries = {}
    __dict_names = ['areas', 'professional_roles', 'vacancy_search_fields', 'experience', 'employment', 'schedule']
    @classmethod
    def init_dictionary(cls, dict_name):
        if dict_name in cls.__dict_names:
            cls.__dictionaries[dict_name] = Dictionary(dict_name)

    @classmethod
    def area_code_is_valid(cls, new_area_code: int) -> bool:
        if not cls.__dictionaries.get('areas'):
            cls.init_dictionary('areas')
            area_dict = cls.__dictionaries.get('areas')
            if area_dict:
                return new_area_code in area_dict.items.keys()
            else:
                return False

    @classmethod
    def list_of_areas(cls, parent_area: int = 0, sort_by_code: bool = True):
        result = []
        if not cls.__dictionaries.get('areas'):
            cls.init_dictionary('areas')
        if parent_area:
            pass
        else:
            result = cls.__dictionaries['areas']
