from rich.traceback import install

from dreidel.controller.home_controller import HomeController
from dreidel.views.qt_view import QtHomeView

install(word_wrap=True, width=None)


def run():
    controller = HomeController(QtHomeView())
    controller.main()


if __name__ == "__main__":
    run()
