from collections.abc import Callable


class MenuItem:
    """
    Класс пункта меню в пользовательском интерфейсе
    """

    def __init__(self, caption: str, function: Callable | None = None):  # type: ignore
        """
        Конструктор
        :param caption: заголовок пункта меню
        :param function: метод, вызываемый при выборе пункта меню
        """
        self.caption: str = caption
        self.__function = function

    def __str__(self) -> str:
        """
        Символьное представление пункта меню - его заголовок
        """
        return self.caption

    def set_handler(self, handler: Callable) -> None:
        """
        сеттер метода при выборе пункта меню
        :param handler: имя метода
        """
        self.__function = handler

    def execute(self) -> None:
        """
        Обработчик события выбора пункта меню
        """
        if self.__function:
            self.__function()
