import numpy as np


class ANFIS:
    """
    Class for the ANFIS model with the TSK conclusion.
    """
    def __init__(self, number_of_rules):
        self.n_rules = number_of_rules
        self.a = np.random.uniform(-1, 1, (number_of_rules, 1))
        self.b = np.random.uniform(-1, 1, (number_of_rules, 1))
        self.c = np.random.uniform(-1, 1, (number_of_rules, 1))
        self.d = np.random.uniform(-1, 1, (number_of_rules, 1))
        self.p = np.random.uniform(-1, 1, (number_of_rules, 1))
        self.q = np.random.uniform(-1, 1, (number_of_rules, 1))
        self.r = np.random.uniform(-1, 1, (number_of_rules, 1))
        self.w, self.w1, self.w2 = None, None, None
        self.f, self.o = None, None

    def zero_grads(self):
        """
        Function for setting all the gradients to zero. Used at the beginning of the each backward pass.
        :return:
        """
        self.a_grads = np.zeros((self.n_rules, 1))
        self.b_grads = np.zeros((self.n_rules, 1))
        self.c_grads = np.zeros((self.n_rules, 1))
        self.d_grads = np.zeros((self.n_rules, 1))
        self.p_grads = np.zeros((self.n_rules, 1))
        self.q_grads = np.zeros((self.n_rules, 1))
        self.r_grads = np.zeros((self.n_rules, 1))

    def get_rule_value_x(self, x):
        """
        Calculation of the sigmoid function for the x coordinates.
        :param x:
        :return:
        """
        return np.reciprocal(np.add(1, np.exp(np.multiply(self.b, np.subtract(x, self.a)))))

    def get_rule_value_y(self, y):
        """
        Calculation of the sigmoid function for the y coordinates.
        :param y: y coordinates
        :return:
        """
        return np.reciprocal(np.add(1, np.exp(np.multiply(self.d, np.subtract(y, self.c)))))

    def forward_pass(self, x, y):
        """
        Forward pass through the model
        :param x: x coordinates
        :param y: y coordinates
        :return:
        """
        self.w1 = self.get_rule_value_x(x)
        self.w2 = self.get_rule_value_y(y)
        self.w = np.multiply(self.w1, self.w2)
        self.f = np.multiply(self.p, x) + np.multiply(self.q, y) + self.r
        self.o = np.sum(np.multiply(self.w, self.f), axis=0) / np.sum(self.w, axis=0)
        self.o = np.expand_dims(self.o, axis=0)
        return

    def backward_pass(self, x, y, z):
        """
        Backward pass where the gradients are calculated according to the formulas written in the report.
        :param x: x coordinates
        :param y: y coordinates
        :param z: z coordinates (ground truth)
        :return:
        """
        self.zero_grads()
        for j in range(x.shape[1]):
            x_tmp = x[:, j]
            y_tmp = y[:, j]
            z_tmp = z[:, j]
            x_tmp = np.expand_dims(x_tmp, axis=1)
            y_tmp = np.expand_dims(y_tmp, axis=1)
            z_tmp = np.expand_dims(z_tmp, axis=1)
            self.forward_pass(x_tmp, y_tmp)
            x_tmp = x_tmp[0, 0]
            y_tmp = y_tmp[0, 0]
            z_tmp = z_tmp[0, 0]
            d_o = -(z_tmp - self.o)
            for i in range(self.n_rules):
                d_pi = (np.sum(self.w*(np.subtract(self.f[i], self.f))))/(np.sum(self.w))
                d_alpha = self.w2[i]
                d_beta = self.w1[i]
                d_a = self.b[i]*self.w1[i]*(1 - self.w[i])
                d_b = -(x_tmp - self.a[i])*self.w1[i]*(1 - self.w1[i])
                d_c = self.d[i]*self.w2[i]*(1 - self.w2[i])
                d_d = -(y_tmp - self.c[i])*self.w2[i]*(1 - self.w2[i])
                d_z = (self.w[i])/(np.sum(self.w))
                d_p = x_tmp
                d_q = y_tmp
                d_r = 1
                self.a_grads[i, 0] = self.a_grads[i, 0] + d_o*d_pi*d_alpha*d_a
                self.b_grads[i, 0] = self.b_grads[i, 0] + d_o*d_pi*d_alpha*d_b
                self.c_grads[i, 0] = self.c_grads[i, 0] + d_o*d_pi*d_beta*d_c
                self.d_grads[i, 0] = self.d_grads[i, 0] + d_o*d_pi*d_beta*d_d
                self.p_grads[i, 0] = self.p_grads[i, 0] + d_o*d_z*d_p
                self.q_grads[i, 0] = self.q_grads[i, 0] + d_o*d_z*d_q
                self.r_grads[i, 0] = self.r_grads[i, 0] + d_o*d_z*d_r
        return

    def update_weights(self, lr1, lr2):
        """
        Method for updating the gradients
        :param lr1: learning rate for the sigmoid functions
        :param lr2: learning rate for the z function
        :return:
        """
        self.a = self.a - lr1 * self.a_grads
        self.b = self.b - lr1 * self.b_grads
        self.c = self.c - lr1 * self.c_grads
        self.d = self.d - lr1 * self.d_grads
        self.p = self.p - lr2 * self.p_grads
        self.q = self.q - lr2 * self.q_grads
        self.r = self.r - lr2 * self.r_grads
        return

    def train(self, x, y, z, lr, lr2):
        """
        Train step function
        :param x: x coordinates
        :param y: y coordinates
        :param z: z coordinates (ground truth)
        :param lr: learning rate for sigmoid functions
        :param lr2: learning rate for z function
        :return:
        """
        self.backward_pass(x, y, z)
        self.update_weights(lr, lr2)
        return

    def predict(self, x, y):
        """
        Predict function for given input data.
        :param x: x coordinates
        :param y: y coordinates
        :return: predictions of the z coordinate
        """
        self.forward_pass(x, y)
        return self.o
