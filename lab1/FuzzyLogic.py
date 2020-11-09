from FuzzyStructures import *


def zadher_negate(input_set: FuzzySet):
    """
    Klasična negacija koja za svaki element iz skupa vraća 1-f(x).
    :param input_set: ulazni set koji se negira
    :return:
    """
    new_set = FuzzySet()
    for element, value in input_set.get_items():
        new_set.set_value(element, 1-value)
    return new_set


def zadher_or(set1: FuzzySet, set2: FuzzySet):
    """
    Funkcija koja implementira operaciju OR (unija). Uzima se maximalna vrijednost pripadnosti od dva elementa.
    :param set1:
    :param set2:
    :return:
    """
    new_fuzzy_set = FuzzySet()
    if not(set1.domain.__eq__(set2.domain)):
        print("Domene moraju biti iste! Vraćam prazni skup!")
        return new_fuzzy_set
    new_domain = sorted(set(set1.get_elements() + set2.get_elements()))
    for element in new_domain:
        new_fuzzy_set.set_value(element, max(set1.get_value(element), set2.get_value(element)))
    return new_fuzzy_set


def zadher_and(set1: FuzzySet, set2: FuzzySet):
    """
    Funkcija koja implementira operaciju AND (presjek). Uzima se minimalna vrijednost pripadnosti od dva elementa.
    :param set1:
    :param set2:
    :return:
    """
    new_fuzzy_set = FuzzySet()
    if not(set1.domain.__eq__(set2.domain)):
        print("Domene moraju biti iste! Vraćam prazni skup!")
        return new_fuzzy_set
    new_domain = sorted(set(set1.get_elements() + set2.get_elements()))
    for element in new_domain:
        new_fuzzy_set.set_value(element, min(set1.get_value(element), set2.get_value(element)))
    return new_fuzzy_set


def hamacher_t_norm(set1, set2, v=0.0):
    """
    Funckija koja implementira Hamacherovu parametriziranu T normu po uputama iz knjige.
    :param set1:
    :param set2:
    :param v:
    :return:
    """
    if v < 0:
        print("V mora bit nenegativan! Automatski ga postavljam na 0.")
        v = 0.0
    new_fuzzy_set = FuzzySet()
    if not(set1.domain.__eq__(set2.domain)):
        print("Domene moraju biti iste! Vraćam prazni skup!")
        return new_fuzzy_set
    new_domain = sorted(set(set1.get_elements() + set2.get_elements()))
    for element in new_domain:
        a = set1.get_value(element)
        b = set2.get_value(element)
        new_fuzzy_set.set_value(element, a*b / (v + (1 - v)*(a + b - a*b)))
    return new_fuzzy_set


def hamacher_s_norm(set1, set2, v=0.0):
    """
    Funkcija koja implementira Hamacherovu parametriziranu S normu po uputama iz knjige.
    :param set1:
    :param set2:
    :param v:
    :return:
    """
    if v < 0:
        print("V mora bit nenegativan! Automatski ga postavljam na 0.")
        v = 0.0
    new_fuzzy_set = FuzzySet()
    if not(set1.domain.__eq__(set2.domain)):
        print("Domene moraju biti iste! Vraćam prazni skup!")
        return new_fuzzy_set
    new_domain = sorted(set(set1.get_elements() + set2.get_elements()))
    for element in new_domain:
        a = set1.get_value(element)
        b = set2.get_value(element)
        new_fuzzy_set.set_value(element, (a + b - a*b*(2-v)) / (1 - (1 - v)*a*b))
    return new_fuzzy_set


def yager_t_norm(set1, set2, q=0.0):
    """
    Funkcija koja implementira Yagerovu parametriziranu T normu.
    :param set1:
    :param set2:
    :param q:
    :return:
    """
    if q < 0:
        print("Q mora bit nenegativan! Automatski ga postavljam na 0.")
        q = 0.0
    new_fuzzy_set = FuzzySet()
    if not(set1.domain.__eq__(set2.domain)):
        print("Domene moraju biti iste! Vraćam prazni skup!")
        return new_fuzzy_set
    new_domain = sorted(set(set1.get_elements() + set2.get_elements()))
    for element in new_domain:
        a = set1.get_value(element)
        b = set2.get_value(element)
        new_fuzzy_set.set_value(element, 1 - min(1, ((1 - a)**q + (1 - b)**q)**(1./q)))
    return new_fuzzy_set


def yager_s_norm(set1, set2, q=0.0):
    """
    Funkcija koja implementira Yagerovu parametriziranu S normu.
    :param set1:
    :param set2:
    :param q:
    :return:
    """
    if q < 0:
        print("Q mora bit nenegativan! Automatski ga postavljam na 0.")
        q = 0.0
    new_fuzzy_set = FuzzySet()
    if not(set1.domain.__eq__(set2.domain)):
        print("Domene moraju biti iste! Vraćam prazni skup!")
        return new_fuzzy_set
    new_domain = sorted(set(set1.get_elements() + set2.get_elements()))
    for element in new_domain:
        a = set1.get_value(element)
        b = set2.get_value(element)
        new_fuzzy_set.set_value(element, min(1, (a**q + b**q)**(1./q)))
    return new_fuzzy_set

