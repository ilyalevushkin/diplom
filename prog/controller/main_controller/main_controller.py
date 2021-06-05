
from view.main_view.main_window import MainWindow
from view.result_view.result_window import ResultWindow
from view.teach_model_view.teach_model_window import TeachModelWindow

from ..result_controller.result_controller import ResultController
from ..teach_model_controller.teach_model_controller import TeachModelController

from model.sounds_extraction_module.sounds_extraction_module import SoundsExtractionModule


class MainController:
    def __init__(self):
        self.main_window = MainWindow(self)
        self.main_window.show()
        self.sounds_extraction_module = SoundsExtractionModule()

        # инициализация teach_model_controller
        self.teach_model_controller = TeachModelController(self, self.sounds_extraction_module)

        # инициализация result_controller
        self.result_controller = ResultController(self, self.sounds_extraction_module)

    def launch_teach_model_view(self):
        self.teach_model_controller.show_window()

    def teach_model_window_closed(self):
        self.main_window.try_enable_get_result_btn()

    def launch_result_view(self):
        self.result_controller.show_window()

    def clear_model(self):
        self.sounds_extraction_module.clear_classification_model()

    def load_test_signal(self, filename):
        return self.sounds_extraction_module.load_test_signal(filename)

    def get_status(self, data):
        if data == 'test_signal':
            return self.sounds_extraction_module.get_status_test_signal()
        elif data == 'model':
            return self.sounds_extraction_module.get_status_classification_module()

    def choose_model(self, path):
        return self.sounds_extraction_module.choose_model(path)

    def save_model(self, path):
        return self.sounds_extraction_module.save_classification_model(path)
