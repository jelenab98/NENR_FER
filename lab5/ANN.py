import numpy as np
import random


class Sigmoid:
    """
    Sigmoid activation function for ANN.
    """
    def __init__(self, a=1):
        self.a = a

    def calculate(self, x):
        return np.reciprocal(np.add(1, np.exp(-x)))

    def derivate(self, x):
        return x*(1 - x)


class NeuralNetwork:
    """
    Class for feed forward fully connected neural network.
    Layers with custom activation functions can be constructed. Learning is achieved with backpropagation algorithm.
    Calculation of backpropagation is done in matrix form.
    """
    def __init__(self, layers, activations, weight_file=None):
        self.layers = layers
        self.activations = activations
        self.weights = []
        self.gradients = []
        self.activation_outputs = []
        self.outputs = []
        if weight_file is not None:
            self.load_weights(weight_file)
        else:
            self.initialize_weights()

    def load_weights(self, input_file):
        """
        Helper method for loading pretrained weights.
        :param input_file: path to file with pretrained weights
        :return:
        """
        self.weights = []
        with open(input_file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            w_rows = line.strip('\n').split(',')
            n = len(w_rows)
            m = len(w_rows[0].split(' '))
            tmp_arr = np.zeros((n, m))
            for i, w_row in enumerate(w_rows):
                w_elements = w_row.split(' ')
                for j, w_element in enumerate(w_elements):
                    tmp_arr[i, j] = float(w_element)
            self.weights.append(np.copy(tmp_arr))

    def save_weights(self, output_file):
        """
        Helper method for saving weights after training.
        :param output_file: path to file where the weights will be stored
        :return:
        """
        with open(output_file, 'w') as f:
            for idx, layer in enumerate(self.weights):
                s = ''
                for i in range(layer.shape[0]):
                    for j in range(layer.shape[1]):
                        s += "{} ".format(layer[i, j])
                    s = s.strip(' ')
                    s += ','
                s = s.strip(',')
                if idx != len(self.layers) - 1:
                    s += '\n'
                f.write(s)

    def initialize_weights(self, w_min=-0.001, w_max=0.001):
        """
        Initialization of weights to random values around zero.
        :param w_min: minimum value of weights
        :param w_max: maximum value of weights
        :return:
        """
        for idx in range(len(self.layers) - 1):
            self.weights.append(np.random.uniform(w_min, w_max, (self.layers[idx+1], self.layers[idx])))

    def forward_pass(self, x):
        """
        Forward pass in which activation outputs are calculated and stored.
        :param x: input examples - activations of first neurons
        :return:
        """
        net = np.copy(x)
        self.activation_outputs = []
        for idx in range(len(self.weights)):
            net = self.activations[-1].calculate(np.matmul(self.weights[idx], net))
            self.activation_outputs.append(net)
        return

    def backward_pass(self, x, y):
        """
        Backward pass in which error values and gradients are calculated and stored.
        :param x: input examples - activations of first neurons
        :param y: ground truth labels/values for corresponding input examples
        :return: temporary gradients for the given inputs
        """
        self.gradients = []
        errors = [None] * len(self.weights)
        errors[-1] = (self.activation_outputs[-1] - y)*self.activations[-1].derivate(self.activation_outputs[-1])

        for idx in reversed(range(len(errors) - 1)):
            errors[idx] = self.activations[-1].derivate(self.activation_outputs[idx])*(
                np.matmul(self.weights[idx + 1].T, errors[idx+1]))

        self.gradients.append(np.matmul(errors[0], x.T))

        for i, error in enumerate(errors[1:]):
            self.gradients.append(np.matmul(error, self.activation_outputs[i].T))
        return

    def predict(self, x):
        """
        Predictions calculated by network.
        :param x: input examples for which the predictions are desired.
        :return:
        """
        self.forward_pass(x)
        return self.activation_outputs[-1]

    def update_weights(self, lr):
        """
        Final step of backpropagation algorithm. Weights are updated according to calculated gradients and learning rate
        :param lr: learning rate
        :return:
        """
        for idx in range(len(self.weights)):
            self.weights[idx] = np.add(self.weights[idx], -lr*self.gradients[idx])

    def train(self, x, y, lr):
        """
        Train step for given inputs. Forward pass calculated the outputs from each layer and backward pass calculates
        the errors and gradients for each layer. Adjustment of weights is the last step.
        :param x: input examples
        :param y: ground truths for given inputs
        :param lr: learning rate
        :return:
        """
        self.forward_pass(x)
        self.backward_pass(x, y)
        self.update_weights(lr)


def train(dataset, model, algorithm='mini-batch', epochs=30, lr=0.001, batch_size=9, stop_value=0.002):
    """
    Helper method for training the network. 3 different train methods can be achieved - SGD, mini-Batch and Batch.
    :param dataset: training examples with ground truths
    :param model: ANN model
    :param algorithm: mini-batch | SGD | batch - method for training
    :param epochs: number of epochs for iteration
    :param lr: learning rate
    :param batch_size: dimension of batch size for mini-batch approach
    :param stop_value: minimum value of MSE to stop the training process
    :return:
    """
    X, y = dataset
    for epoch in range(epochs):
        if algorithm == 'SGD':
            examples = list(range(X.shape[1]))
            random.shuffle(examples)
            for j in examples:
                X_tmp = X[:, j]
                X_tmp = np.expand_dims(X_tmp, axis=1)
                y_tmp = y[:, j]
                y_tmp = np.expand_dims(y_tmp, axis=1)
                model.train(X_tmp, y_tmp, lr)
        elif algorithm == "mini-batch":
            for i in range(0, 20, 2):
                tmp_list = [i, i+1, i+20, i+21, i+40, i+41, i+60, i+61, i+80, i+81]
                X_tmp = X[:, tmp_list]
                y_tmp = y[:, tmp_list]
                model.train(X_tmp, y_tmp, lr)
        else:
            model.train(X, y, lr)

        preds = model.predict(X)
        mse = np.mean(np.square(preds - y))

        if epoch % 2000 == 0:
            print("Epoch: {}/{}, MSE: {}".format(epoch, epochs, mse))
        if mse < stop_value:
            print("STOP: {}/{}, MSE: {}".format(epoch, epochs, mse))
            break
