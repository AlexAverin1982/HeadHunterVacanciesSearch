import requests
import json


class Dictionary:
    def __init__(self, name: str):
        def add_this_sub_area(area_data: dict):
            result = {}
            area_id = area_data.get('id', '')
            area_name = area_data.get('name', '')
            if area_id + area_name:
                result[area_id] = {'name': area_name, 'areas': []}
                result[area_id]['areas'] = [add_this_sub_area(subitem) for subitem in area_data.get('areas', [])]
            return result

        self.name: str = name
        req = requests.get('https://api.hh.ru/'+name)
        if req.ok:
            data_str = req.content.decode()
            dict_data = json.loads(data_str)
            req.close()

            if name == 'areas':
                self.items = [add_this_sub_area(item) for item in dict_data]
                print(self.items)
            else:
                dict_data = dict_data.get('categories', [])
                self.items = [item for item in dict_data]
            # print(self.items)


