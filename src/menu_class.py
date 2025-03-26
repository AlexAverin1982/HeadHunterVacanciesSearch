from typing import Callable

from src.menu_item_class import MenuItem

class Menu:
    """
    Класс меню пользовательского интерфейса
    """

    def __init__(self, name: str, caption: str, status_bar: Callable | None = None, show_search_params: bool = True):
        self.__name: str = name
        self.caption: str = caption
        # self.__prompt = prompt
        self.__status_bar = status_bar
        self.__items = []
        self.show_search_params = show_search_params

    def __str__(self) -> str:
        # result = 'Выберите дальнейшее действие:\n'
        # result = self.caption + '\n'
        result = ''
        for i, item in enumerate(self.__items):
            result += f"{str(i + 1)}. {str(item)}\n"
        if self.__status_bar:
            result += '\n' + str(self.__status_bar())
        else:
            result += '\n'
        return result

    def add_item(self, caption: str, pos: int, function: Callable | None = None) -> None:
        """
        Добавление пункта меню
        :param caption: Текст добавляемого пункта меню
        :param pos:  Позиция, в которую добавляется пункт меню
        :param function: Обработчик события выбора пункта меню
        """
        menu_item = MenuItem(caption=caption, function=function)
        self.__items.insert(pos, menu_item)

    def delete_item(self, item_name: str) -> None:
        """
        Удаление пункта меню
        :param Текст удаляемого пункта меню
        """
        item_names = [str(item) for item in self.__items]
        if item_name in item_names:
            ind = item_names.index(item_name)
            del self.__items[ind]

    def select_menu_item(self, ind: int) -> None:
        """
        Выполнение действие пункта меню
        :param ind: индекс пункта меню
        """
        self.__items[ind].execute()

    def has_item(self, item_caption: str) -> int:
        """
        Проверяет, есть ли в данном меню пункт с указанным заголовком
        :param заголовок искомого пункта
        :return: индекс пункта, если в этом меню пункт с таким заголовком есть, -1, если нет
        """
        result = -1
        for ind, item in enumerate(self.__items):
            if item.caption == item_caption:
                result = ind
                break
        return result

    def set_menu_item_handler(self, menu_item_handler: tuple[str: Callable]) -> None:
        """
        Устанавливает обработчик пункта меню
        :param menu_item_handler: пара заголовок меню : обработчик
        """
        ind = self.has_item(menu_item_handler[0])
        if ind != -1:
            self.__items[ind].set_handler(menu_item_handler[1])

