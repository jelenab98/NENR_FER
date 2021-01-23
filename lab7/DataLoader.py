import numpy as np
import matplotlib.pyplot as plt


class Dataset:
    def __init__(self, m, classes):
        self.m = m
        self.n_classes = classes
        self.x = None
        self.y = None
        self.n = None

    def load(self, input_file):
        """
        Function for loading the data.
        :param input_file: path to file
        :return:
        """
        with open(input_file, 'r') as f:
            lines = f.readlines()

        self.n = len(lines)
        self.x = np.zeros((self.m, self.n))
        self.y = np.zeros((self.n_classes, self.n), dtype=int)
        row_counts = self.m + self.n_classes
        for idx, line in enumerate(lines):
            elements = line.strip('\n').split('\t')
            for i in range(self.m):
                self.x[i, idx] = float(elements[i])
            for j in range(self.n_classes):
                self.y[j, idx] = int(elements[row_counts - self.n_classes + j])

    def vizualise(self, x, y, title):
        """
        Visualization of the dataset.
        :param x: x coordinates of the centroids
        :param y: y coordinate of the centroids
        :param title: title to show
        :return:
        """
        fig = plt.figure(figsize=(6, 4))
        ozn1 = np.array([1, 0, 0])
        ozn2 = np.array([0, 1, 0])
        ozn3 = np.array([0, 0, 1])
        o1, o2, o3 = False, False, False
        for i in range(self.n):
            if np.array_equal(self.y[:, i], ozn1):
                if o1:
                    plt.scatter(self.x[0, i], self.x[1, i], color="purple")
                else:
                    o1 = True
                    plt.scatter(self.x[0, i], self.x[1, i], color="purple", label="A")
            elif np.array_equal(self.y[:, i], ozn2):
                if o2:
                    plt.scatter(self.x[0, i], self.x[1, i], color="magenta")
                else:
                    o2 = True
                    plt.scatter(self.x[0, i], self.x[1, i], color="magenta", label="B")
            else:
                if o3:
                    plt.scatter(self.x[0, i], self.x[1, i], color='pink')
                else:
                    o3 = True
                    plt.scatter(self.x[0, i], self.x[1, i], color="pink", label="C")
        plt.scatter(x, y, color="black")
        plt.title(title)
        plt.ylim(0, 1)
        plt.xlim(0, 1)
        plt.legend()
        plt.show()
