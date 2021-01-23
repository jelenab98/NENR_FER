import matplotlib.pyplot as plt
import numpy as np


def y(x, s):
    return 1/(1 + np.abs(x - 2)/np.abs(s))


def plot_s():
    x = np.linspace(-8, 10, 1000)
    s_1 = y(x, 1)
    s_025 = y(x, 0.25)
    s_4 = y(x, 4)

    fig = plt.figure(figsize=(8, 6))
    plt.plot(x, s_025, label="s = 0.25", color="purple")
    plt.plot(x, s_1, label="s = 1", color="magenta")
    plt.plot(x, s_4, label="s = 4", color="pink")
    plt.legend()
    plt.xlim(-8, 10)
    plt.show()

if __name__ == '__main__':
    x = np.expand_dims(np.array([1, 2]), axis=1)
    xx = np.repeat(x, 9, axis=1)
    w_i = np.ones((2, 8))
    print(xx - w_i)
