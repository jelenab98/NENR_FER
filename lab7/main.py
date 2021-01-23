from ANN import *
from DataLoader import *
from GeneticAlgorithm import *


if __name__ == '__main__':
    d = Dataset(2, 3)
    d.load("zad7-dataset.txt")
    layers = [2, 8, 4, 3]
    params = calculate_params(layers)
    model = NewNeuralNetwork(layers, params=params)
    ga = EliminationGA(d, model, 50, params, 0.1, 0.05, 0.95, 0.05, 1e6, 1e-3, 4, 3, 1, True)
    ga.calculate()
    tocnost = model.calculate_one_hot_error(d.x, d.y)
    print("Tocnost modela na skupu za ucenje je: {}".format(tocnost))
    model.save_params("2_84_3_novi2.txt")
    coordinate_weights = np.zeros((layers[0], layers[1]))
    coordinate_variance = np.zeros((layers[0], layers[1]))
    weights = []
    for i in range(layers[0]):
        coordinate_weights[i, :] = model.params[model.coords_list[i], 0]
        coordinate_variance[i, :] = model.params[model.coords_list[i + model.layers[0]], 0]
    print(coordinate_weights)
    print()
    print(coordinate_variance)
    d.vizualise(coordinate_weights[0, :], coordinate_weights[1, :], "Arhitektura mreže: {}".format(layers))
