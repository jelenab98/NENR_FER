from GeneticAlgorithm import *
from DataLoaders import *
from matplotlib import pyplot as plt


def show_genes(ga_class: GeneticAlgorithm):
    """
    Pomocna metoda koja sluzi za vizualizaciju ground truth podataka i predikcija algoritma.
    :param ga_class: primjerak klase genetskog algoritma
    :return:
    """
    best_gene = ga_class.population[ga_class.best_index]
    predictions = ga_class.data.function(best_gene)
    gt = ga_class.data.dataset[:, 2]

    fig, axs = plt.subplots(3)
    axs[0].plot(range(250), predictions, 'violet', label='Predikcije')
    axs[1].plot(range(250), gt, 'black', label='GT')
    axs[2].plot(range(250), predictions, 'violet', label='Predikcije')
    axs[2].plot(range(250), gt, 'black', label='GT', linestyle=':')
    fig.suptitle("Predikcije i GT za parametre najbolje jedinke uz MSE: {}".format(ga_class.min_error))
    plt.xlabel("Primjeri iz skupa podataka")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    type_dataset = input("Odaberite dataset za učenje (1 ili 2) >> ")
    if type_dataset == '1':
        dataset = Dataset('zad4-dataset1.txt')
    elif type_dataset == '2':
        dataset = Dataset('zad4-dataset2.txt')
    else:
        print("Krivi odabir dataseta. Prekidam izvođenje.")
        raise ValueError
    type_ga = input('Odaberite vrstu genetskog algoritma (KA - kanonski, 3T - 3-turnirski) >> ')
    if type_ga == 'KA':
        elitism = input("Elitizam - y/n? ")
        flag = elitism.lower() == 'y'
        ga = GenerationGA(dataset, elitism=flag)
    elif type_ga == '3T':
        ga = EliminationGA(dataset)
    else:
        print("Krivi odabir. Zaustavljam izvođenje.")
        raise ValueError
    ga.calculate()
    show_genes(ga)
