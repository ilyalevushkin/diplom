
class AudioParams:

    @staticmethod
    def sr():
        return 16000

    @staticmethod
    def frame_sz():
        return 2500

    @staticmethod
    def hop_part():
        return 0.6

    @staticmethod
    def wavelet():
        return 'db4'

    @staticmethod
    def wavelet_level():
        return 6

    @staticmethod
    def min_phonem_interval():
        return 0.025
