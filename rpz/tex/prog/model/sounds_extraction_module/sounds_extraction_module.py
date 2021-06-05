
from model.load_data_module.load_data_module import LoadDataModule
from model.classification_module.classification_module import ClassificationModule
from model.feature_extraction_module.feature_extraction_module import FeatureExtractionModule
from model.data_preprocessing_module.data_preprocessing_module import DataPreprocessingModule
from model.graph_module.graph_module import GraphModule


class SoundsExtractionModule:
    def __init__(self):
        self.load_data_module = LoadDataModule()
        self.data_preprocessing_module = DataPreprocessingModule()
        self.feature_extraction_module = FeatureExtractionModule()
        self.graph_module = GraphModule()
        self.classification_module = ClassificationModule(self.data_preprocessing_module,
                                                          self.feature_extraction_module)


    def get_status_classification_module(self):
        return self.classification_module.model.status


    def get_status_test_signal(self):
        return self.load_data_module.test_signal.status


    def get_status_train_signals(self):
        return self.load_data_module.train_signals.status


    def get_status_train_markups(self):
        return self.load_data_module.train_markups.status

    def clear_classification_model(self):
        self.load_data_module.clear_model_data()
        self.classification_module.clear_model()


    def fit_classification_model(self):
        if self.get_status_classification_module() != 'Model havent chosen':
            return 'Model chosen'
        train_signals_status = self.get_status_train_signals()
        if train_signals_status == 'Audio-files havent chosen':
            return train_signals_status
        train_markups_status = self.get_status_train_markups()
        if train_markups_status == 'Markups havent chosen':
            return train_markups_status
        status = self.classification_module.fit(self.load_data_module.train_signals.data,
                                                self.load_data_module.train_markups.data)
        return status

    def predict_classification_model(self):
        if self.get_status_classification_module() != 'Model teached':
            return 'Model didnt chosen', ''
        test_signal_status = self.get_status_test_signal()
        if test_signal_status == 'Audio-files havent chosen':
            return test_signal_status, ''
        # возвращает статус и список predicted_markups временных промежутков
        status, predicted_markups = self.classification_module.predict(self.load_data_module.test_signal.data)
        if predicted_markups:
            self.load_data_module.save_predicted_markups(predicted_markups)
            graph = self.graph_module.create_predicted_graph(predicted_markups, self.load_data_module.test_signal.data,
                                                             self.feature_extraction_module.get_t_between_pos(
                                                                 self.load_data_module.test_signal.data, 0.))
            graph_path = self.load_data_module.save_predicted_graph(graph)
            return status, graph_path
        else:
            return status, ''


    def save_classification_model(self, path):
        classification_status = self.get_status_classification_module()
        if classification_status != 'Model teached':
            return 'Model havent chosen'
        return self.load_data_module.save_model(self.classification_module.model.data, path)


    def load_train_signals(self, filenames):
        status = self.get_status_train_signals()
        if status == 'Audio-files have chosen':
            return status
        return self.load_data_module.load_train_signals(filenames)


    def load_train_markups(self, filename):
        status = self.get_status_train_markups()
        if status == 'Markups have chosen':
            return status
        return self.load_data_module.load_train_markups(filename)


    def load_test_signal(self, filename):
        return self.load_data_module.load_test_signal(filename)


    def choose_model(self, path):
        try:
            model = self.load_data_module.load_model(path)
            if model:
                return self.classification_module.load_model(model)
        except:
            return 'LoadErrorModel'
