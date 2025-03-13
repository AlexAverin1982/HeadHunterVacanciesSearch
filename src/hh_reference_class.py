import requests
import json
from typing_extensions import Self

class HeadHunterReference:
    references: dict[str: Self] = {}
    # @classmethod
    # def init(self):
    # 
    #     req = requests.get('https://api.hh.ru/professional_roles')
    #     if req.ok:
    #         data_str = req.content.decode()
    #         dict_data = json.loads(data_str)
    #         req.close()
    #         for item in dict_data:
    #             add_this_sub_item(item, self.items_tree_by_name, self.items_tree_by_id)
    # 
    # @classmethod
    # def item_code_is_valid(self, new_item_code: int) -> bool:
    #     if not self.all_items_dict_by_id:
    #         self.init()
    #     return str(new_item_code) in self.all_items_dict_by_id.keys()
    def __init__(self, reference_name: str, items_key_name: str):
            def add_this_sub_item(item_data: dict, parent_dict_by_name: dict, parent_dict_by_id: dict, level: int):
                item_id = item_data.get('id', '')
                item_name = item_data.get('name', '')
                if item_id + item_name:
                    parent_dict_by_name[item_name] = {'id': item_id, items_key_name: {}}
                    parent_dict_by_id[item_id] = {'name': item_name, items_key_name: {}}
                    self.all_items_dict_by_name[item_name] = parent_dict_by_name[item_name]
                    self.all_items_dict_by_id[item_id] = parent_dict_by_id[item_id]
                    if level == 0:
                        self.top_level_items_dict_by_id[item_id] = parent_dict_by_id[item_id]
                        self.top_level_items_dict_by_name[item_name] = parent_dict_by_name[item_name]

                    for sub_item in item_data.get(items_key_name, []):
                        add_this_sub_item(sub_item,
                                          parent_dict_by_name[item_name][items_key_name],
                                          parent_dict_by_id[item_id][items_key_name], level + 1)

            self.items_tree_by_name: dict = {}
            self.items_tree_by_id: dict = {}
            self.all_items_dict_by_name = {}
            self.all_items_dict_by_id = {}
            self.top_level_items_dict_by_name = {}
            self.top_level_items_dict_by_id = {}
            req = requests.get(f'https://api.hh.ru/{reference_name}')
            if req.ok:
                data_str = req.content.decode()
                dict_data = json.loads(data_str)
                req.close()
                for item in dict_data:
                    add_this_sub_item(item, self.items_tree_by_name, self.items_tree_by_id, 0)

                HeadHunterReference.references[reference_name] = self

    def item_code_is_valid(self, new_item_code: str) -> bool:
        return new_item_code in self.all_items_dict_by_id.keys()
