
import numpy as np

from model.data import Data
from model.params.classification_params import ClassificationParams

class ClassificationModule:
    def __init__(self, in_data_preprocessing_module, in_feature_extraction_module):
        self.data_preprocessing_module = in_data_preprocessing_module
        self.feature_extraction_module = in_feature_extraction_module
        self.params = ClassificationParams()
        self.model = Data('Модель не выбрана')

    def clear_model(self):
        self.model = Data('Модель не выбрана')

    def fit(self, signals, markups):
        if self.model.status == 'Модель обучена':
            return self.model.status
        try:
            # получает массив сигналов: [[path, audio],...], возвращает массив признаков: [[path, feature],...]
            features = self.feature_extraction_module.extract_from_signals(signals)
            # получает массив признаков [[path, feature],...],
            # разметку в pandas с колонками: ['filename', 'start', 'end']
            # возвращает обучающую выборку в pandas формате: [feature, feature, ..., y], y = {0,1}
            train_data = self.data_preprocessing_module.create_train_data(features, markups)

            # перемешиваем данные
            train_data = train_data.sample(frac=1)

            y_train = train_data['y'].astype('int64')
            X_train = train_data.drop(axis=0, columns=['y'])

            self.params.model.fit(X_train, y_train)

            self.model.data = self.params.model
            self.model.status = 'Модель обучена'
        except:
            return 'Ошибка обучения модели'
        return self.model.status

    # возвращает статус и список predicted_markups временных промежутков
    def predict(self, signal):
        if self.model.status != 'Модель обучена':
            return self.model.status
        try:
            features = self.feature_extraction_module.extract_from_signal(signal)
            # получает на вход признаки signal, возвращает pandas признаки с их именами
            test_data = self.data_preprocessing_module.create_test_data(features)
            # получаем индексы шумов
            #useless_indexes=[]
            useless_indexes = self.data_preprocessing_module.remove_low_energy(test_data)
            # перемешиваем данные
            test_data = test_data.sample(frac=1)
            predictions = self.model.data.predict(test_data)
            return 'Звуки успешно выделены', self._convert_predictions_to_time_list(predictions, useless_indexes)
        except:
            return 'Ошибка! Не удалось выделить звуки', None

    # получает на вход список нулей и единиц, возвращает список временных промежутков
    def _convert_predictions_to_time_list(self, predictions, useless_indexes):
        # получаем список ВСЕХ временных промежутков
        time_list = self.feature_extraction_module.get_t_between_frames(predictions, 0.)
        # оставляем только те, у которых единица
        res = []
        dt = (time_list[1] - time_list[0]) / 2
        for pos, (t, prediction) in enumerate(zip(time_list, predictions)):
            if prediction and pos not in useless_indexes:
                res.append(t + dt)
        return res

    def load_model(self, model):
        self.model.data = model
        self.model.status = 'Модель обучена'
        return 'Модель успешно загружена'

