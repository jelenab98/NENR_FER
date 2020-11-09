from Defuzziers import *
from FuzzySystem import *
from FuzzyBase import *
import sys

if __name__ == '__main__':
    variables = FuzzyVariables()
    rudder_system = RudderControl(variables, defuzzier_COA)
    acceleration_system = AccelerationControl(variables, defuzzier_COA)
    while True:
        elements = input().strip('\n').split(' ')
        if elements[0] == "KRAJ":
            break
        L = int(elements[0])
        D = int(elements[1])
        Lk = int(elements[2])
        Dk = int(elements[3])
        V = int(elements[4])
        S = int(elements[5])
        k = rudder_system.make_decision(L, D, Lk, Dk, V, S)
        a = acceleration_system.make_decision(L, D, Lk, Dk, V, S)
        print("{} {}".format(a, k))
        sys.stdout.flush()
