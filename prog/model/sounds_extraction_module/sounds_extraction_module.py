
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

    # статусы classification_module: ['Модель не выбрана', 'Модель выбрана', 'Модель обучена']
    def get_status_classification_module(self):
        return self.classification_module.model.status

    # статусы test_signal: ['Аудио-файл не выбран', 'Аудио-файл выбран']
    def get_status_test_signal(self):
        return self.load_data_module.test_signal.status

    # статусы train_signals: ['Аудио-файлы не выбраны', 'Аудио-файлы выбраны']
    def get_status_train_signals(self):
        return self.load_data_module.train_signals.status

    # статусы train_markups: ['Разметка не выбрана', 'Разметка выбрана']
    def get_status_train_markups(self):
        return self.load_data_module.train_markups.status

    def clear_classification_model(self):
        self.load_data_module.clear_model_data()
        self.classification_module.clear_model()

    # обучает модель. возвращает следующие статусы: ['Модель уже обучена', 'Аудио-файлы не выбраны',
    # 'Разметка не выбрана', 'Ошибка обучения модели: <<переданная ошибка>>', ]
    # работает только в случае необученной модели и загруженной
    def fit_classification_model(self):
        if self.get_status_classification_module() != 'Модель не выбрана':
            return 'Модель уже обучена или выбрана'
        train_signals_status = self.get_status_train_signals()
        if train_signals_status == 'Аудио-файлы не выбраны':
            return train_signals_status
        train_markups_status = self.get_status_train_markups()
        if train_markups_status == 'Разметка не выбрана':
            return train_markups_status
        status = self.classification_module.fit(self.load_data_module.train_signals.data,
                                                self.load_data_module.train_markups.data)
        return status

    # предсказать результат. Возвращает пару - статус, список ответов???
    def predict_classification_model(self):
        if self.get_status_classification_module() != 'Модель обучена':
            return 'Модель не выбрана или не обучена', ''
        test_signal_status = self.get_status_test_signal()
        if test_signal_status == 'Аудио-файл не выбран':
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

    # сохраняет модель классификации. Возвращает статус операции (str)
    def save_classification_model(self, path):
        classification_status = self.get_status_classification_module()
        if classification_status != 'Модель обучена':
            return 'Модель не загружена или не обучена'
        return self.load_data_module.save_model(self.classification_module.model.data, path)

    # загружает аудио-файлы для обучения, возвращает статус
    def load_train_signals(self, filenames):
        status = self.get_status_train_signals()
        if status == 'Аудио-файлы выбраны':
            return status
        return self.load_data_module.load_train_signals(filenames)

    # загружает разметку для обучения, возвращает статус
    def load_train_markups(self, filename):
        status = self.get_status_train_markups()
        if status == 'Разметка выбрана':
            return status
        return self.load_data_module.load_train_markups(filename)

    # загружает аудио-файл для тестирования, возвращает статус
    def load_test_signal(self, filename):
        #status = self.get_status_test_signal()
        #if status == 'Аудио-файл выбран':
        #    return status
        return self.load_data_module.load_test_signal(filename)

    # загружает модель классификации, возвращает статус
    def choose_model(self, path):
        try:
            model = self.load_data_module.load_model(path)
            if model:
                return self.classification_module.load_model(model)
        except:
            return 'Ошибка загрузки модели'
