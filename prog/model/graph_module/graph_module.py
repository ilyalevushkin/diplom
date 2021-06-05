import matplotlib.pyplot as plt

class GraphModule:
    # получает список временных промежутков и дискретный сигнал. Возвращает график
    def create_predicted_graph(self, predicted_markups, test_signal, t_lst):
        fig = plt.figure(figsize=(20, 7))
        ax = plt.plot(t_lst, test_signal)
        plt.vlines(predicted_markups, test_signal.min(), test_signal.max(), color='r')
        plt.xlabel('Время, с', fontsize=16)
        plt.ylabel('Амплитуда', fontsize=16)
        #plt.legend([name])
        #plt.title(name)
        return fig
