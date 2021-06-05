import numpy as np
import librosa
import librosa.display
from scipy import signal
from scipy import interpolate
import json
from pywt import wavedec
from math import log10
from pathlib import Path

# начальные параметры
class Initial_params:
	def __init__(self, sr, frame_sz, 
		hop_part, method, level):
		# частота дискретизации (Гц)
		self.sr = sr
		# размер фрейма (количество отсчетов)
		self.frame_sz = frame_sz
		# 1 - размер перекрытия окна (в долях)
		self.hop_part = hop_part
		# Выбор Вейвлет преобразования
		self.method = method
		# Выбор до какого уровня декомпозиции раскладывается вейвлет
		self.level = level
		
	# возвращает список временных промежутков вместо sig
	def get_t_lst(self, sig, offset):
		t_values = np.arange(len(sig)) / float(self.sr)
		return offset + t_values


class WaveletTransformation:
	def __init__(self, sr = 16000, frame_sz = 512, 
		hop_part = 0.6, method = 'db4', level = 6):
		self.init_par = Initial_params(sr, frame_sz, 
			hop_part, method, level)

	# загружаем аудиофайл и применяем wavelet преобразование 
	# (на выходе дискретизированный сигнал и wavelet коэффициенты для каждого фрейма)
	# И ИХ ИМЕНА! (coeffs_names)
	# offset - с какого момента считываем сигнал (секунды)
	# duration - продолжительность (секунды)
	# file_name - имя файла (строка)
	def wavelet_load_data(self, offset, duration, file_name):
		# чтение из файла и дискретизация сигнала
		descrete_sig = self._get_signal(file_name, self.init_par.sr, offset, duration)

		# разбитие сигнала на фреймы
		frames_signal = self._splitting_signal_on_frames(descrete_sig, self.init_par.frame_sz, 
			self.init_par.hop_part, self.init_par.sr)

		# устранение деффекта на краях с помощью оконной функции Хамминга
		frames_hamming_signal = self._hamming_func(frames_signal, self.init_par.frame_sz)

		# применение вейвлет-преобразования
		frames_coeffs = self._frames_wavelet(frames_hamming_signal, self.init_par.method, self.init_par.level)
		
		# получаем наименования коэффициентов
		coeffs_names = self._get_wavelet_columns_names(frames_coeffs[0])
		return descrete_sig, frames_coeffs, coeffs_names

	# получает время перед каждым фреймом
	def get_t_between_frames(self, offset, frames_coeffs):
		t_values = []
		cur_time = offset
		dt = self.init_par.frame_sz * self.init_par.hop_part / self.init_par.sr
		for i in range(len(frames_coeffs)):
			t_values.append(cur_time)
			cur_time += dt
		return t_values


	def _get_wavelet_columns_names(self, frames_coeffs):
		columns = []
		n = len(frames_coeffs) - 1
		for pos, A_coeffs in enumerate(frames_coeffs[0]):
			columns.append('A_' + str(n) + str(pos))
		for i, D_coeffs in enumerate(frames_coeffs[1:]):
			for j, D_i_coeffs in enumerate(D_coeffs):
				columns.append('D_' + str(n - i) + '_' + str(j))
		return columns

	def _get_signal(self, audio_path, sr, offset, duration):
		x , sr = librosa.load(audio_path, sr=sr, offset=offset, duration=duration)
		return x


	def _splitting_signal_on_frames(self, descrete_sig, frame_sz, hop_part, sr):
		frames = librosa.util.frame(descrete_sig, frame_length=frame_sz, hop_length=int(hop_part * frame_sz), axis=0)
		#show_frames_signal(frames, sr)
		return frames

	def _hamming_func(self, frames_signal, frame_sz):
		w = signal.windows.hamming(frame_sz, sym=True)
		return np.array([w * frame for frame in frames_signal])

	def _wavelet_conv(self, sig, method, level):
		return np.array(wavedec(sig, method, level=level))

	def _frames_wavelet(self, frames_signal, method, level):
		return np.array([self._wavelet_conv(sig, method, level) for sig in frames_signal], dtype=object)

