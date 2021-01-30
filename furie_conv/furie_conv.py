from math import *
import numpy as np
import matplotlib.pyplot as plt

# sin(x)
def first_func(x):
    return sin(x)


# sin(3x)
def second_func(x):
    return sin(3 * x)

# sin(x) + sin(3x)
def sum_func(x):
    return first_func(x) + second_func(x)

def first_then_second_func(x):
    return second_func(x) if x > 0 else first_func(x)


def furie_func(f, x, omega):
    res = 0

    for i in x:
        res += f(i) / exp(i * omega)
    return res / sqrt(2 * pi)


def show_graphic(y_lst, x_lst, str_y, str_x, ax):
    x = np.array(x_lst)
    y = np.array(y_lst)

    ax.plot(x, y)

    ax.set_ylabel(str_y)
    ax.set_xlabel(str_x)

    ax.grid(True)


if __name__ == '__main__':
    fig, ax = plt.subplots(nrows=2, ncols=2)

    t = [i for i in np.arange(-10, 11)]

    omega = [i for i in np.arange(0, 101)]


    show_graphic([sum_func(i) for i in t], t, 'sin(x) + sin(3x)', 't', ax[0][0])

    show_graphic([first_then_second_func(i) for i in t], t, 'sin(x), then sin(3x)', 't', ax[0][1])

    show_graphic([furie_func(sum_func, t, i) for i in omega], omega, 'FFT1', 'Гц', ax[1][0])

    show_graphic([furie_func(first_then_second_func, t, i) for i in omega], omega, 'FFT2', 'Гц', ax[1][1])

    plt.show()