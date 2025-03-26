import locale
import faulthandler

from src.application_class import Application


if __name__ == '__main__':
    locale.setlocale(category=locale.LC_ALL, locale="Russian")
    faulthandler.enable()
    app = Application()
    # app.init_menus()
    app.run()

