from FuzzyStructures import *


def is_u_times_u(relation: FuzzySet):
    """
    Funkcija koja provjerava je li dana relacija binarna unarna relacija. Relacija je unarna ukoliko ima na dijagonali
    elemente oblika (x,x) za svaki x iz domene. Relacija također treba sadržavati parove (x, y) i (y, x) za sve
    kombinacije x i y iz domene skupa.
    :param relation:
    :return:
    """
    if len(relation) == 0:
        print("Poslan je prazan skup na ispitivanje! Vraćam None!")
        return None
    first_elem = relation.get_element_at_index(0)
    if type(first_elem) is not tuple:
        return False
    if len(first_elem) > 2:
        return False
    if int(len(relation) ** 0.5) ** 2 != len(relation):
        print("Dužina nije kvadratna! Skup sigurno nije UxU!")
        return False
    for idx, (element1, element2) in enumerate(relation.get_elements()):
        if idx % (int(len(relation) ** 0.5) + 1) == 0:
            if element1 != element2:
                return False
            continue
        if relation.get_value((element2, element1)) == -1:
            return False

    return True


def is_symmetric(relation: FuzzySet):
    """
    Funkcija koja provjerava je li relacija simetrična. Relacija će biti simetrična ukoliko parovi (x,y) i (y,x) imaju
    istu vrijednot funkcije pripadnosti skupu.
    :param relation:
    :return:
    """
    if not is_u_times_u(relation):
        print("Nije unarna! Nema provjere!")
        return None

    for el1, el2 in relation.get_elements():
        if el1 == el2:
            continue
        if relation.get_value((el1, el2)) != relation.get_value((el2, el1)):
            return False
    return True


def is_reflexive(relation: FuzzySet):
    """
    Funkcija koja provjerava je li dana relacija refleksivna. Relacija će biti refleksivna ukoliko elementi (x,x) imaju
    vrijednost funkcije pripadnosti skupu 1.
    :param relation:
    :return:
    """
    if not is_u_times_u(relation):
        print("Nije unarna! Nema provjere!")
        return None

    for (el1, el2), value in relation.get_items():
        if el1 == el2 and value != 1:
            return False
    return True


def is_max_min_transitive(relation: FuzzySet):
    """
    Funkcija koja provjerava je li relacija max min tranzitivna. Relacija je tranzitivna ako vrijedi
    mi(a,c) >= max( min(mi(a,b), mi(b,c))) za svaki b iz domene - a - c
    :param relation:
    :return:
    """
    if not(is_u_times_u(relation)):
        print("Nije unarna! Nema provjere!")
        return None

    d1, d2 = relation.get_parents()
    domain = set(d1.get_elements())
    for (el1, el2), value in relation.get_items():
        if el1 == el2:
            continue
        tmp_domain = domain - {el1} - {el2}
        tmp_values = []
        for el in tmp_domain:
            tmp_values.append(min(relation.get_value((el1, el)), relation.get_value((el, el2))))
        if value < max(tmp_values):
            return False
    return True


def is_fuzzy_equivalence(relation: FuzzySet):
    """
    Funckija koja provjerava je li relacija relacija ekvivalencije. Relacija ekvivalencije je istovremeno i refleksivna,
    simetrična, ali i max-min tranzitivna.
    :param relation:
    :return:
    """
    return is_reflexive(relation) and is_symmetric(relation) and is_max_min_transitive(relation)


def composition_of_binary_relations(relation1: FuzzySet, relation2: FuzzySet):
    """
    Funkcija koja provodi kompoziciju dviju relacije. Kompozicija je moguća samo ako su relacije dimenzija UxV i VxZ pri
    čemu će nastati nova relacija dimenzija UxZ. Kompozicija se provodi po principu max-min.
    :param relation1:
    :param relation2:
    :return:
    """
    d1_1, d1_2 = relation1.get_parents()
    d2_1, d2_2 = relation2.get_parents()
    if len(d1_1) != len(d2_2) or len(d1_2) != len(d2_1):
        print("Krivo zadane domene! Vraćam None!")
        return None
    new_domain = combine(d1_1, d2_2)
    new_relation = FuzzySet(domain=new_domain)

    for el1_1 in d1_1.get_elements():
        for el2_2 in d2_2.get_elements():
            tmp_values = []
            for el1_2 in d1_2.get_elements():
                tmp_values.append(min(relation1.get_value((el1_1, el1_2)), relation2.get_value((el1_2, el2_2))))
            new_relation.set_value((el1_1, el2_2), max(tmp_values))

    return new_relation
