import numpy as np


class DataLoader:
    def __init__(self, m, n, low=-4, high=4):
        self.n = n
        self.m = m
        self.low = low
        self.high = high
        self.x = None
        self.y = None
        self.z = None

    @staticmethod
    def f(x, y):
        return ((x - 1) ** 2 + (y + 2) ** 2 - 5 * x * y + 3) * np.cos(x / 5) ** 2

    def construct(self):
        """
        Constructing the data.
        :return:
        """
        x = np.arange(self.low, self.high+1)
        x = np.repeat(x, 1 + self.high - self.low, axis=0)
        x = np.expand_dims(x, axis=0)
        y = np.arange(self.low, self.high+1)
        y = np.tile(y, 1 + self.high - self.low)
        y = np.expand_dims(y, axis=0)
        self.z = self.f(x, y)
        self.x = np.repeat(x, self.m, axis=0)
        self.y = np.repeat(y, self.m, axis=0)

    def save_data(self, output_file):
        """
        Helper function to load the data.
        :param output_file: path to file for loading the data
        :return:
        """
        with open(output_file, 'w') as f:
            for i in range(self.n):
                f.write("{} {} {}\n".format(self.x[0, i], self.y[0, i], self.z[0, i]))

    def load_data(self, input_file):
        """
        Helper function to save the constructed data.
        :param input_file: path to file for saving the data
        :return:
        """
        x = np.zeros((1, self.n))
        y = np.zeros((1, self.n))
        self.z = np.zeros((1, self.n))
        with open(input_file, 'r') as f:
            lines = f.readlines()
        for idx, line in enumerate(lines):
            x_i, y_i, z_i = line.strip('\n').split(' ')
            x[0, idx] = float(x_i)
            y[0, idx] = float(y_i)
            self.z[0, idx] = float(z_i)

        self.x = np.repeat(x, self.m, axis=0)
        self.y = np.repeat(y, self.m, axis=0)
