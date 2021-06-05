
from view.teach_model_view.teach_model_window import TeachModelWindow

class TeachModelController:
    def __init__(self, in_main_controller, in_sounds_extraction_module):
        self.main_controller = in_main_controller
        self.window = TeachModelWindow(self)
        self.sounds_extraction_module = in_sounds_extraction_module

    def show_window(self):
        self.window.show()

    def window_closed(self):
        self.main_controller.teach_model_window_closed()

    def load_train_signals(self, filenames):
        return self.sounds_extraction_module.load_train_signals(filenames)

    def load_train_markups(self, filename):
        return self.sounds_extraction_module.load_train_markups(filename)

    def get_status(self, data):
        if data == 'train_signals':
            return self.sounds_extraction_module.get_status_train_signals()
        elif data == 'train_markups':
            return self.sounds_extraction_module.get_status_train_markups()
        elif data == 'model':
            return self.sounds_extraction_module.get_status_classification_module()

    def fit_model(self):
        return self.sounds_extraction_module.fit_classification_model()
