from DataGenerator import *
from GUI import *
from ANN import *
import json


def get_config(config_file='config.json'):
    with open(config_file, 'r') as f:
        configs = json.load(f)
    return configs


def set_config(config_file='config.json'):
    configs = {"open_generator_gui": "y",
               "use_generated_data": "n",
               "representative_points": 30,
               "input_dataset_file": "full_data.txt",
               "output_dataset_file": None,
               "layers": [60, 12, 5],
               "load_weights_file": None,
               "save_weights_file": None,
               "algorithm": "mini-batch",
               "lr": 0.01,
               "stop_error": 0.001,
               "epochs": 10000,
               "open_classifier_gui": "y"}

    with open(config_file, 'w') as f:
        json.dump(configs, f)


def main_example(configs):
    if configs["open_generator_gui"] == 'y':
        app = GenerateLettersApp()
        app.mainloop()
        if configs["use_generated_data"] == 'y':
            data = app.all_points
            dataset = GreekLetters(data=data, representative_points=configs['representative_points'],
                                   output_file=configs['output_dataset_file'])
    if configs['input_dataset_file'] is not None:
        dataset = GreekLetters(input_file=configs['input_dataset_file'])
    if configs['layers'][0] != 2*configs['representative_points']:
        configs["layers"][0] = 2*configs['representative_points']
    if configs["layers"][-1] != 5:
        configs["layers"][-1] = 5
    activation = Sigmoid()
    model = NeuralNetwork(layers=configs['layers'], activations=[activation for i in range(len(configs['layers']) - 1)])
    X = dataset.X.reshape((dataset.total_inputs, 2*dataset.m))
    y = dataset.y
    if configs['load_weights_file'] is not None:
        model.load_weights(configs['load_weights_file'])
    else:
        train(dataset=(X.T, y.T), model=model, algorithm=configs['algorithm'],
              epochs=configs['epochs'], lr=configs['lr'], stop_value=configs['stop_error'])
        if configs['save_weights_file'] is not None:
            model.save_weights(configs['save_weights_file'])
    if configs['open_classifier_gui'] == 'y':
        dataset2 = GreekLetters(representative_points=configs['representative_points'], mode="test")
        app = ClassifierApp(model, dataset2)
        app.mainloop()

    return


def quad_example():
    x = np.array([[-1], [-0.8], [-0.6], [-0.4], [-0.2], [0], [0.2], [0.4], [0.6]])
    y = np.array([[1], [0.64], [0.36], [0.16], [0.04], [0], [0.04], [0.16], [0.36]])
    acts = Sigmoid()
    model = NeuralNetwork([1, 6, 6, 1], [acts, acts, acts, acts, acts])
    train((x.T, y.T), model, algorithm="batch", lr=0.5, stop_value=0.0001, epochs=750000)
    pred = model.predict(x.T)
    print("{:^10} | {:^10} | {:^10}".format("Input", "GT", "Prediction"))
    print("-" * 36)
    for i in range(x.shape[0]):
        print("{:^10.2f} | {:^10.2f} | {:^10.2f}".format(x[i, 0], y[i, 0], pred[0, i]))
    return


if __name__ == '__main__':
    data_configs = get_config('config.json')
    main_example(data_configs)
    # quad_example()
