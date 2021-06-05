
import numpy as np
import pandas as pd
from pandas import json_normalize
import json
from scipy.stats import norm

# класс преобразует df['start', 'end'] (float64) в нормальное распределение границ в виде (x, y)
# начальные параметры:
# min_phonem_interval - минимальный межфонемный интервал
# sr - частота дискретизации (количество кадров (разбиений) в секунду)
# distance - на сколько разметка человека границ фонем может максимум ошибаться
# quantile - с какой вероятностью она может ошибаться
class NormBordersDistribution:
    def __init__(self, min_phonem_interval = 0.025, sr=16000, distance=0.2, quantile=0.95):
        self.min_phonem_interval = min_phonem_interval
        self.distance = distance
        self.quantile = quantile
        self.sr = sr
        # зададим ср кв отклонение (scale) такое, что 95% квантиль находится на расстоянии 200 мс от. медианы
        # в переводе на русский - считаем, что разметка человека где граница фонем может ошибаться максимум на 0.2 мс 
        # в обе стороны с 95% вероятностью
        self.scale = self._calc_norm_scale_for_quantile(self.distance, self.quantile)
    
    def convert_df_start_end_to_norm_borders_distribution(self, df):
        try:
            df_start_end = df.loc[:,['start','end']]
        except Exception as e:
            print("No data like df.loc[:,['start', 'end']]")
            print(str(e))
            return
        
        borders = self._borders_preprocessing(df, 'start', 'end')
        
        x, y = self._transform_borders_lst_to_norm_distribution_func(borders, self.distance, self.scale, self.sr)
        return x, y
        

    def _borders_preprocessing(self, df, column_name_1, column_name_2):
        # сливаем start и end в один список границ и сортируем границы
        borders = np.sort(np.array(self._merge_2_columns_on_row(df, 'start', 'end')))
        
        # убираем границы, разница между которыми меньше 25 мсек
        return self._check_on_min_phonem_interval(borders, self.min_phonem_interval)

    
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
            while (next_elem_i < len(lst)):
                before_elem = lst[next_elem_i - 1]
                if (lst[next_elem_i] - before_elem < min_phonem_interval):
                    flag = True
                    res.append(np.mean([before_elem, lst[next_elem_i]]))
                    next_elem_i += 1
                else:
                    res.append(before_elem)
                next_elem_i += 1
            if (lst[-1] - res[-1] >= min_phonem_interval):
                res.append(lst[-1])
            lst = res
        return lst
    
    def _calc_norm_scale_for_quantile(self, distance, quantile):
        # ничего лучше не придумал, как перебирать значения
        start_scale = 0.5
        step = 0.01
        last_distance = norm.ppf(quantile, loc=0., scale=start_scale)
        # чтоб не крашилась на больших distance
        if (last_distance < distance):
            return start_scale

        while (last_distance > distance):
            start_scale -= step
            last_distance = norm.ppf(quantile, loc=0., scale=start_scale)
        # выбираем наиближайнее к distance
        return start_scale if (abs(last_distance - distance) - 
                abs(norm.ppf(quantile, loc=0., scale=start_scale + step) - distance)) < 0 else start_scale + step
    
    def _transform_borders_lst_to_norm_distribution_func(self, borders, distance, scale, sr):
        x_norm_borders = np.array([])
        y_norm_borders = np.array([])
        before_border = borders[0]
        before_distance_between_borders = distance
        
        for border in borders[1:]:
            distance_between_borders = (border - before_border) / 2
            
            # определяем, на сколько разбиваем каждый промежуток
            frequency = round(sr * (distance_between_borders + before_distance_between_borders))
            
            # разбиваем иксы
            next_x = np.linspace(before_border - before_distance_between_borders,\
                                                   before_border + distance_between_borders, frequency)
            x_norm_borders = np.hstack([x_norm_borders, next_x])
            # считаем нормальное распределение и добавляем в y_norm_borders
            y_norm_borders = np.hstack([y_norm_borders, norm.pdf(next_x, loc = before_border, scale = scale)])
            
            before_border = border
            before_distance_between_borders = distance_between_borders

        # определяем, на сколько разбиваем каждый промежуток
        frequency = round(sr * (distance_between_borders + before_distance_between_borders))
        
        next_x = np.linspace(before_border - before_distance_between_borders,\
                                                   before_border + distance, frequency)
        
        x_norm_borders = np.hstack([x_norm_borders, next_x])
        y_norm_borders = np.hstack([y_norm_borders, norm.pdf(next_x, loc = before_border, scale = scale)])
        return x_norm_borders, y_norm_borders