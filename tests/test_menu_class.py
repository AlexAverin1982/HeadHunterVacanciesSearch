from src.menu_class import Menu


def test_status_bar() -> None:
    def status_bar_function() -> str:
        return "status"

    menu = Menu(
        name="menu with status", caption="menu caption", status_bar=status_bar_function
    )
    output = []
    print = lambda s: output.append(s)
    print(str(menu))
    assert output[-1] == "\nstatus"
