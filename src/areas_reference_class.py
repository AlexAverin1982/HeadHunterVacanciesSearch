import json

import requests


class AreasReference:
    top_level: list[str] = []  # список id регионов, у которых parent_id == None
    items_by_name: dict = {}  # словарь всех регионов, где ключи - имена регионов
    items_by_id: dict = {}  # словарь всех регионов, где ключи - id регионов

    def __init__(self) -> None:  # type ignore

        def add_subareas(areas_list: list) -> None:
            for area_data in areas_list:
                id = area_data.get("id")
                if not id:
                    continue
                elif self.items_by_id.get(id):
                    continue
                name = area_data.get("name")
                parent_id = area_data.get("parent_id")
                if parent_id is None:
                    AreasReference.top_level.append(id)
                else:
                    subareas_ids = AreasReference.items_by_id[parent_id].get("areas")
                    if isinstance(subareas_ids, list):
                        subareas_ids.append(id)

                    parent_name = AreasReference.items_by_id[parent_id].get("name")
                    if parent_name:
                        subareas_names = AreasReference.items_by_name.get(
                            parent_name, {}
                        ).get("areas")
                        if isinstance(subareas_names, list):
                            subareas_names.append(id)

                areas = area_data.get("areas")
                AreasReference.items_by_name[name] = {"id": id, "areas": []}
                AreasReference.items_by_id[id] = {"name": name, "areas": []}

                add_subareas(areas)

        # self.items_tree_by_name: dict = {}
        # self.items_tree_by_id: dict = {}
        # self.items_by_name: dict = {}
        # self.items_by_id: dict = {}
        # self.items_by_name: dict = {}
        # self.top_level_items_dict_by_id: dict = {}
        self.subitems: list[str] = (
            []
        )  # список id регионов, у которых parent_id == id текущего региона
        # page=0
        # for page in range(100):
        # url = f"https://api.hh.ru/areas?per_page=100&page={page}"
        req = requests.get("https://api.hh.ru/areas")
        if req.ok:
            data_str = req.content.decode()
            req.close()
            all_areas_list = json.loads(data_str)
            add_subareas(all_areas_list)
        else:
            req.close()

    def item_code_is_valid(self, new_item_code: str) -> bool:  # type: ignore
        """проверка, принадлежит ли указанный код данному справочнику"""
        return new_item_code in self.items_by_id.keys()
