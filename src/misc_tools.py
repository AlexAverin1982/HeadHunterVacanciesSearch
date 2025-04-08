"""
вспомогательные и полезные функции
"""


def get_indices(indices_str: str, items_count: int = 0) -> list[int]:
    """
    Функция возвращает список индексов как расшифровка строки, где через запятую и тире указаны нужные номера
    :param indices_str: строка, где указаны номера (не индексы, первый номер равен 1!) через запятую и тире
    :param items_count: количество элементов индексируемой коллекции для контроля границ
    """
    indices_list = indices_str.split(",")
    indices = []
    for index in indices_list:
        if index.strip().isdigit():
            index = int(index.strip()) - 1  # type: ignore[assignment]
            indices.append(min(index, items_count - 1))
        elif index.find("-") > -1:
            index = index.replace(" ", "")
            p = index.find("-")
            start = index[:p]
            if not start:
                start = 0  # type: ignore[assignment]
            elif start.strip().isdigit():  # type: ignore[assignment]
                start = min(int(start.strip()) - 1, items_count - 1)  # type: ignore[assignment]
            else:
                continue
            end = index[p + 1:]
            if not end:
                if items_count > 0:
                    end = items_count - 1  # type: ignore[assignment]
                else:
                    continue
            elif end.strip().isdigit():
                end = min(int(end.strip()) - 1, items_count - 1)  # type: ignore[assignment]
            else:
                continue
            indices.extend(range(int(start), int(end + 1)))  # type: ignore[operator]
    return sorted(list(set(indices)))  # type: ignore[arg-type]


def vacancy_complies(vac_data: dict, conditions: dict, ignore_if_none: bool) -> bool:
    """
    Соответствие вакансии условиям
    :param vac_data: свойства вакансии
    :param conditions: условия для анализа
    :param ignore_if_none: True: если свойство условия в вакансии не указано, данная часть условия игнорируется, иначе
    считается, что вакания все равно не подходит
    :return: True - вакансия соответствует условиям или лучше
    """
    result = True
    if not conditions:
        return result
    vac_text = str(vac_data)
    for condition_key, condition_data in conditions.items():
        if condition_key in ["page", "per_page", "search_limit", "auto_convert_to_rur"]:
            continue
        vacancy_value = vac_data.get(condition_key)
        if condition_key == "text":
            search_string = condition_data.get("value")
            if search_string:
                if search_string[0] == "^":
                    result = (
                        (vac_text.find("'" + search_string[1:]) > -1)
                        or (vac_text.find(" " + search_string[1:]) > -1)
                        or (vac_text.find(" " + search_string[1:]) > -1)
                    )
                else:
                    result = vac_text.find(search_string) > -1
            if result:
                continue
            else:
                break
        elif condition_key == "only_with_salary":  # анализируем, указана ли зарплата
            if not isinstance(condition_data, dict):
                continue
            condition_value = condition_data.get("value")
            if condition_value is None:
                continue
            salary_data = vac_data.get(
                "salary"
            )  # смотрим, указана ли зарплата в вакансии
            if salary_data is None:  # не, не указана
                result = ignore_if_none  # эта часть условия игнорируется
            else:
                if isinstance(salary_data, dict):
                    salary_value = salary_data.get("from")
                    if (
                        salary_value is None
                    ):  # нижний порог зарплаты в вакансии не указан
                        salary_value = salary_data.get("to")  # ищем верхний
                    if salary_value:  # зарплата в вакансии указана
                        if isinstance(salary_value, int):  # числом
                            result = bool(condition_data)
                        elif isinstance(vacancy_value, str) and vacancy_value.isdigit():
                            result = bool(condition_data)  # строкой с числом
                        else:  # зарплата указана неверно или не указана
                            result = ignore_if_none  # эта часть условия игнорируется
                    else:  # зарплата не указана
                        result = ignore_if_none  # эта часть условия игнорируется
                else:
                    raise ValueError("Нестандартный вариант указания зарплаты")
            # if isinstance(vacancy_value, dict):
            # else:
            #     raise ValueError('Нестандартный вариант указания зарплаты')
        elif isinstance(condition_data, dict):
            # if vacancy_value:
            if "id" in condition_data.keys():
                condition_id = condition_data["id"]
                if not condition_id:
                    continue
                if isinstance(vacancy_value, dict):
                    result = condition_data["id"] == vacancy_value.get("id", "")
            elif "value" in condition_data.keys():
                condition_value = condition_data["value"]
                if not condition_value:
                    continue
            elif "from" in condition_data.keys():
                cond_value = condition_data.get("from")
                if not isinstance(cond_value, int):
                    if isinstance(cond_value, str) and cond_value.isdigit():
                        cond_value = int(cond_value)
                    else:
                        continue
                if not isinstance(cond_value, int):
                    if result:
                        continue
                    else:
                        break
                vac_value = vacancy_value.get("from")
                if not isinstance(vac_value, int):
                    if isinstance(vac_value, str) and vac_value.isdigit():
                        vac_value = int(vac_value)
                    else:
                        result = not ignore_if_none
                    if not isinstance(vac_value, int):
                        if result:
                            continue
                        else:
                            break
            # if isinstance(condition_data, dict):
            #     if isinstance(vacancy_value, dict):
            #             result = condition_data["id"] == vacancy_value.get("id", "")
            #         elif "from" in condition_data.keys():
            #             cond_value = condition_data.get("from")
            #             if not isinstance(cond_value, int):
            #                 if isinstance(cond_value, str) and cond_value.isdigit():
            #                     cond_value = int(cond_value)
            #                 else:
            #                     continue
            #             if not isinstance(cond_value, int):
            #                 if result:
            #                     continue
            #                 else:
            #                     break
            #             vac_value = vacancy_value.get("from")
            #             if not isinstance(vac_value, int):
            #                 if isinstance(vac_value, str) and vac_value.isdigit():
            #                     vac_value = int(vac_value)
            #                 else:
            #                     result = not ignore_if_none
            #                 if not isinstance(vac_value, int):
            #                     if result:
            #                         continue
            #                     else:
            #                         break
            #
            #             result = int(cond_value) <= int(vac_value)
            #     else:
            #         result = False
            # # result = condition_value == vacancy_value
        else:
            result = not ignore_if_none
        if not result:
            break
    return result
