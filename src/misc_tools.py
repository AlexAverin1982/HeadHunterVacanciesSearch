def get_indices(indices_str: str, items_count: int = 0) -> list[int]:
    """
    Функция возвращает список индексов как расшифровка строки, где через запятую и тире указаны нужные номера
    :param indices_str: строка, где указаны номера (не индексы, первый номер равен 1!) через запятую и тире
    :param items_count: количество элементов индексируемой коллекции для контроля границ
    """
    indices_list = indices_str.split(',')
    indices = []
    for index in indices_list:
        if index.strip().isdigit():
            indices.append(int(index.strip()) - 1)
        elif index.find('-') > -1:
            p = index.find('-')
            start = index[:p]
            if not start:
                start = 0
            elif start.strip().isdigit():
                start = int(start.strip()) - 1
            else:
                continue
            end = index[p + 1:]
            if not end:
                if items_count > 0:
                    end = items_count - 1
                else:
                    continue
            elif end.strip().isdigit():
                end = min(int(end.strip()) - 1, len(self.vacancies) - 1)
            else:
                continue
            indices.extend(range(start, end + 1))
    return indices
