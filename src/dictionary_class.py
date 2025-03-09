import requests
import json


class Dictionary:
    def __init__(self, name: str):
        def add_this_sub_area(area_data: dict):
            self.items[area_data.get('id', 0)] = area_data.get('name', '')
            for subitem in area_data.get('areas', []):
                add_this_sub_area(subitem)

        self.name: str = name
        req = requests.get('https://api.hh.ru/'+name)
        if req.ok:
            data_str = req.content.decode()
            dict_data = json.loads(data_str)
            req.close()

            if name == 'areas':
                self.items = {}
                for item in dict_data:
                    add_this_sub_area(item)
            else:
                dict_data = dict_data.get('categories', [])
                self.items = [item for item in dict_data]
            # print(self.items)


