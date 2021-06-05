import pandas as pd
import librosa
from itertools import chain
import ast
import matplotlib.pyplot as plt
import pickle

from model.data import Data
from model.params.audio_params import AudioParams
from model.params.markups_params import MarkupsParams


class LoadDataModule:
    def __init__(self):
        self.test_signal = Data('Аудио-файл не выбран')
        self.test_signal_filename = 'undefined_filename'
        self.train_signals = Data('Аудио-файлы не выбраны')
        self.train_markups = Data('Разметка не выбрана')

    # загрузка аудио-данных через librosa.load. Сохраняет массив: [[path, audio],...]
    def load_train_signals(self, paths):
        res = []
        for path in paths:
            df = self.train_markups.data
            filename = self._get_filename_from_path(path)
            intervals = ast.literal_eval(df[df.recordname == filename].intervals.iloc[0])
            for interval in intervals:
                res.append([path, librosa.load(path, sr=AudioParams.sr(), offset=interval[0],
                                               duration=interval[1]-interval[0])[0]])
        self.train_signals.data = res
        self.train_signals.status = 'Аудио-файлы выбраны'
        return self.train_signals.status

    def _get_filename_from_path(self, path):
        pos = path.rfind('/')
        if pos != -1:
            return path[pos + 1:]
        return path

    # загрузка данных в pandas формате
    def load_train_markups(self, path):
        df = pd.read_csv(path)
        self.train_markups.data = df
        self.train_markups.status = 'Разметка выбрана'
        return self.train_markups.status

    # загрузка аудио-данных через librosa.load. Сохраняет audio
    def load_test_signal(self, path):
        self.test_signal_filename = self._get_filename_from_path(path)[:-4]
        self.test_signal.data, _ = librosa.load(path, sr=AudioParams.sr(), offset=0.)
        self.test_signal.status = 'Аудио-файл выбран'
        return self.test_signal.status

    # сохраняем предсказанные данные в формате csv (поступают в формате list)
    def save_predicted_markups(self, predicted_markups):
        df = pd.DataFrame({'y': predicted_markups})
        df.to_csv('./Data/result_markups/'+self.test_signal_filename+'.csv')

    # сохраняем построенный график в формате png (поступает в формате plt)
    def save_predicted_graph(self, graph):
        graph_path = './Data/result_photo/'+self.test_signal_filename+'.png'
        plt.savefig(graph_path)
        return graph_path

    def clear_model_data(self):
        self.train_signals = Data('Аудио-файлы не выбраны')
        self.train_markups = Data('Разметка не выбрана')

    def load_model(self, path):
        with open(path, 'rb') as file:
            return pickle.load(file)

    def save_model(self, model, path):
        with open(path, 'wb') as file:
            pickle.dump(model, file)
        return 'Модель успешно сохранена'
