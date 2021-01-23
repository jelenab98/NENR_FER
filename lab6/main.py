import numpy as np
import random
from DataLoader import DataLoader
from ANFIS import ANFIS
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import sys


def train(dataset, model, algorithm='batch', epochs=30, lr1=0.001, lr2 = 0.01, stop_value=0.002):
    x, y, z = dataset
    mse_list = []
    for epoch in range(epochs + 1):
        if algorithm == 'SGD':
            examples = list(range(x.shape[1]))
            random.shuffle(examples)
            # examples = range(x.shape[1])
            for j in examples:
                x_tmp = x[:, j]
                x_tmp = np.expand_dims(x_tmp, axis=1)
                y_tmp = y[:, j]
                y_tmp = np.expand_dims(y_tmp, axis=1)
                z_tmp = z[:, j]
                z_tmp = np.expand_dims(z_tmp, axis=1)
                model.train(x_tmp, y_tmp, z_tmp, lr1, lr2)
        else:
            model.train(x, y, z, lr1, lr2)

        preds = model.predict(x, y)
        mse = 0.5*np.mean(np.square(preds - z))
        mse_list.append(mse)
        if epoch % 100 == 0:
            print("Epoch: {}/{}, MSE: {}".format(epoch, epochs, mse))
        if mse < stop_value:
            print("STOP: {}/{}, MSE: {}".format(epoch, epochs, mse))
            break
    return mse_list


def sig(a, b, x):
    return 1/(1 + np.exp(b*(x - a)))


def plot_sig(a, b, c, d, x, y):
    y1 = []
    y2 = []
    for i in range(len(a)):
        y1_tmp = []
        y2_tmp = []
        for j in range(len(x)):
            prvi = sig(a[i], b[i], x[j])
            drugi = sig(c[i], d[i], y[j])
            y1_tmp.append(prvi)
            y2_tmp.append(drugi)
        y1.append(y1_tmp)
        y2.append(y2_tmp)

    z = []
    for a1, a2 in zip(y1, y2):
        tmp_z = []
        for a11, a22 in zip(a1, a2):
            tmp_z.append(a11*a22)
        z.append(tmp_z)

    plt.figure(figsize=(15, 10))
    for idx, a1 in enumerate(z):
        plt.plot(x, a1, label="Pravilo {}".format(idx +1))

    plt.legend()
    plt.show()
    figure = plt.figure(figsize=(15, 10))
    plt.subplot(2, 1, 1)
    plt.title("Funkcije pripadnosti za ulaz x")
    for idx, a1 in enumerate(y1):
        plt.plot(x, a1, label="Pravilo {}".format(idx + 1))
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.title("Funkcije pripadnosti za ulaz y")
    for idx, a2 in enumerate(y2):
        plt.plot(y, a2, label="Pravilo {}".format(idx+1))
    plt.legend()

    plt.show()


def plot_errors(mse_sgd, mse_batch, epochs_sgd, epochs_batch, dod):
    figure = plt.figure(figsize=(10, 4))
    #plt.plot(range(epochs_batch + 1), dod, label='Velika stopa učenja')
    plt.plot(range(epochs_sgd+1), mse_sgd, label="SGD")
    plt.plot(range(epochs_batch+1), mse_batch, label="Batch")
    plt.title("Usporedba greške za različite verzije algoritama učenja")
    plt.legend()
    plt.show()


def plot_gt(x, y, z,outputs):
    figure = plt.figure(figsize=(10, 8))
    ax = plt.axes(projection="3d")
    ax.plot3D(x, y, z, label='GT')
    ax.plot3D(x, y, outputs, label='Predikcija')
    plt.legend()
    plt.show()


def save_errors(mse, filee):
    with open(filee, 'w') as f:
        for m in mse:
            f.write("{}\n".format(m))


def load_errors(input_file):
    error = []
    with open(input_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        error.append(float(line.strip('\n')))

    return error


def save_outputs(outputs, filee):
    with open(filee, 'w') as f:
        for i in range(outputs.shape[1]):
            f.write("{}\n".format(outputs[0, i]))


def load_outputs(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    outs = np.zeros((1, 81))
    for idx in range(len(lines)):
        outs[0, idx] = float(lines[idx].strip('\n'))
    return outs


def save_coeffs(model, output_file):
    with open(output_file, 'w') as f:
        for i in range(model.n_rules):
            f.write("{} {} {} {}\n".format(model.a[i, 0], model.b[i, 0], model.c[i, 0], model.d[i, 0]))


def load_coeffs(input_file):
    a = []
    b = []
    c = []
    d = []
    with open(input_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        a_i, b_i, c_i, d_i= line.strip('\n').split(' ')
        a.append(float(a_i))
        b.append(float(b_i))
        c.append(float(c_i))
        d.append(float(d_i))
    return a, b, c, d


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        print("Krivi broj parametara!")
        exit()
    m = int(args[1])
    da = DataLoader(m, 81, -4, 4)
    da.construct()
    x = da.x[0, :]
    y = da.y[0, :]
    z = da.z[0, :]

    anfis = ANFIS(m)
    res = train((da.x, da.y, da.z), anfis, algorithm='batch', epochs=1000, lr1=5e-4, lr2=1e-3)
    preds = anfis.predict(da.x, da.y)
    plot_gt(x, y, z, preds[0, :])

    anfis = ANFIS(m)
    res2 = train((da.x, da.y, da.z), anfis, algorithm='SGD', epochs=1000, lr1=5e-4, lr2=1e-3)
    preds = anfis.predict(da.x, da.y)
    plot_gt(x, y, z, preds[0, :])

