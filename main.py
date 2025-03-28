import faulthandler
import locale

from src.application_class import Application

if __name__ == "__main__":
    locale.setlocale(category=locale.LC_ALL, locale="Russian")
    faulthandler.enable()
    app = Application()
    app.run()
