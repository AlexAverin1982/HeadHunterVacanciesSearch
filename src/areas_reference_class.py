import requests
import json

class AreaReference:
    areas_tree_by_name: dict = {}
    areas_tree_by_id: dict = {}
    all_areas_dict_by_name = {}
    all_areas_dict_by_id = {}

    @classmethod
    def init(cls):
        def add_this_sub_area(area_data: dict, parent_dict: dict):
            area_id = area_data.get('id', '')
            area_name = area_data.get('name', '')
            if area_id + area_name:
                cls.areas_tree_by_name[area_name] = {'id': area_id, 'areas': []}
                result[area_name] =
                result[area_name]['areas'] = [add_this_sub_area(subitem) for subitem in area_data.get('areas', [])]
            return result

        req = requests.get('https://api.hh.ru/areas')
        if req.ok:
            data_str = req.content.decode()
            dict_data = json.loads(data_str)
            req.close()
            for item in dict_data:
                add_this_sub_area(item, cls.areas_tree_by_name)
            print(cls.areas_tree_by_name)
