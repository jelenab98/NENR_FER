from FuzzyRelations import *
from FuzzyStructures import *
from FuzzyLogic import *
import copy


if __name__ == '__main__':

    u = Domain(1, 6)
    u2 = combine(u, u)

    r1 = FuzzySet(domain=u2)
    r1.set_value((1, 1), 1)
    r1.set_value((2, 2), 1)
    r1.set_value((3, 3), 1)
    r1.set_value((4, 4), 1)
    r1.set_value((5, 5), 1)
    r1.set_value((1, 3), 0.5)
    r1.set_value((3, 1), 0.5)

    r2 = FuzzySet(domain=u2)
    r2.set_value((1, 1), 1)
    r2.set_value((2, 2), 1)
    r2.set_value((3, 3), 1)
    r2.set_value((4, 4), 1)
    r2.set_value((5, 5), 1)
    r2.set_value((1, 3), 0.5)
    r2.set_value((3, 1), 0.1)

    r3 = FuzzySet(domain=u2)
    r3.set_value((1, 1), 1)
    r3.set_value((2, 2), 1)
    r3.set_value((3, 3), 0.3)
    r3.set_value((4, 4), 1)
    r3.set_value((5, 5), 1)
    r3.set_value((2, 1), 0.6)
    r3.set_value((1, 2), 0.6)
    r3.set_value((2, 3), 0.7)
    r3.set_value((3, 2), 0.7)
    r3.set_value((1, 3), 0.5)
    r3.set_value((3, 1), 0.5)

    r4 = FuzzySet(domain=u2)
    r4.set_value((1, 1), 1)
    r4.set_value((2, 2), 1)
    r4.set_value((3, 3), 1)
    r4.set_value((4, 4), 1)
    r4.set_value((5, 5), 1)
    r4.set_value((2, 1), 0.4)
    r4.set_value((1, 2), 0.4)
    r4.set_value((2, 3), 0.5)
    r4.set_value((3, 2), 0.5)
    r4.set_value((1, 3), 0.4)
    r4.set_value((3, 1), 0.4)
    
    print("r1 je definiran nad UxU?", is_u_times_u(r1))
    print()
    print("r1 je simetrična?", is_symmetric(r1))
    print("r2 je simetrična?", is_symmetric(r2))
    # print("r3 je simetrična?", is_symmetric(r3))
    # print("r4 je simetrična?", is_symmetric(r4))
    print()
    print("r1 je refleksivna?", is_reflexive(r1))
    # print("r2 je refleksivna?", is_reflexive(r2))
    print("r3 je refleksivna?", is_reflexive(r3))
    # print("r4 je refleksivna?", is_reflexive(r4))
    print()
    # print("r1 je max-min tranzitivna?", is_max_min_transitive(r1))
    # print("r2 je max-min tranzitivna?", is_max_min_transitive(r2))
    print("r3 je max-min tranzitivna?", is_max_min_transitive(r3))
    print("r4 je max-min tranzitivna?", is_max_min_transitive(r4))
    print()

    u1 = Domain(1, 5)
    u2 = Domain(1, 4)
    u3 = Domain(1, 5)

    r1 = FuzzySet(combine(u1, u2))
    r1.set_value((1, 1), 0.3)
    r1.set_value((1, 2), 1)
    r1.set_value((3, 3), 0.5)
    r1.set_value((4, 3), 0.5)

    r2 = FuzzySet(combine(u2, u3))
    r2.set_value((1, 1), 1)
    r2.set_value((2, 1), 0.5)
    r2.set_value((2, 2), 0.7)
    r2.set_value((3, 3), 1)
    r2.set_value((3, 4), 0.4)

    r3 = composition_of_binary_relations(r1,r2)
    print(r3)
    print()

    u = Domain(1, 5)
    r = FuzzySet(combine(u, u))
    r.set_value((1, 1), 1)
    r.set_value((2, 2), 1)
    r.set_value((3, 3), 1)
    r.set_value((4, 4), 1)
    r.set_value((2, 1), 0.3)
    r.set_value((1, 2), 0.3)
    r.set_value((2, 3), 0.5)
    r.set_value((3, 2), 0.5)
    r.set_value((4, 3), 0.2)
    r.set_value((3, 4), 0.2)

    r2 = copy.deepcopy(r)

    print("Početna relacija je neizrazita relacija ekvivalencije?", is_fuzzy_equivalence(r2))
    print()

    for i in range(1, 4):
        r2 = composition_of_binary_relations(r2, r)

        print("Broj odrađenih kompocizija: {}. Relacija je: \n{}".format(i, r2))
        print("Ova relacija je neizrazita relacija ekvivalencije?", is_fuzzy_equivalence(r2))
        print()
        

