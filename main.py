import locale

from src.application_class import Application


if __name__ == '__main__':
    locale.setlocale(category=locale.LC_ALL, locale="Russian")
    app = Application()
    # app.init_menus()
    app.run()

