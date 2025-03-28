import json

import requests


class HeadHunterReference:
    """
    Класс для работы (быстрый поиск, отображение свойств) со справочниками headhunter
    """

    references: dict = {}

    def __init__(self, reference_name: str, items_key_name: str | list[str]):  # type: ignore
        """
        конструктор
        :param reference_name: имя справочника
        :param items_key_name: имя подчиненных элементов,
        """

        def add_this_sub_item(
                item_data: dict,
                key_name: str | list[str],
                parent_dict_by_name: dict | None,
                parent_dict_by_id: dict | None,
                level: int,
        ) -> None:
            """
            рекурсионное добавление многоуровневых записей справочников
            :param item_data:  данные, которые нужно записать в справочник
            :param key_name: ключ нужной информации
            :param parent_dict_by_name: словарь-родитель текущего уровня, где ключи - имена
            :param parent_dict_by_id: словарь-родитель текущего уровня, где ключи - коды
            :param level: текущий уровень вложенности записей
            :return:
            """
            item_id = item_data.get("id", "")
            item_name = item_data.get("name", "")
            # if isinstance(key_name, str):
            if item_id + item_name:
                if parent_dict_by_name is not None:
                    parent_dict_by_name[item_name] = {"id": item_id, key_name: {}}
                if parent_dict_by_id is not None:
                    parent_dict_by_id[item_id] = {"name": item_name, key_name: {}}

                self.all_items_dict_by_name[item_name] = parent_dict_by_name[item_name]  # type: ignore[index]
                self.all_items_dict_by_id[item_id] = parent_dict_by_id[item_id]  # type: ignore[index]
                if level == 0:
                    self.top_level_items_dict_by_id[item_id] = parent_dict_by_id[  # type: ignore[index]
                        item_id
                    ]
                    self.top_level_items_dict_by_name[item_name] = parent_dict_by_name[  # type: ignore[index]
                        item_name
                    ]

                for sub_item in item_data.get(key_name, []):
                    add_this_sub_item(
                        sub_item,
                        items_key_name,
                        parent_dict_by_name[item_name][key_name],  # type: ignore[index]
                        parent_dict_by_id[item_id][key_name],  # type: ignore[index]
                        level + 1,
                    )
            # else:
            #     if isinstance(key_name, list):
            #         for key in key_name:
            #             sub_item_data = item_data.get(key)
            #             if isinstance(sub_item_data, dict):
            #                 add_this_sub_item(sub_item_data, key_name, parent_dict_by_name,
            #                                   parent_dict_by_id, level + 1)
            #             elif isinstance(sub_item_data, list):
            #                 for list_item in sub_item_data:
            #                     add_this_sub_item(list_item, key, parent_dict_by_name,
            #                                       parent_dict_by_id, level + 1)

        self.items_tree_by_name: dict = {}
        self.items_tree_by_id: dict = {}
        self.all_items_dict_by_name: dict = {}
        self.all_items_dict_by_id: dict = {}
        self.top_level_items_dict_by_name: dict = {}
        self.top_level_items_dict_by_id: dict = {}
        req = requests.get(f"https://api.hh.ru/{reference_name}")
        if req.ok:
            data_str = req.content.decode()
            dict_data = json.loads(data_str)
            req.close()

            for item in dict_data:
                if isinstance(item, dict):
                    add_this_sub_item(
                        item,
                        items_key_name,
                        self.items_tree_by_name,
                        self.items_tree_by_id,
                        0,
                    )

                elif isinstance(dict_data, dict):
                    if isinstance(items_key_name, list):
                        for key in items_key_name:
                            sub_item = dict_data.get(key)
                            if sub_item:
                                if isinstance(sub_item, list):
                                    for list_item in sub_item:
                                        if isinstance(list_item, dict):
                                            item_id = list_item.get("id")
                                            item_name = list_item.get("name")
                                            if item_id and item_name:
                                                self.all_items_dict_by_name[
                                                    item_name
                                                ] = {"id": item_id}
                                                self.all_items_dict_by_id[item_id] = {
                                                    "name": item_name
                                                }
                                # print(sub_item)

            HeadHunterReference.references[reference_name] = self

    def item_code_is_valid(self, new_item_code: str) -> bool:  # type: ignore
        """проверка, принадлежит ли указанный код данному справочнику"""
        return new_item_code in self.all_items_dict_by_id.keys()
