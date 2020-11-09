def lambda_function(x, alpha=None, beta=None, gamma=None, *args):
    """
    Lambda-funkcija implementira po formuli danoj u knjizi s predavanja.
    :param x:
    :param alpha:
    :param beta:
    :param gamma:
    :return:
    """
    if alpha is None or beta is None or gamma is None:
        print("Krivo zadani parametri! Vraćam 0.0!")
        return 0.0
    if not(alpha < beta < gamma):
        print("Krivo zadani parametri! Vraćam 0.0!")
        return 0.0
    if x < alpha:
        return 0.0
    elif alpha <= x < beta:
        return (x - alpha)/(beta - alpha)
    elif beta <= x < gamma:
        return (gamma - x)/(gamma - beta)
    else:
        return 0.0


def l_function(x, alpha=None, beta=None, *args):
    """
    L-funkcija implementirana po formuli danoj u knjizi s predavanja.
    :param x:
    :param alpha:
    :param beta:
    :return:
    """
    if alpha is None or beta is None:
        print("Krivo zadani parametri! Vraćam 0.0!")
        return 0.0
    if not(alpha < beta):
        print("Krivo zadani parametri! Vraćam 0.0!")
        return 0.0
    if x < alpha:
        return 1.0
    elif alpha <= x < beta:
        return (beta - x)/(beta - alpha)
    else:
        return 0.0


def gamma_function(x, alpha=None, beta=None, *args):
    """
    Gamma-funkcija implementriana po formuli danoj u knjizi s predavanja.
    :param x:
    :param alpha:
    :param beta:
    :return:
    """
    if alpha is None or beta is None:
        print("Krivo zadani parametri! Vraćam 0.0!")
        return 0.0
    if not(alpha < beta):
        print("Krivo zadani parametri! Vraćam 0.0!")
        return 0.0
    if x < alpha:
        return 0.0
    elif alpha <= x < beta:
        return (x - alpha)/(beta - alpha)
    else:
        return 1.0


def pi_function(x, alpha=None, beta=None, gamma=None, delta=None, *args):
    """
    Pi-funkcija implementirana po formuli danoj u knjizi s predavanja.
    :param x:
    :param alpha:
    :param beta:
    :param gamma:
    :param delta:
    :return:
    """
    if alpha is None or beta is None or gamma is None or delta is None:
        print("Krivo zadani parametri! Vraćam 0.0!")
        return 0.0
    if not(alpha < beta < gamma < delta):
        print("Krivo zadani parametri! Vraćam 0.0!")
        return 0.0
    if x < alpha:
        return 0.0
    elif alpha <= x < beta:
        return (x - alpha)/(beta - alpha)
    elif beta <= x < gamma:
        return 1.0
    elif gamma <= x < delta:
        return (delta - x)/(delta - gamma)
    else:
        return 0.0
