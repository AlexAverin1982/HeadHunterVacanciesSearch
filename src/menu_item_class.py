from collections.abc import Callable

class MenuItem:
    """
    Класс пункта меню в пользовательском интерфейсе
    """

    def __init__(self, caption: str, function: Callable | None = None):
        self.caption: str = caption
        self.__function = function

    def __str__(self) -> str:
        return self.caption

    def set_handler(self, handler: Callable):
        self.__function = handler

    def execute(self):
        """
        Обработчик события выбора пункта меню
        """
        if self.__function:
            self.__function()