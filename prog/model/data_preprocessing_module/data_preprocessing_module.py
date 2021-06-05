import numpy as np
from itertools import chain
import pandas as pd
import ast

from model.feature_extraction_module.feature_extraction_module import FeatureExtractionModule
from model.params.markups_params import MarkupsParams
from model.params.audio_params import AudioParams

class DataPreprocessingModule:

    # получает на вход signal, возвращает признаки signal
    def create_test_data(self, features):
        features_names = FeatureExtractionModule.get_wavelet_columns_names(features[0])
        #res_data = []
        #for feature in features:
        #    res_data.append(list(chain(*feature)))
        #return pd.DataFrame(res_data, columns=features_names)
        return pd.DataFrame(features, columns=features_names)

    def remove_low_energy(self, data):
        indexes = []
        for row in data.iterrows():
            energy = row[1][:-1].sum()
            if energy < 0.005:
                indexes.append(row[0])
        return indexes

    # получает массив признаков [[path, feature],...], разметку в pandas с колонками: ['recordname', 'start', 'end']
    # возвращает обучающую выборку в pandas формате: [feature, feature, ..., y], y = {0,1}
    def create_train_data(self, features, df_markups):
        # получаем названия признаков
        features_names = FeatureExtractionModule.get_wavelet_columns_names(features[0][1][0])
        features_names.append('y')
        res_data = []
        for path, frames_coeffs in features:
            filename = self._get_filename_from_path(path)
            for interval in ast.literal_eval(df_markups[df_markups[MarkupsParams.filename()] == filename]
                                                     .intervals.iloc[0]):
                # получаем временные промежутки между фреймами
                t_positions_between_frames = FeatureExtractionModule.get_t_between_frames(frames_coeffs, interval[0])
                # формируем список Вейвлет-коэффициентов (n) - один фрейм
                # (длина списка - t_positions_between_frames) и добавляем к нему y={0,1}
                y = np.zeros(frames_coeffs.shape[0])
                borders = self._borders_preprocessing(
                    df_markups[df_markups[MarkupsParams.filename()] == filename],
                    MarkupsParams.start_end()[0], MarkupsParams.start_end()[1])
                # оставляем только те границы, что лежат в интервале interval
                borders = self._filter_borders(borders, interval)
                for border in borders:
                    for t_pos in range(len(t_positions_between_frames)):
                        if t_positions_between_frames[t_pos] > border:
                            y[t_pos] = 1.
                            break
                # преобразуем frames_coeffs
                res_data_i = []
                for frames, y_i in zip(frames_coeffs, y):
                    #lst_i = list(chain(*frame))
                    lst_i = [np.square(frame).sum() for frame in frames]
                    lst_i.append(y_i)
                    res_data_i.append(lst_i)
                res_data.extend(res_data_i)
        return pd.DataFrame(res_data, columns=features_names)


    def _filter_borders(self, borders, interval):
        res = []
        for border in borders:
            if border >= interval[0] and border <= interval[1]:
                res.append(border)
        return res

    def _get_filename_from_path(self, path):
        pos = path.rfind('/')
        if pos != -1:
            return path[pos + 1:]
        return path

    def _borders_preprocessing(self, df, column_name_1, column_name_2):
        # сливаем start и end в один список границ и сортируем границы
        borders = np.sort(np.array(self._merge_2_columns_on_row(df, column_name_1, column_name_2)))

        # убираем границы, разница между которыми меньше 25 мсек
        return self._check_on_min_phonem_interval(borders, AudioParams.min_phonem_interval())

    def _merge_2_columns_on_row(self, df, column_name_1, column_name_2):
        lst = []
        for column_1_i, column_2_i in zip(df[column_name_1], df[column_name_2]):
            lst.append(column_1_i)
            lst.append(column_2_i)
        return lst

    def _check_on_min_phonem_interval(self, lst, min_phonem_interval):
        flag = True
        while flag:
            flag = False
            res = []
            next_elem_i = 1
            while next_elem_i < len(lst):
                before_elem = lst[next_elem_i - 1]
                if lst[next_elem_i] - before_elem < min_phonem_interval:
                    flag = True
                    res.append(np.mean([before_elem, lst[next_elem_i]]))
                    next_elem_i += 1
                else:
                    res.append(before_elem)
                next_elem_i += 1
            if lst[-1] - res[-1] >= min_phonem_interval:
                res.append(lst[-1])
            lst = res
        return lst

