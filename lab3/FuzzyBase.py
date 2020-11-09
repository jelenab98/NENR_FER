from LogicStructures import *
from Functions import *


class FuzzyVariables:
    """
    Pomocna klasa u kojoj su hardkodirane koristene jezicne varijable za sustav broda.
    """
    def __init__(self):
        self.udaljenost_domain = Domain(0, 1301)
        self.ubrzanje_domain = Domain(-10, 15)
        self.brzina_domain = Domain(20, 61)
        self.kormilo_domain = Domain(-90, 91)
        self.smjer_domain = Domain(0, 2)

        self.smjer_tocan = FuzzySet(self.smjer_domain)
        self.smjer_tocan.set_value(1, 1)
        self.smjer_kriv = FuzzySet(self.smjer_domain)
        self.smjer_kriv.set_value(0, 1)

        self.kormilo_ostro_desno = FuzzySet(self.kormilo_domain, l_function, -60, -30)
        self.kormilo_desno = FuzzySet(self.kormilo_domain, lambda_function, -60, -30, -15)
        self.kormilo_blago_desno = FuzzySet(self.kormilo_domain, lambda_function, -30, -15, 0)
        self.kormilo_ravno = FuzzySet(self.kormilo_domain, lambda_function, -15, 0, 15)
        self.kormilo_blago_lijevo = FuzzySet(self.kormilo_domain, lambda_function, 0, 15, 30)
        self.kormilo_lijevo = FuzzySet(self.kormilo_domain, lambda_function, 15, 30, 60)
        self.kormilo_ostro_lijevo = FuzzySet(self.kormilo_domain, gamma_function, 30, 60)

        self.brzina_presporo = FuzzySet(self.brzina_domain, l_function, 25, 30)
        self.brzina_sporo = FuzzySet(self.brzina_domain, lambda_function, 25, 35, 40)
        self.brzina_taman = FuzzySet(self.brzina_domain, lambda_function, 35, 40, 45)
        self.brzina_brzo = FuzzySet(self.brzina_domain, lambda_function, 40, 45, 55)
        self.brzina_prebrzo = FuzzySet(self.brzina_domain, gamma_function, 55, 60)

        self.ubrzanje_koci = FuzzySet(self.ubrzanje_domain, l_function, -7, -5)
        self.ubrzanje_uspori = FuzzySet(self.ubrzanje_domain, lambda_function, -7, -5, 0)
        self.ubrzanje_nula = FuzzySet(self.ubrzanje_domain, lambda_function, -5, 0, 5)
        self.ubrzanje_ubrzaj = FuzzySet(self.ubrzanje_domain, lambda_function, 0, 5, 10)
        self.ubrzanje_turbo = FuzzySet(self.ubrzanje_domain, gamma_function, 5, 10)

        self.udaljenost_kriticno_blizu = FuzzySet(self.udaljenost_domain, l_function, 15, 40)
        self.udaljenost_blizu = FuzzySet(self.udaljenost_domain, lambda_function, 15, 40, 95)
        self.udaljenost_sredina = FuzzySet(self.udaljenost_domain, lambda_function, 65, 95, 125)
        self.udaljenost_daleko = FuzzySet(self.udaljenost_domain, lambda_function, 95, 125, 150)
        self.udaljenost_jako_daleko = FuzzySet(self.udaljenost_domain, gamma_function, 125, 150)

        self.L_kriticno_blizu = Antecedent(self.udaljenost_kriticno_blizu, "L")
        self.L_blizu = Antecedent(self.udaljenost_blizu, 'L')
        self.L_sredina = Antecedent(self.udaljenost_sredina, 'L')
        self.L_daleko = Antecedent(self.udaljenost_daleko, 'L')
        self.L_jako_daleko = Antecedent(self.udaljenost_jako_daleko, 'L')
        self.L_ne_kriticno_blizu = Antecedent(zadher_negate(self.udaljenost_kriticno_blizu), 'L')
        self.L_ne_blizu = Antecedent(zadher_negate(self.udaljenost_blizu), 'L')

        self.Lk_kriticno_blizu = Antecedent(self.udaljenost_kriticno_blizu, "Lk")
        self.Lk_blizu = Antecedent(self.udaljenost_blizu, 'Lk')
        self.Lk_sredina = Antecedent(self.udaljenost_sredina, 'Lk')
        self.Lk_daleko = Antecedent(self.udaljenost_daleko, 'Lk')
        self.Lk_jako_daleko = Antecedent(self.udaljenost_jako_daleko, 'Lk')
        self.Lk_ne_kriticno_blizu = Antecedent(zadher_negate(self.udaljenost_kriticno_blizu), 'Lk')
        self.Lk_ne_blizu = Antecedent(zadher_negate(self.udaljenost_blizu), 'Lk')

        self.D_kriticno_blizu = Antecedent(self.udaljenost_kriticno_blizu, "D")
        self.D_blizu = Antecedent(self.udaljenost_blizu, 'D')
        self.D_sredina = Antecedent(self.udaljenost_sredina, 'D')
        self.D_daleko = Antecedent(self.udaljenost_daleko, 'D')
        self.D_jako_daleko = Antecedent(self.udaljenost_jako_daleko, 'D')
        self.D_ne_kriticno_blizu = Antecedent(zadher_negate(self.udaljenost_kriticno_blizu), 'D')
        self.D_ne_blizu = Antecedent(zadher_negate(self.udaljenost_blizu), 'D')

        self.Dk_kriticno_blizu = Antecedent(self.udaljenost_kriticno_blizu, "Dk")
        self.Dk_blizu = Antecedent(self.udaljenost_blizu, 'Dk')
        self.Dk_sredina = Antecedent(self.udaljenost_sredina, 'Dk')
        self.Dk_daleko = Antecedent(self.udaljenost_daleko, 'Dk')
        self.Dk_jako_daleko = Antecedent(self.udaljenost_jako_daleko, 'Dk')
        self.Dk_ne_kriticno_blizu = Antecedent(zadher_negate(self.udaljenost_kriticno_blizu), 'Dk')
        self.Dk_ne_blizu = Antecedent(zadher_negate(self.udaljenost_blizu), 'Dk')

        self.V_presporo = Antecedent(self.brzina_presporo, 'V')
        self.V_sporo = Antecedent(self.brzina_sporo, 'V')
        self.V_taman = Antecedent(self.brzina_taman, 'V')
        self.V_brzo = Antecedent(self.brzina_brzo, 'V')
        self.V_prebrzo = Antecedent(self.brzina_prebrzo, 'V')

        self.S_kriv = Antecedent(self.smjer_kriv, 'S')
