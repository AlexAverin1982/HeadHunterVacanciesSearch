import requests
import json

class ProfessionsReference:
    areas_tree_by_name: dict = {}
    areas_tree_by_id: dict = {}
    all_areas_dict_by_name = {}
    all_areas_dict_by_id = {}

    @classmethod
    def init(cls):
        def add_this_sub_area(area_data: dict, parent_dict_by_name: dict, parent_dict_by_id: dict):
            area_id = area_data.get('id', '')
            area_name = area_data.get('name', '')
            if area_id + area_name:
                parent_dict_by_name[area_name] = {'id': area_id, 'areas': {}}
                parent_dict_by_id[area_id] = {'name': area_name, 'areas': {}}
                cls.all_areas_dict_by_name[area_name] = parent_dict_by_name[area_name]
                cls.all_areas_dict_by_id[area_id] = parent_dict_by_id[area_id]
                for sub_area in area_data.get('areas', []):
                    add_this_sub_area(sub_area,
                                      parent_dict_by_name[area_name]['areas'],
                                      parent_dict_by_id[area_id]['areas'])

        req = requests.get('https://api.hh.ru/professional_roles')
        if req.ok:
            data_str = req.content.decode()
            dict_data = json.loads(data_str)
            req.close()
            for item in dict_data:
                add_this_sub_area(item, cls.areas_tree_by_name, cls.areas_tree_by_id)

    @classmethod
    def area_code_is_valid(cls, new_area_code: int) -> bool:
        if not cls.all_areas_dict_by_id:
            cls.init()
        return str(new_area_code) in cls.all_areas_dict_by_id.keys()
