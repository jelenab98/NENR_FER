import numpy as np
import matplotlib.pyplot as plt


class GreekLetters:
    """
    Custom dataset class for preprocessing, saving and loading the dataset of Handwritten Greek letter - a, b, g, d, e.
    """
    def __init__(self, data=None, representative_points=30, input_file=None, output_file=None, mode="train"):
        self.input_file = input_file
        self.output_file = output_file
        self.current_input = 0
        self.tmp_array = None
        self.approx_distances = None
        self.label = None
        self.m = representative_points
        if mode == 'test':
            self.data = data
            self.total_inputs = 1
            self.X = np.zeros(shape=(1, representative_points, 2))
            self.y = np.zeros(shape=(1, 5))

        else:
            if input_file:
                self.load()
            else:
                self.data = data
                self.total_inputs = sum([len(data[x]) for x in data])
                self.X = np.zeros(shape=(self.total_inputs, representative_points, 2))
                self.y = np.zeros(shape=(self.total_inputs, 5))

    def process_for_test(self, data):
        """
        Processing the data in test mode
        :param data: inputs from GUI Render.
        :return:
        """
        self.data = data
        self.normalize_points(self.data)
        self.calculate_distances()
        approx_distance = np.sum(self.approx_distances)
        tmp_step = approx_distance / (self.m - 1)

        self.X[self.current_input, 0] = self.tmp_array[0]
        self.X[self.current_input, -1] = self.tmp_array[-1]
        self.y[self.current_input] = self.label
        tmp_distance = 0
        idx = 0

        for i in range(1, self.m - 1):
            k = i * tmp_step
            while tmp_distance <= k:
                idx += 1
                tmp_distance += self.approx_distances[idx]
            self.X[self.current_input, i] = self.tmp_array[idx]

    def process_data(self):
        """
        Processing the data in train mode.
        :return:
        """
        for greek_letter, all_points in self.data.items():
            self.make_one_hot_encoded_label(greek_letter)
            for points in all_points:
                self.normalize_points(points)
                self.calculate_distances()
                approx_distance = np.sum(self.approx_distances)
                tmp_step = approx_distance / (self.m - 1)

                self.X[self.current_input, 0] = self.tmp_array[0]
                self.X[self.current_input, -1] = self.tmp_array[-1]
                self.y[self.current_input] = self.label
                tmp_distance = 0
                idx = 0

                for i in range(1, self.m-1):
                    k = i*tmp_step
                    while tmp_distance <= k:
                        idx += 1
                        tmp_distance += self.approx_distances[idx]
                    self.X[self.current_input, i] = self.tmp_array[idx]

                self.current_input += 1

    def calculate_distances(self):
        """
        Calculation of distances between points.
        :return:
        """
        self.approx_distances = np.linalg.norm(self.tmp_array[1:, :] - self.tmp_array[0:-1, :], axis=1)

    def normalize_points(self, points):
        """
        Normalization of points to range [-1, 1]
        :param points: points to process
        :return:
        """
        self.tmp_array = np.squeeze(np.array(points))
        self.tmp_array = np.subtract(self.tmp_array, self.tmp_array.mean(axis=(0, 1)))
        self.tmp_array = np.divide(self.tmp_array, np.max(np.abs(self.tmp_array)))

    def make_one_hot_encoded_label(self, greek_letter):
        """
        Calculating one hot encoded vectors for each letter.
        :param greek_letter:
        :return:
        """
        if greek_letter in ('alpha', "1.0 0.0 0.0 0.0 0.0"):
            self.label = np.array([1, 0, 0, 0, 0])
        elif greek_letter in ('beta', "0.0 1.0 0.0 0.0 0.0"):
            self.label = np.array([0, 1, 0, 0, 0])
        elif greek_letter in ('gamma', "0.0 0.0 1.0 0.0 0.0"):
            self.label = np.array([0, 0, 1, 0, 0])
        elif greek_letter in ("delta", "0.0 0.0 0.0 1.0 0.0"):
            self.label = np.array([0, 0, 0, 1, 0])
        else:
            self.label = np.array([0, 0, 0, 0, 1])

    def get_label(self, one_hot_encoded_label):
        """
        Defining label for given one hot encoded vector.
        :param one_hot_encoded_label:
        :return:
        """
        if np.array_equal(one_hot_encoded_label, np.array([1, 0, 0, 0, 0])):
            return "alpha"
        elif np.array_equal(one_hot_encoded_label, np.array([0, 1, 0, 0, 0])):
            return "beta"
        elif np.array_equal(one_hot_encoded_label, np.array([0, 0, 1, 0, 0])):
            return "gamma"
        elif np.array_equal(one_hot_encoded_label, np.array([0, 0, 0, 1, 0])):
            return "delta"
        else:
            return "epsilon"

    def save(self):
        """
        Helper method for saving the dataset.
        :return:
        """
        with open(self.output_file, 'w') as f:
            for idx in range(self.total_inputs):
                output_string = ""
                for i in range(self.m):
                    output_string += "{} {},".format(self.X[idx, i, 0], self.X[idx, i, 1])
                output_string += "{} {} {} {} {}\n".format(self.y[idx, 0], self.y[idx, 1], self.y[idx, 2],
                                                           self.y[idx, 3], self.y[idx, 4])
                f.write(output_string)

    def load(self):
        """
        Helper method for loading the already processed dataset.
        :return:
        """
        with open(self.input_file, 'r') as f:
            lines = f.readlines()

        self.total_inputs = len(lines)
        self.X = np.zeros(shape=(self.total_inputs, self.m, 2))
        self.y = np.zeros(shape=(self.total_inputs, 5))

        for line in lines:
            elements = line.strip('\n').split(',')
            letters = elements[-1]
            self.make_one_hot_encoded_label(letters)
            self.y[self.current_input] = self.label
            for idx, element in enumerate(elements[0:-1]):
                x, y = element.strip().split(' ')
                self.X[self.current_input, idx] = np.array([float(x), float(y)])
            self.current_input += 1

    def visualize_dataset(self):
        """
        Visualization of data points.
        :return:
        """
        figure = plt.figure(figsize=(16, 20))
        for i in range(1, 5):
            plt.subplot(2, 2, i)
            plt.plot(self.X[i * 3, :, 0], -1 * self.X[i * 3, :, 1], color='pink')
            plt.scatter(self.X[i*3, :, 0], -1*self.X[i*3, :, 1], color='violet')
            plt.title("{}".format(self.get_label(self.y[i*3])))
        plt.show()
