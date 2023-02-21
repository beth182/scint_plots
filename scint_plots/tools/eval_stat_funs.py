# imports
import numpy as np
import pandas as pd


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


def variable_hitrate(obs, mod, obs_uncertainty=10):
    """
    Hit Rate
    :param obs: Pandas series of observations (or dataset 1).
    :param mod: Pandas series of model data (or dataset 2).
    :param obs_uncertainty: The observation uncertainty, as a percentage.
     We use 10 %: For day-time eddy covariance data: Martin Best thesis page 119
    :return:
    """

    # make pandas df
    df = pd.DataFrame({'obs': obs, 'mod': mod})

    # calculate the observation error
    df['obs_error'] = (df.obs / 100) * obs_uncertainty

    df['max_threshold'] = df['obs'] + df['obs_error']
    df['min_threshold'] = df['obs'] - df['obs_error']

    # set up dataframe with column of zeros
    df['hits'] = np.zeros(len(df))

    # change to one for successful hit
    df.hits[(df['mod'] >= df['min_threshold']) & (df['mod'] <= df['max_threshold'])] = 1

    # get hit rate
    hr_variable = df.hits.mean() * 100

    return hr_variable
