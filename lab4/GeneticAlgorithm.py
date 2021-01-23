import numpy as np
import random


class GeneticAlgorithm:
    """
    Klasa genetskog algoritma u kojoj su implementirane metode za križanje, mutaciju, generiranje populacije te
    apstraktna metoda koja je drukcija ovisno o tome implementira li se generacijski ili eliminacijski algoritam.
    """
    def __init__(self, dataset, population_size=30, gene_size=5, p_mutation=0.02, p_cross=0.95,
                 max_iter=100000, epsilon=5e-5):
        self.data = dataset
        self.gene_size = gene_size
        self.size = population_size
        self.p_mutation = p_mutation
        self.p_cross = p_cross
        self.max_iters = max_iter
        self.epsilon = epsilon
        self.population = np.zeros((population_size, gene_size))
        self.evals = dict()
        self.fitness = dict()
        self.min_error = np.inf
        self.best_index = -1

    def generate_population(self):
        """
        Generiranje random populacije. Veličina populacije određena je varijablom size, a veličina pojedina jedinke
        varijablom gene size. Pri stvaranju populacije, odmah evaluiramo i uspješnost te jedinke (kaznu) te njoj
        pripadnu mjeru dobrote (recipročna vrijednost kazne).
        :return:
        """
        for i in range(self.size):
            genes = np.random.uniform(-4, 4, (self.gene_size, 1))
            value = self.data.calculate(genes)
            self.evals[i] = value
            self.fitness[i] = np.reciprocal(value)
            self.population[i, :] = genes.squeeze()
            if value < self.min_error:
                self.min_error = value
                self.best_index = i

    def select_and_reproduce(self):
        """
        Apstraktna metoda za ostvarivanje selekcije i reprodukcije (križanje + mutacija)
        :return:
        """
        raise NotImplementedError

    def calculate(self):
        """
        Osnovni tijek rada genetskog algoritma. Svaku tisućitu iteraciju se ispisuje vrijednost novostvorene jedinke
        kao mjera kontrole rada algoritma. Algoritam pri kraju rada ispisuje podatke o najboljoj jedinki koja je
        pohranjena u varijabli best index.
        :return:
        """
        self.generate_population()
        i = 0
        while i < self.max_iters and self.min_error > self.epsilon:
            self.select_and_reproduce()
            if i % 1000 == 0:
                print("Iter: {}, min_error: {}".format(i, self.min_error))
            i += 1

        print("Finished! Iter: {}, min_error:{}, best_gene: {}".format(i, self.min_error,
                                                                       self.population[self.best_index]))

    def one_point_crossover(self, idx_parent1, idx_parent2):
        """
        Križanje s jednom točkom prekida. Prije točke prekida uzimaju se vrijednosti prvog roditelja, a nakon točke
        prekida vrijednosti drugog roditelja.
        :param idx_parent1: indeks prvog roditelja
        :param idx_parent2: indeks drugog roditelja
        :return: novostvoreno dijete
        """
        parent1 = self.population[idx_parent1, :]
        parent2 = self.population[idx_parent2, :]
        break_index = np.random.randint(0, self.gene_size)
        child = parent1.copy()
        child[break_index:] = parent2[break_index:]
        return child

    def discrete_recombination(self, idx_parent1, idx_parent2):
        """
        Diskretna rekombinacija u kojoj se nasmumičnim odabirom uzimaju vrijednosti prvog ili drugog roditelja i tako
        se formira genom djeteta.
        :param idx_parent1: indeks prvog roditelja
        :param idx_parent2: indeks drugog roditelja
        :return: novostvoreno dijete
        """
        parent1 = self.population[idx_parent1, :]
        parent2 = self.population[idx_parent2, :]
        child = np.array([np.random.choice([p1, p2]) for p1, p2 in zip(parent1, parent2)])
        return child

    def simple_arithmetic_recombination(self, idx_parent1, idx_parent2):
        """
        Jednostvna aritmetička rekombinacija u kojoj se odredi točka prekida. Prije točke prekida se uzimaju vrijednosti
        prvog roditelja, a nakon prekida artimetička sredina oba roditelja.
        :param idx_parent1: indeks prvog roditelja
        :param idx_parent2: indeks drugog roditelja
        :return: novostvoreno dijete
        """
        parent1 = self.population[idx_parent1, :]
        parent2 = self.population[idx_parent2, :]
        break_index = np.random.randint(0, self.gene_size)
        child = parent1.copy()
        child[break_index:] = (parent1[break_index:] + parent2[break_index:]) / 2
        return child

    def single_arithmetic_recombination(self, idx_parent1, idx_parent2):
        """
        Jednostruka aritmetička rekombinacija u kojoj se određuje indeks zamijene vrijednosti. U dijete se kopiraju
        vrijednosti prvog roditelja, a na nasumično odabrani indeks se kopira odgovarajuća vrijednost drugog roditelja.
        :param idx_parent1: indeks prvog roditelja
        :param idx_parent2: indeks drugog roditelja
        :return: novostvoreno dijete
        """
        parent1 = self.population[idx_parent1, :]
        parent2 = self.population[idx_parent2, :]
        child = parent1.copy()
        break_index = np.random.randint(0, self.gene_size)
        child[break_index] = parent2[break_index]
        return child

    def whole_arithmetic_recombination(self, idx_parent1, idx_parent2):
        """
        Potpuna artimetička rekombinacija u kojoj se dijete stvara kao aritmetička sredina oba roditelja.
        :param idx_parent1: indeks prvog roditelja
        :param idx_parent2: indeks drugog roditelja
        :return: novostvoreno dijete
        """
        parent1 = self.population[idx_parent1, :]
        parent2 = self.population[idx_parent2, :]
        child = (parent1+parent2) / 2
        return child

    def mutation(self, gene):
        """
        Jednostavna mutacija u kojoj se za svaki element gena gleda je li nasumično određena vjerojatnost manja od
        vjerojatnosti mutacija i ako je onda se taj element promijeni tako da mu se odredi nova vrijednost.
        :param gene: ulazni gen koji se mutira
        :return: mutirani gen
        """
        for i in range(self.gene_size):
            if np.random.uniform(0, 1) <= self.p_mutation:
                gene[i] = np.random.uniform(-4, 4)
        return gene

    def roulette_wheel_selection(self):
        """
        Selekcija po kriteriju kotača ruleta. Odredi se nasumična vrijednost funkcije dobrote i onda se kreće po kotaču
        tako da se ide po jedinkama u populaciji i provjerava se čiji raspon funkcije dobrote upada u odaberenu
        vrijednost.
        :return: indeks jedinke koja je selektirana
        """
        max_fitness = sum(self.fitness.values())
        random_pick = np.random.uniform(0, max_fitness)
        tmp_wheel = 0
        for idx, fitness in self.fitness.items():
            tmp_wheel += fitness
            if tmp_wheel > random_pick:
                return idx


class GenerationGA(GeneticAlgorithm):
    """
    Generacijski kanonski genetički algoritam koji koristi selekciju po kriteriju kotača ruleta. Kriterij križanja jest
    diskretna rekombinacija, a mutacija koja se provodi jest jednostavna mutacija. U ovom slučaju se vodi evidencija o
    staroj i novoj populaciji koja na kraju itercije postaje nova populacija. Ukoliko je odabereno svojstvo elitizma, u
    novu populaciju se prenosi jedna najbolja jedinka.
    """
    def __init__(self, dataset, population_size=30, gene_size=5, p_mutation=0.01, p_cross=0.95,
                 max_iter=50000, epsilon=4e-4, elitism=True):
        super().__init__(dataset, population_size, gene_size, p_mutation, p_cross, max_iter, epsilon)
        self.elitism = elitism

    def select_and_reproduce(self):
        new_population = np.zeros((self.size, self.gene_size))
        new_evals = dict()
        new_fitness = dict()
        new_min_error = np.inf
        new_best_index = -1
        idx = 0

        if self.elitism:
            new_population[0, :] = self.population[self.best_index, :]
            new_best_index = 0
            new_min_error = self.min_error
            idx += 1

        while idx < self.size:
            idx_parent1 = self.roulette_wheel_selection()
            idx_parent2 = self.roulette_wheel_selection()

            if np.random.uniform(0, 1) > self.p_cross:
                continue

            child = self.discrete_recombination(idx_parent1, idx_parent2)
            child = self.mutation(child)
            value = self.data.calculate(child)

            new_population[idx, :] = child
            new_evals[idx] = value
            new_fitness[idx] = np.reciprocal(value)

            if value < new_min_error:
                new_min_error = value
                new_best_index = idx

            idx += 1

        self.population = new_population
        self.evals = new_evals
        self.fitness = new_fitness
        self.best_index = new_best_index
        self.min_error = new_min_error
        return


class EliminationGA(GeneticAlgorithm):
    """
    Eliminacijski genetski algoritam koji koristi 3-turnisku selekciju kao kriterij selekcije, diskretnu rekombinaciju
    za križanje i jednostavnu mutaciju.
    """
    def select_and_reproduce(self):
        g1, g2, g3 = random.sample(range(self.size), 3)

        g1_eval = self.evals[g1]
        g2_eval = self.evals[g2]
        g3_eval = self.evals[g3]

        key_value = [(g1, g1_eval), (g2, g2_eval), (g3, g3_eval)]
        idx_worst = max(key_value, key=lambda x: x[1])[0]

        if idx_worst == g1:
            idx_parent1 = g2
            idx_parent2 = g3
        elif idx_worst == g2:
            idx_parent1 = g1
            idx_parent2 = g3
        else:
            idx_parent1 = g1
            idx_parent2 = g2

        child = self.discrete_recombination(idx_parent1, idx_parent2)
        child = self.mutation(child)
        value = self.data.calculate(child)

        self.population[idx_worst, :] = child
        self.evals[idx_worst] = value
        self.fitness[idx_worst] = np.reciprocal(value)

        if value < self.min_error:
            self.min_error = value
            self.best_index = idx_worst
        return
