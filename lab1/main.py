from Functions import *
from FuzzyLogic import *


def printing(element, input_string=None):
    if input_string:
        print(input_string)
    print(element)


if __name__ == '__main__':
    d1 = Domain(0, 5)
    printing(d1, 'Elementi domene d1:')
    d2 = Domain(0, 3)
    printing(d2, 'Elementi domene d2:')
    d3 = combine(d1, d2)
    printing(d3, 'Elementi domene d3:')
    print(d3.get_element(0))
    print(d3.get_element(5))
    print(d3.get_element(14))
    print(d3.get_index((4, 1)))

    print("-----------------------------------------------------------------------------------------------------------")

    d = Domain(0, 11)
    set1 = FuzzySet(d)
    set1.set_value(0, 1.0)
    set1.set_value(1, 0.8)
    set1.set_value(2, 0.6)
    set1.set_value(3, 0.4)
    set1.set_value(4, 0.2)
    printing(set1, 'Set1:')
    d2 = Domain(-5, 6)
    set2 = FuzzySet(d2, lambda_function, -4, 0, 4)
    printing(set2, 'Set2:')

    print("-----------------------------------------------------------------------------------------------------------")

    printing(set1, 'Set1:')
    not_set1 = zadher_negate(set1)
    printing(not_set1, 'notSet1:')
    union = zadher_or(set1, not_set1)
    printing(union, 'Set1 union notSet1:')
    hinters = hamacher_t_norm(set1, not_set1, v=1.0)
    printing(hinters, 'Set1 intersection with notSet1 using parameterised Hamacher T norm with parameter 1.0:')

    end = input('Please press any key or close to end!\n')
