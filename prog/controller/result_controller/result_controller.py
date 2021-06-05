
from view.result_view.result_window import ResultWindow


class ResultController:
    def __init__(self, in_main_controller, in_sounds_extraction_module):
        self.main_controller = in_main_controller
        self.sounds_extraction_module = in_sounds_extraction_module
        self.window = ResultWindow(self)

    def show_window(self):
        self.window.show()
        self.window.paint_graph()

    def extract_sounds(self):
        return self.sounds_extraction_module.predict_classification_model()
