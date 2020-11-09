from FuzzyLogic import *


class Antecedent:
    """
    Pomocna klasa koja definira antecedent. Svakom skupu je pridodjeljena i oznaka kako bi se lakse odredila trazena
    vrijednost prilikom odredivanja razine pripadnosti skupu.
    """
    def __init__(self, input_set, variable):
        self.fuzzy_set = input_set
        self.variable = variable

    def calculate(self, l, d, l_k, d_k, v, s):
        if self.variable == 'L':
            return self.fuzzy_set.get_value(l)
        elif self.variable == 'D':
            return self.fuzzy_set.get_value(d)
        elif self.variable == 'Lk':
            return self.fuzzy_set.get_value(l_k)
        elif self.variable == 'Dk':
            return self.fuzzy_set.get_value(d_k)
        elif self.variable == 'V':
            return self.fuzzy_set.get_value(v)
        elif self.variable == 'S':
            return self.fuzzy_set.get_value(s)
        else:
            return 0


class Rule:
    """
    Klasa koja implementira strukturu pravila oblika ANTECEDENTI -> CILJ. Antecedenti mogu biti povezani razlicitim
    "veznicima" (I, ILI) pa je ovisno o njima i razlicit izracun finalne relacije.
    """
    def __init__(self, antecedents, conjunctions, goal_set):
        self.antecedents = antecedents
        self.conjunctions = conjunctions
        self.goal_set = goal_set

    def calculate(self, l, d, l_k, d_k, v, s):
        """
        Metoda koja racuna zaklucak pravila temeljem singleton vrijednosti. Metoda izracuna je jos dodatno
        pojednostavljena naspram klasicnog racunanja. Izracunaju se mjere pripadnosti antecedenta za odredene ulazne
        vrijednosti i zatim se ovisno o pravilu odreduje iznos antecedenta. Finalni zaklucak bit ce relacija koja gleda
        minimalnu vrijednost izmedu antecedenta i cilja.
        :param l: udaljenost od lijeve obale
        :param d: udaljenost od desne obale
        :param l_k: udaljenost od lijeve obale pod kutem
        :param d_k: udaljenost od desne obale pod kutem
        :param v: brzina
        :param s: smjer
        :return: relacija-zakljucak
        """
        value = self.antecedents[0].calculate(l, d, l_k, d_k, v, s)
        for i in range(1, len(self.antecedents)):
            tmp_value = self.antecedents[i].calculate(l, d, l_k, d_k, v, s)
            if self.conjunctions[i-1] == 'ILI':
                value = max(tmp_value, value)
            else:
                value = min(tmp_value, value)

        new_set = FuzzySet()

        for domain_element in self.goal_set.get_domain().get_elements():
            new_set.set_value(domain_element, value)
        return zadher_and(new_set, self.goal_set)
