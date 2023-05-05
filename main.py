from PySide6.QtWidgets import QApplication

from gui.view import View
from datamodel.data import *


if __name__ == "__main__":

    # m1 = MacroCalc()
    # data = {'name': 'Name'}
    # m1.add(data)
    # mc = MacroCalcCache()
    # mc.add(m1)

    app = QApplication()
    view = View()
    view.show()
    app.exec()
