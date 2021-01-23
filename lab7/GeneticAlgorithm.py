import numpy as np
import random


class GeneticAlgorithm:
    """
    Klasa genetskog algoritma u kojoj su implementirane metode za križanje, mutaciju, generiranje populacije te
    apstraktna metoda koja je drukcija ovisno o tome implementira li se generacijski ili eliminacijski algoritam.
    """
    def __init__(self, dataset, model, population_size=30, gene_size=56, p_mutation1=0.02, p_mutation2=0.01,
                 p_cross=0.95, p_mutation3=0.5, max_iter=100000, epsilon=5e-5, t1=2, t2=1, t3=1, elitism=True,
                 elitism_rate=0.5):
        self.data = dataset
        self.model = model
        self.gene_size = gene_size
        self.size = population_size
        self.elitism = elitism
        self.p_mutation1 = p_mutation1
        self.p_mutation2 = p_mutation2
        self.p_mutation3 = p_mutation3
        self.p_cross = p_cross
        self.max_iters = max_iter
        self.epsilon = epsilon
        self.elitism_rate = int(elitism_rate*population_size)
        self.v1 = t1/(t1 + t2 + t3)
        self.v2 = t2/(t1 + t2 + t3)
        self.v3 = t3/(t1 + t2 + t3)
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
            genes = np.random.uniform(-0.5, 1.5, (self.gene_size, 1))
            self.model.params = genes
            value = self.model.calculate_error(self.data.x, self.data.y)
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
            if (i/self.size) % 100 == 0:
                print("Iter: {}, min_error: {}".format(i, self.min_error))
            i += 1

        print("Finished! Iter: {}, min_error:{}".format(i, self.min_error))
        self.model.params = np.expand_dims(self.population[self.best_index], axis=1)

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
            if np.random.uniform(0, 1) <= self.p_mutation1:
                gene[i] = np.random.uniform(-4, 4)
        return gene

    def mutation1(self, gene, sigma1, flag):
        """
        Jednostavna mutacija u kojoj se za svaki element gena gleda je li nasumično određena vjerojatnost manja od
        vjerojatnosti mutacija i ako je onda se taj element promijeni tako da mu se odredi nova vrijednost.
        :param flag:
        :param sigma1:
        :param gene: ulazni gen koji se mutira
        :return: mutirani gen
        """
        for i in range(self.gene_size):
            if flag:
                if np.random.uniform(0, 1) <= self.p_mutation1:
                    gene[i] += np.random.normal(0, sigma1)
            else:
                if np.random.uniform(0, 1) <= self.p_mutation3:
                    gene[i] += np.random.normal(0, sigma1)
        return gene

    def mutation2(self, gene, sigma2):
        """
        Jednostavna mutacija u kojoj se za svaki element gena gleda je li nasumično određena vjerojatnost manja od
        vjerojatnosti mutacija i ako je onda se taj element promijeni tako da mu se odredi nova vrijednost.
        :param gene: ulazni gen koji se mutira
        :return: mutirani gen
        """
        for i in range(self.gene_size):
            if np.random.uniform(0, 1) <= self.p_mutation2:
                gene[i] = np.random.normal(0, sigma2)
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
    def select_and_reproduce(self):
        new_population = np.zeros((self.size, self.gene_size))
        new_evals = dict()
        new_fitness = dict()
        new_min_error = np.inf
        new_best_index = -1
        idx = 0

        if self.elitism:
            sorted_values = {k: v for k, v in sorted(self.evals.items(), key=lambda item: item[1])}
            best_indexes = list(sorted_values.keys())[0:self.elitism_rate]
            new_population[0:self.elitism_rate, :] = self.population[best_indexes, :]
            new_best_index = 0
            new_min_error = self.min_error
            idx += 1

        while idx < self.size:
            idx_parent1 = self.roulette_wheel_selection()
            idx_parent2 = self.roulette_wheel_selection()

            if np.random.uniform(0, 1) > self.p_cross:
                continue

            crossover_version = random.randint(0, 3)
            if crossover_version == 0:
                child = self.discrete_recombination(idx_parent1, idx_parent2)
            elif crossover_version == 1:
                child = self.whole_arithmetic_recombination(idx_parent1, idx_parent2)
            else:
                child = self.simple_arithmetic_recombination(idx_parent1, idx_parent2)

            mutation_version = random.uniform(0, self.v1 + self.v2 + self.v3)
            if mutation_version <= self.v1:
                child = self.mutation1(child, 0.25, True)
            elif mutation_version <= self.v1 + self.v2:
                child = self.mutation1(child, 1.5, False)
            else:
                child = self.mutation2(child, 2)
            self.model.params = np.expand_dims(child, axis=1)
            value = self.model.calculate_error(self.data.x, self.data.y)

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

        crossover_version = random.randint(0, 3)
        if crossover_version == 0:
            child = self.discrete_recombination(idx_parent1, idx_parent2)
        elif crossover_version == 1:
            child = self.whole_arithmetic_recombination(idx_parent1, idx_parent2)
        else:
            child = self.simple_arithmetic_recombination(idx_parent1, idx_parent2)

        mutation_version = random.uniform(0, self.v1+self.v2+self.v3)
        if mutation_version <= self.v1:
            child = self.mutation1(child, 0.25, True)
        elif mutation_version <= self.v1 + self.v2:
            child = self.mutation1(child, 1, False)
        else:
            child = self.mutation2(child, 1)
        self.model.params = np.expand_dims(child, axis=1)
        value = self.model.calculate_error(self.data.x, self.data.y)

        self.population[idx_worst, :] = child
        self.evals[idx_worst] = value
        self.fitness[idx_worst] = np.reciprocal(value)

        if value < self.min_error:
            self.min_error = value
            self.best_index = idx_worst
        return
