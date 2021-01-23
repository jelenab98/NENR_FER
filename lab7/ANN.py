import numpy as np


def sigmoid(x):
    return np.reciprocal(np.add(1, np.exp(-x)))


def d_sigmoid(x):
    return x * (1 - x)


def custom_activation(x, w, s):
    return 1/(1 + np.sum(np.abs(x - w)/np.abs(s), axis=0))


def calculate_params(layers):
    result = layers[0]*layers[0]*layers[1]
    for idx in range(2, len(layers)):
        result += layers[idx]*layers[idx - 1]
    return result


class NewNeuralNetwork:
    """
    Class of the ANN model with matrix representation of the parameters.
    """
    def __init__(self, layers, params=None, input_file=None):
        self.layers = layers
        self.params = None
        self.outputs = []
        if input_file:
            self.load_params(input_file)
            self.n_params = self.params.shape[0]
        else:
            self.n_params = params
            self.params = np.random.uniform(-3, 3, (self.n_params, 1))

        self.coords_list = []
        self.pomak = self.layers[0]*self.layers[0]
        for i in range(self.pomak):
            tmp_list = list(range(i, self.layers[1]*self.pomak + i, self.pomak))
            self.coords_list.append(tmp_list)

    def load_params(self, input_file):
        """
        Helper method for loading the data.
        :param input_file: path to file
        :return:
        """
        with open(input_file, 'r') as f:
            lines = f.readlines()
        self.params = np.zeros((len(lines), 1))
        for idx, line in enumerate(lines):
            self.params[idx, 0] = float(line.strip('\n'))

    def save_params(self, output_file):
        """
        Helper method for saving the data.
        :param output_file: path to file
        :return:
        """
        with open(output_file, 'w') as f:
            for i in range(self.params.shape[0]):
                f.write("{}\n".format(self.params[i, 0]))

    def predict(self, x):
        """
        Predictions for the input x
        :param x: input coordinates
        :return:
        """
        self.forward_pass(x)
        return self.outputs[-1]

    def calculate_error(self, x, y):
        """
        Calculation of the MSE for the predictions and ground truth data.
        :param x: input data
        :param y: ground truth data
        :return: MSE of predictions and GT
        """
        self.forward_pass(x)
        return np.mean(np.square(y - self.outputs[-1]))

    def predict_one_hot(self, x):
        """
        One-hot encoded predictions for the given input x.
        :param x: input coordinates
        :return:
        """
        return np.where(self.predict(x) < 0.5, 0, 1)

    def calculate_one_hot_error(self, x, y):
        """
        Accuracy calculation for the one-hot encoded data
        :param x: input coordinates
        :param y: GT data
        :return: accuracy of the model
        """
        preds = self.predict_one_hot(x)
        correct = 0
        for i in range(y.shape[1]):
            if np.array_equal(preds[:, i], y[:, i]):
                correct += 1
        return correct/y.shape[1]

    def forward_pass(self, x):
        """
        Forward pass through the model.
        :param x: input coordinates
        :return:
        """
        coordinate_weights = np.zeros((self.layers[0], self.layers[1]))
        coordinate_variance = np.zeros((self.layers[0], self.layers[1]))
        weights = []
        for i in range(self.layers[0]):
            coordinate_weights[i, :] = self.params[self.coords_list[i], 0]
            coordinate_variance[i, :] = self.params[self.coords_list[i + self.layers[0]], 0]
        tmp_idx = self.pomak*self.layers[1]
        for idx in range(len(self.layers) - 2):
            dims = (self.layers[idx + 2], self.layers[idx + 1])
            #print(dims, dims[0]*dims[1])
            d = self.params[tmp_idx: tmp_idx + self.layers[idx + 2]*self.layers[idx + 1]]
            #print(self.params[self.pomak*self.layers[1]: self.pomak*self.layers[1] + dims[0]*dims[1]].shape)
            weights.append(np.reshape(d, dims))
            tmp_idx += self.layers[idx + 2]*self.layers[idx + 1]

        net = np.zeros((self.layers[1], x.shape[1]))
        for i in range(x.shape[1]):
            x_tmp = x[:, i]
            x_tmp = np.expand_dims(x_tmp, axis=1)
            net_tmp = custom_activation(x_tmp, coordinate_weights, coordinate_variance)
            net[:, i] = net_tmp

        self.outputs = [net]
        for idx in range(len(weights)):
            net = sigmoid(np.matmul(weights[idx], net))
            self.outputs.append(net)
        return
