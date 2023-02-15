# imports
import numpy as np


def hitrate(obs, mod, threshold):
    """
    Hit Rate
    :param obs:
    :param mod:
    :param threshold:
    :return:
    """
    differences = mod - obs
    absdiff = abs(differences)
    nlist = []
    for item in absdiff:
        if item <= threshold:
            n = 1.0
        else:
            n = 0.0
        nlist.append(n)
    narray = np.array(nlist)
    # changed to make this a percentage
    hr = narray.mean() * 100

    return hr
