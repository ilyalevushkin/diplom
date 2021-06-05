
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
            features = self.feature_extraction_module.extract_from_signals(signals)

            train_data = self.data_preprocessing_module.create_train_data(features, markups)


            train_data = train_data.sample(frac=1)

            y_train = train_data['y'].astype('int64')
            X_train = train_data.drop(axis=0, columns=['y'])

            self.params.model.fit(X_train, y_train)

            self.model.data = self.params.model
            self.model.status = 'Модель обучена'
        except:
            return 'Ошибка обучения модели'
        return self.model.status


    def predict(self, signal):
        if self.model.status != 'Model have teached':
            return self.model.status
        try:
            features = self.feature_extraction_module.extract_from_signal(signal)

            test_data = self.data_preprocessing_module.create_test_data(features)

            test_data = test_data.sample(frac=1)
            predictions = self.model.data.predict(test_data)
            return 'Sounds have got', self._convert_predictions_to_time_list(predictions)
        except:
            return 'Error! Cant get sounds.', None


    def _convert_predictions_to_time_list(self, predictions):

        time_list = self.feature_extraction_module.get_t_between_frames(predictions, 0.)

        res = []
        dt = time_list[1] - time_list[0]
        for t, prediction in zip(time_list, predictions):
            if prediction:
                res.append(t + dt)
        return res

    def load_model(self, model):
        self.model.data = model
        self.model.status = 'Model have chosen'
        return 'Model loaded'

