import numpy as np
import librosa
from scipy import signal
from pywt import wavedec

from model.params.audio_params import AudioParams

class FeatureExtractionModule:

    @staticmethod
    def get_wavelet_columns_names(features):
        '''columns = []
        n = len(features) - 1
        for pos, A_coeffs in enumerate(features[0]):
            columns.append('A_' + str(n) + str(pos))
        for i, D_coeffs in enumerate(features[1:]):
            for j, D_i_coeffs in enumerate(D_coeffs):
                columns.append('D_' + str(n - i) + '_' + str(j))
        return columns'''
        #return ['A', 'D6', 'D5', 'D4', 'D3', 'D2', 'D1']
        res = ['D' + str(i) for i in range(len(features) - 1, 0, -1)]
        res.insert(0, 'A')
        return res
        #return ['D' + str(i) for i in range(len(features))]

    @staticmethod
    def get_t_between_frames(frames_coeffs, offset):
        t_values = []
        cur_time = offset
        dt = AudioParams.frame_sz() * AudioParams.hop_part() / AudioParams.sr()
        for i in range(len(frames_coeffs)):
            t_values.append(cur_time)
            cur_time += dt
        return np.array(t_values)

    @staticmethod
    def get_t_between_pos(sig, offset):
        t_values = []
        cur_time = offset
        dt = 1 / AudioParams.sr()
        for i in range(len(sig)):
            t_values.append(cur_time)
            cur_time += dt
        return np.array(t_values)

    # получает массив сигналов: [[path, signal],...], возвращает словарь признаков: {path: feature}
    def extract_from_signals(self, sigs):
        res = []
        for path_sig in sigs:
            res.append([path_sig[0], self.extract_from_signal(path_sig[1])])
        return res

    # получает на вход signal, возвращает признаки signal
    def extract_from_signal(self, sig):
        # разбитие сигнала на фреймы
        frames_sig = self._splitting_signal_on_frames(sig, AudioParams.frame_sz(), AudioParams.hop_part())

        # устранение деффекта на краях с помощью оконной функции Хамминга
        frames_hamming_sig = self._hamming_func(frames_sig, AudioParams.frame_sz())

        # применение вейвлет-преобразования
        frames_coeffs = self._frames_wavelet(frames_hamming_sig, AudioParams.wavelet(), AudioParams.wavelet_level())

        return frames_coeffs

    def _splitting_signal_on_frames(self, descrete_sig, frame_sz, hop_part):
        frames = librosa.util.frame(descrete_sig, frame_length=frame_sz, hop_length=int(hop_part * frame_sz), axis=0)
        return frames

    def _hamming_func(self, frames_signal, frame_sz):
        w = signal.windows.hamming(frame_sz, sym=True)
        return np.array([w * frame for frame in frames_signal])

    def _wavelet_conv(self, sig, method, level):
        levels = np.array(wavedec(sig, method, level=level))
        return [np.square(level).sum() for level in levels]

    def _frames_wavelet(self, frames_signal, method, level):
        return np.array([self._wavelet_conv(sig, method, level) for sig in frames_signal], dtype=object)

