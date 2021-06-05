from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QWidget


class ResultWindow(QWidget):
    def __init__(self, in_controller):
        super(ResultWindow, self).__init__()
        self.ui = uic.loadUi("view/result_view/result_window.ui", self)
        self.controller = in_controller

    @pyqtSlot(name='on_close_button_clicked')
    def close_btn(self):
        self.close()

    def paint_graph(self):
        status, result_graph_path = self.controller.extract_sounds()
        if len(result_graph_path) > 0:
            self.ui.graph_label.setStyleSheet("QLabel{{border-image: url({});}}"
                                              .format(result_graph_path))
        else:
            msgBox = QMessageBox()
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText(status)
            msgBox.exec()
