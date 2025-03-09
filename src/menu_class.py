from typing_extensions import Self
from typing import Any, Callable


class Menu:
    def __init__(self, caption: str, items: list[tuple[str, Callable]] | None = None, footer: str = '',
                 previous_menu: Self | None = None):
        self.caption = caption
        self.items = items
        self.footer = footer
        self.previous_menu: Self | None = previous_menu

    def __str__(self):
        # result = '\n' + self.caption + '\n' + 'Выберите дальнейшее действие:\n'
        result = 'Выберите дальнейшее действие:\n'
        for i, item in enumerate(self.items):
            result += f"{str(i+1)}. {item[0]}\n"

        result += f'\n{self.footer}\n'

        return result
