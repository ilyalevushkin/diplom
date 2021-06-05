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
        self.test_signal = Data('Audio-file havent chosen')
        self.test_signal_filename = 'undefined_filename'
        self.train_signals = Data('Audio-files havent chosen')
        self.train_markups = Data('Markups havent chosen')


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
        self.train_signals.status = 'Audio-files have chosen'
        return self.train_signals.status

    def _get_filename_from_path(self, path):
        pos = path.rfind('/')
        if pos != -1:
            return path[pos + 1:]
        return path


    def load_train_markups(self, path):
        df = pd.read_csv(path)
        self.train_markups.data = df
        self.train_markups.status = 'Markups have chosen'
        return self.train_markups.status


    def load_test_signal(self, path):
        self.test_signal_filename = self._get_filename_from_path(path)[:-4]
        self.test_signal.data, _ = librosa.load(path, sr=AudioParams.sr(), offset=0.)
        self.test_signal.status = 'Audio-file have chosen'
        return self.test_signal.status


    def save_predicted_markups(self, predicted_markups):
        df = pd.DataFrame({'y': predicted_markups})
        df.to_csv('./Data/result_markups/'+self.test_signal_filename+'.csv')


    def save_predicted_graph(self, graph):
        graph_path = './Data/result_photo/'+self.test_signal_filename+'.png'
        plt.savefig(graph_path)
        return graph_path

    def clear_model_data(self):
        self.train_signals = Data('Audio-files havent chosen')
        self.train_markups = Data('Markups havent chosen')

    def load_model(self, path):
        with open(path, 'rb') as file:
            return pickle.load(file)

    def save_model(self, model, path):
        with open(path, 'wb') as file:
            pickle.dump(model, file)
        return 'Model saved'
