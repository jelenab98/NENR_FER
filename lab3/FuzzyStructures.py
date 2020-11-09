from collections import OrderedDict
#from FuzzyRelations import *


class Domain:
    def __init__(self, min_value=None, max_value=None):
        self.parent1 = None
        self.parent2 = None
        if min_value is not None and max_value is not None:
            self.elements = [x for x in range(int(min_value), int(max_value))]
        else:
            self.elements = []

    def __eq__(self, other):
        if len(other) != len(self.elements):
            return False
        for i in range(len(self.elements)):
            if self.elements[i] != other.get_element(i):
                return False
        return True

    def __len__(self):
        return len(self.elements)

    def __str__(self):
        return_string = ""
        for element in self.elements:
            return_string += "Element domene: {}\n".format(element)
        return_string += "Kardinalitet skupa: {}\n".format(len(self.elements))
        return return_string

    def set_parents(self, parent1, parent2):
        """
        Postavljanje reference na roditelje domene ako je domena Kartezijev produkt dvije domene.
        :param parent1:
        :param parent2:
        :return:
        """

        self.parent1 = parent1
        self.parent2 = parent2

    def get_element(self, index):
        """
        Funkcija za pristupanje elementu na željenom indexu.
        :param index: željeni indeks elementa
        :return:
        """
        try:
            return self.elements[index]
        except:
            print("Indeks je veći od kardinaliteta skupa!")

    def get_index(self, element):
        """
        Funkcija za dobivanje indeksa za određeni element iz skupa.
        :param element: element za koji tražimo indeks
        :return:
        """
        try:
            return self.elements.index(element)
        except:
            print("Element nije u skupu!")

    def update_elements(self, element):
        """
        Dodavanje elemenata u skup, automatski se dodaje na kraj skupa pa sortira
        :param element: element koji dodajemo u skup
        :return:
        """
        self.elements.append(element)
        self.elements = sorted(self.elements)

    def is_included(self, element):
        """
        Provjera je li neki element u domeni ili ne.
        :param element: element koji ispitujemo je li u domeni
        :return:
        """
        return element in self.elements

    def get_parents(self):
        """
        Vraća roditelje domene na temelju kojih je domena nasatala Kartzeijevim produktom. Vratit će se None ako domena
        nije Kartzeijev produkt.
        :return:
        """
        return self.parent1, self.parent2

    def get_elements(self):
        """
        Vraća listu elemenata koji čine domenu. Ova funkcija je napisana radi preglednosti zbog klase FuzzySet.
        :return:
        """
        return self.elements


class FuzzySet:
    def __init__(self, domain=None, fn_range=None, *fn_args):

        self.domain_elements = OrderedDict()
        self.domain = Domain()
        if domain:
            self.domain = domain
            for element in domain.elements:
                self.domain_elements[element] = 0.0
            if fn_range:
                for element in domain.elements:
                    self.domain_elements[element] = fn_range(element, *fn_args)

    def __len__(self):
        return len(self.domain)

    def __str__(self):
        return_string = ''
        if len(self.domain) != 0 and type(self.get_element_at_index(0)) is tuple:
            string_ispis = 'mu'
        else:
            string_ispis = 'd'
        for element in self.domain_elements:
            return_string += string_ispis+'({}) = {:.2f}\n'.format(element, self.domain_elements[element])
        return return_string.strip('\n')

    def set_value(self, element, value):
        """
        Funkcija za promjenu vrijednosti funkcije pripadnosti nekog elementa iz domene/skupa.
        :param element: element koji želimo promjeniti (unosi se element a ne pripadni index elementa)
        :param value: nova vrijednosti funkcije pripadnosti
        :return:
        """
        self.domain_elements[element] = value
        if not(self.domain.is_included(element)):
            self.domain.update_elements(element)

    def get_value(self, element):
        """
        Funkcija za vraćanje vrijednosti funckije pripadnosti za određeni element iz domene. Ako element nije definiran
        u toj domeni, automatski smatramo da mu je funkcija pripadnosti 0.0, ali dajemo 0
        :param element: element iz domene za koji tražimo vrijednosti funkcije pripadnosti
        :return: vrijednost funkcije pripadnosti ili 0 ako nije definirana za taj element
        """
        return self.domain_elements.get(element, 0)

    def get_items(self):
        """
        Funkcija koja vraća listu oblika (element domene, vrijednost funkcije pripadnosti).
        :return: lista s elementima i pripadnim vrijednostima funkcije za skup
        """
        return list(self.domain_elements.items())

    def get_elements(self):
        """
        Funkcija koja vraća listu elemenata domene.
        :return: lista elemenata skupa
        """
        return list(self.domain_elements.keys())

    def get_parents(self):
        """
        Funkcija koja vraća roditelje domene skupa. Ukoliko je skup relacija, vratit će se reference na domene od kojih
        je stvoren Kartezijev produkt.
        :return:
        """
        return self.domain.get_parents()

    def get_domain(self):
        """
        Vraća se domena na temelju koje je set izgrađen.
        :return:
        """
        return self.domain

    def get_element_at_index(self, index):
        """
        Vraća element s određenog indeksa gledanog preko domene.
        :param index:
        :return:
        """
        return self.domain.get_element(index)


def combine(domain1: Domain, domain2: Domain):
    """
    Funkcija za kombiniranje domena. Domene mogu imati listu elemenata u nekom rangu ili mogu imati već stvoren
    kartezijev produkt koji spajajaju s drugim produktom ili rangom. Pretpostavka je da su domene već sortirane uzlazno.
    :param domain1: domena za spajanje
    :param domain2: domena za spajanje
    :return: nova domena kardinaliteta |domain1|*|domain2|
    """
    new_domain = Domain()
    if len(domain1.elements) == 0 or len(domain2.elements) == 0:
        print("Domena je prazna! Vraćam praznu domenu!")
        return new_domain
    new_domain.set_parents(domain1, domain2)
    if type(domain1.elements[0]) is int:
        elements1 = [[x] for x in domain1.elements]
    else:
        elements1 = domain1.elements
    if type(domain2.elements[0]) is int:
        elements2 = [[x] for x in domain2.elements]
    else:
        elements2 = domain2.elements
    for element1 in elements1:
        for element2 in elements2:
            new_domain.update_elements(tuple(element1) + tuple(element2))
    return new_domain
