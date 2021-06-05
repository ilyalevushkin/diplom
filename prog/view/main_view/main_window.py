from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QFileDialog


class MainWindow(QMainWindow):
    def __init__(self, in_controller):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("view/main_view/main_window.ui", self)
        self.controller = in_controller
        self.ui.get_result_button.setEnabled(False)
        self.ui.clear_model_button.setEnabled(False)
        self.ui.save_model_button.setEnabled(False)

    @pyqtSlot(name='on_choose_model_button_clicked')
    def choose_model(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Выберите модель для загрузки',
                                                  './Data/models/', 'Model File(*.pkl)')
        if len(filename) > 0:
            status = self.controller.choose_model(filename)
            if status == 'Модель успешно загружена':
                self.ui.teach_model_button.setEnabled(False)
                self.ui.choose_model_button.setEnabled(False)
                self.ui.clear_model_button.setEnabled(True)
                self.ui.choose_model_label.setText('Модель выбрана')
                self.try_enable_get_result_btn()
            else:
                msgBox = QMessageBox()
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setText(status)
                msgBox.exec()

    @pyqtSlot(name='on_teach_model_button_clicked')
    def teach_model(self):
        self.controller.launch_teach_model_view()
        self.ui.clear_model_button.setEnabled(True)
        self.ui.save_model_button.setEnabled(True)

    @pyqtSlot(name='on_save_model_button_clicked')
    def save_model(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Сохранить модель',
                                                  './Data/models/', 'Model File (*.pkl)')
        if len(filename) > 0:
            status = self.controller.save_model(filename)
            msgBox = QMessageBox()
            msgBox.setStandardButtons(QMessageBox.Ok)
            if status == 'Модель успешно сохранена':
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText(status)
                self.ui.save_model_button.setEnabled(False)
            else:
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setText(status)
            msgBox.exec()

    @pyqtSlot(name='on_clear_model_button_clicked')
    def clear_model(self):
        self.controller.clear_model()
        self.ui.clear_model_button.setEnabled(False)
        self.ui.save_model_button.setEnabled(False)
        self.ui.get_result_button.setEnabled(False)
        self.ui.teach_model_button.setEnabled(True)
        self.ui.choose_model_button.setEnabled(True)


    @pyqtSlot(name='on_choose_test_audio_button_clicked')
    def choose_test_audio(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Выберите mp3-файл для тестирования',
                                                   './Data/test/', 'Audio File(*.mp3)')
        if len(filename) > 0:
            status = self.controller.load_test_signal(filename)
            self.ui.choose_test_audio_label.setText(status)
            self.try_enable_get_result_btn()

    @pyqtSlot(name='on_get_result_button_clicked')
    def get_result(self):
        self.controller.launch_result_view()

    def try_enable_get_result_btn(self):
        if self.controller.get_status('model') == 'Модель обучена':
            test_signal_status = self.controller.get_status('test_signal')
            if test_signal_status == 'Аудио-файл выбран':
                self.ui.get_result_button.setEnabled(True)

