from typing_extensions import Self
from typing import Any, Callable


class Menu:
    def __init__(self, caption: str, items: list[tuple[str, Callable]] | None = None, footer: str = '',
                 previous_menu: Self | None = None):
        self.caption = caption
        self.items = items
        self.footer = footer
        self.previous_menu: Self | None = previous_menu

    def __str__(self) -> str:
        # result = '\n' + self.caption + '\n' + 'Выберите дальнейшее действие:\n'
        result = 'Выберите дальнейшее действие:\n'
        for i, item in enumerate(self.items):
            result += f"{str(i+1)}. {item[0]}\n"

        result += f'\n{self.footer}\n'

        return result

    def add_item(self, item_name: str, pos: int, function: Callable) -> None:
        self.items.insert(pos, (item_name, function))

    def delete_item(self, item_name: str) -> None:
        item_names = [item[0] for item in self.items]
        if item_name in item_names:
            ind = item_names.index(item_name)
            del self.items[ind]
