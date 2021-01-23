import numpy as np


class Dataset:
    """
    Klasa za lakše baratanjem dataseta koji je potreban za provedbu algoritma.
    """
    def __init__(self, dataset_file):
        self.dataset = None
        self.size = None
        self.load_data(dataset_file)

    def load_data(self, dataset_file):
        """
        Učitavanje podataka i smještanje u strukture.
        :param dataset_file: ulazna datoteka koja se čita
        :return:
        """
        with open(dataset_file, 'r') as f:
            lines = f.readlines()
        self.size = len(lines)
        self.dataset = np.zeros((self.size, 3))
        for i in range(self.size):
            elements = lines[i].strip().split('\t')
            for j in range(3):
                self.dataset[i, j] = float(elements[j])
        return

    def function(self, parameters):
        """
        Metoda koja implementira samo računanje funkcije. Računanje funkcije se provodi automatski nad cijelim skupom, a
        ne zasebno nad svakim primjerom.
        :param parameters: ulazna jedinka parametara beta
        :return: vrijednost funkcije za sve ulazne podatke skupa podataka
        """
        b0, b1, b2, b3, b4 = parameters
        x, y = self.dataset[:, 0], self.dataset[:, 1]

        first = np.sin(np.add(b0, np.multiply(b1, x)))
        second_top = np.multiply(b2, np.cos(np.multiply(x, np.add(b3, y))))
        second_bottom = np.reciprocal(np.add(1, np.power(np.e, np.square(np.subtract(x, b4)))))

        return np.add(first, np.multiply(second_top, second_bottom))

    def calculate(self, parameters):
        """
        Računanje funkcije kazne koja je definirana kao MSE - Mean Squared Error.
        :param parameters: ulazna jedinka
        :return: vrijednost funkcije kazne za tu jedinku
        """
        return np.square(self.function(parameters) - self.dataset[:, 2]).mean()

