from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox, QDialog, QFileDialog


class TeachModelWindow(QDialog):
    def __init__(self, in_controller):
        super(TeachModelWindow, self).__init__()
        self.ui = uic.loadUi("view/teach_model_view/teach_model_window.ui", self)
        self.controller = in_controller
        self.ui.fit_model_button.setEnabled(False)
        self.ui.choose_fit_audio_button.setEnabled(False)

    @pyqtSlot(name='on_close_button_clicked')
    def close_btn(self):
        self.controller.window_closed()
        self.close()

    @pyqtSlot(name='on_choose_fit_audio_button_clicked')
    def choose_fit_audio(self):
        filenames, _ = QFileDialog.getOpenFileNames(self, 'Выберите mp3-файлы для обучения',
                                                     './Data/train/', 'Audio Files(*.mp3)')
        if len(filenames) > 0:
            status = self.controller.load_train_signals(filenames)
            self.ui.choose_fit_audio_label.setText(status)

            markups_status = self.controller.get_status('train_markups')
            if status == 'Аудио-файлы выбраны' and markups_status == 'Разметка выбрана':
                model_status = self.controller.get_status('model')
                if model_status == 'Модель не выбрана':
                    self.ui.fit_model_button.setEnabled(True)

    @pyqtSlot(name='on_fit_model_button_clicked')
    def fit_model_btn(self):
        status = self.controller.fit_model()
        msgBox = QMessageBox()
        msgBox.setStandardButtons(QMessageBox.Ok)
        if status == 'Модель обучена':
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(status)
            self.ui.fit_model_label.setText(status)
        else:
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText(status)
        msgBox.exec()

    @pyqtSlot(name='on_choose_fit_markups_button_clicked')
    def choose_fit_markups(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Выберите csv-разметку для обучения',
                                                   './Data/train/', 'CSV File(*.csv)')
        if len(filename) > 0:
            status = self.controller.load_train_markups(filename)
            self.ui.choose_fit_markups_label.setText(status)

            if status == 'Разметка выбрана':
                self.ui.choose_fit_audio_button.setEnabled(True)
                audios_status = self.controller.get_status('train_signals')
                if audios_status == 'Аудио-файлы выбраны':
                    model_status = self.controller.get_status('model')
                    if model_status == 'Модель не выбрана':
                        self.ui.fit_model_button.setEnabled(True)




