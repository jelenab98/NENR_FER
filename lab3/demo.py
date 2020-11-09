from Defuzziers import *
from FuzzySystem import *
from FuzzyBase import *


def print_one_rule(system):
    print("Demonstracija pravila zaključivanja na bazi pravila za kormilo!")
    odabir = input("Odaberite jedno pravilo od 0 do {}\n".format(len(system.rules) - 1))
    if int(odabir) not in range(0, len(system.rules)):
        print("Krivi odabir pravila!")
        return
    print("Odabrano je pravilo ", odabir)
    el = input("Unesite L, D, Lk, Dk, V, S odvojene razmakom >>").strip('\n').split(' ')
    try:
        L = int(el[0])
        D = int(el[1])
        Lk = int(el[2])
        Dk = int(el[3])
        V = int(el[4])
        S = int(el[5])
    except:
        print("Krivo zadane vrijednosti!")
        return
    rule = system.rules[int(odabir)]
    result = rule.calculate(L, D, Lk, Dk, V, S)
    num_result = defuzzier_COA(result)
    print("Za odabrano pravilo izračunata je relacija:\n", result)
    print("\nDefuzirana vrijednost je {}".format(num_result))


def print_all_rules(system):
    print("Demonstracija pravila zaključivanja na bazi pravila za kormilo!")
    el = input("Unesite L, D, Lk, Dk, V, S odvojene razmakom >>").strip('\n').split(' ')
    try:
        L = int(el[0])
        D = int(el[1])
        Lk = int(el[2])
        Dk = int(el[3])
        V = int(el[4])
        S = int(el[5])
    except:
        print("Krivo zadane vrijednosti!")
        return
    result = system.make_union(L, D, Lk, Dk, V, S)
    num_result = defuzzier_COA(result)
    print("Unija svih pravila baze je relacija:\n", result)
    print("\nDefuzirana vrijednost je {}".format(num_result))


if __name__ == '__main__':
    variables = FuzzyVariables()
    rudder_system = RudderControl(variables, defuzzier_COA)
    acceleration_system = AccelerationControl(variables, defuzzier_COA)
    print_one_rule(rudder_system)
    print()
    print_all_rules(rudder_system)
