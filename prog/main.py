import sys
from PyQt5.QtWidgets import QApplication

from controller.main_controller.main_controller import MainController


def main():
    app = QApplication(sys.argv)
    MainController()
    app.exec()


if __name__ == '__main__':
    sys.exit(main())
