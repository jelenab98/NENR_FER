from LogicStructures import *


class FuzzySystem:
    """
    Klasa koja ostvaruje sustav za neizrazito zakljucivanje. Klasa ima metode za izracunavanje zaklucaka pravila, a
    sama pravila se posebno zadaju, ovisno o vrsti sustava.
    """
    def __init__(self, variables, defuzzifier):
        self.rules = list()
        self.variables = variables
        self.defuzzifier = defuzzifier
        self.add_rules()

    def add_rules(self):
        return

    def make_decision(self, l, d, l_k, d_k, v, s):
        """
        Metoda koja implementira samo zakljucivanje. Provodi se unija svih zakljucaka i finalna relacija se provede
        kroz defuzzifier.
        :param l: udaljenost od lijeve obale
        :param d: udaljenost od desne obale
        :param l_k: udaljenost od lijeve obale pod kutem
        :param d_k: udaljenost od desne obale pod kutem
        :param v: brzina
        :param s: smjer
        :return: brojcana vrijednost
        """
        value = self.rules[0].calculate(l, d, l_k, d_k, v, s)
        for idx in range(1, len(self.rules)):
            tmp_value = self.rules[idx].calculate(l, d, l_k, d_k, v, s)
            value = zadher_or(value, tmp_value)
        return self.defuzzifier(value)

    def make_union(self, l, d, l_k, d_k, v, s):
        """
        Metoda koja implementira samo zakljucivanje. Provodi se unija svih zakljucaka i finalna relacija se prosljeduje.
        Implementirano poradi pomocnih metoda za provjeru ispravnosti sustava
        :param l: udaljenost od lijeve obale
        :param d: udaljenost od desne obale
        :param l_k: udaljenost od lijeve obale pod kutem
        :param d_k: udaljenost od desne obale pod kutem
        :param v: brzina
        :param s: smjer
        :return: finalna relacija
        """
        value = self.rules[0].calculate(l, d, l_k, d_k, v, s)
        for idx in range(1, len(self.rules)):
            tmp_value = self.rules[idx].calculate(l, d, l_k, d_k, v, s)
            value = zadher_or(value, tmp_value)
        return value


class RudderControl(FuzzySystem):
    """
    Klasa za upravljanje kormilom. Klasa definira svoja pravila koja su potrebna.
    """
    def add_rules(self):
        rule1 = Rule([self.variables.L_kriticno_blizu, self.variables.Lk_blizu,
                      self.variables.Dk_ne_blizu, self.variables.D_ne_kriticno_blizu],
                     ["ILI", "I", "I"],
                     self.variables.kormilo_ostro_desno)

        rule2 = Rule([self.variables.L_blizu, self.variables.Lk_blizu, self.variables.D_ne_kriticno_blizu,
                     self.variables.Dk_ne_blizu],
                     ["I", "I", "I"],
                     self.variables.kormilo_desno)

        rule3 = Rule([self.variables.L_blizu, self.variables.Lk_blizu, self.variables.D_ne_kriticno_blizu,
                      self.variables.Dk_ne_blizu],
                     ["ILI", "I", "I"],
                     self.variables.kormilo_blago_desno)

        rule4 = Rule([self.variables.L_sredina, self.variables.L_daleko, self.variables.L_jako_daleko,
                      self.variables.D_sredina, self.variables.D_daleko, self.variables.D_jako_daleko],
                     ["ILI", "ILI", "I", "I", "I"],
                     self.variables.kormilo_ravno)

        rule5 = Rule([self.variables.D_blizu, self.variables.Dk_blizu, self.variables.L_ne_kriticno_blizu,
                      self.variables.Lk_ne_blizu],
                     ["ILI", "I", "I"],
                     self.variables.kormilo_blago_lijevo)

        rule6 = Rule([self.variables.D_blizu, self.variables.Dk_blizu, self.variables.L_ne_kriticno_blizu,
                      self.variables.Lk_ne_blizu],
                     ["I", "I", "I"],
                     self.variables.kormilo_lijevo)

        rule7 = Rule([self.variables.D_kriticno_blizu, self.variables.Dk_blizu,
                      self.variables.Lk_ne_blizu, self.variables.L_ne_kriticno_blizu],
                     ["ILI", "I", "I"],
                     self.variables.kormilo_ostro_lijevo)

        rule8 = Rule([self.variables.S_kriv, self.variables.L_kriticno_blizu, self.variables.Lk_blizu,
                      self.variables.Dk_ne_blizu, self.variables.D_ne_kriticno_blizu],
                     ["I", "I", "I", "I"],
                     self.variables.kormilo_ostro_desno)

        rule9 = Rule([self.variables.S_kriv, self.variables.D_kriticno_blizu, self.variables.Dk_blizu,
                      self.variables.Lk_ne_blizu, self.variables.L_ne_kriticno_blizu],
                     ["I", "I", "I", "I"],
                     self.variables.kormilo_ostro_lijevo)

        self.rules.append(rule1)
        self.rules.append(rule2)
        self.rules.append(rule3)
        self.rules.append(rule4)
        self.rules.append(rule5)
        self.rules.append(rule6)
        self.rules.append(rule7)
        self.rules.append(rule8)
        self.rules.append(rule9)


class AccelerationControl(FuzzySystem):
    """
    Klasa za upravljanje akceleracijom. Definira svoja pravila.
    """
    def add_rules(self):

        rule1 = Rule([self.variables.V_presporo, self.variables.V_sporo, self.variables.V_taman],
                     ['ILI', 'ILI'],
                     self.variables.ubrzanje_ubrzaj)

        rule2 = Rule([self.variables.V_prebrzo],
                     [],
                     self.variables.ubrzanje_uspori)

        self.rules.append(rule1)
        self.rules.append(rule2)
