def defuzzier_COA(input_set):
    """
    Sustav za formiranje brojcane vrijednosti neizrazite relacije/skupa. Provodi se postupak Center of Area nad
    primljenim ulaznim skupom.
    :param input_set: ulazna neizrazita relacija/skup
    :return: brojčana vrijednost
    """
    top = 0
    bottom = 0

    for element, value in input_set.get_items():
        top += element*value
        bottom += value

    if bottom == 0:
        return 0
    return int(top / bottom)
