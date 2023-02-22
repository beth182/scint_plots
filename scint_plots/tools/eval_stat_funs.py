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


def hitrate_bins(df_all):
    """

    :param df:
    :return:
    """

    df = df_all.copy()
    # identify obs columns
    obs_cols = []
    ukv_cols = []
    for col in df:
        if col.startswith('QH'):
            obs_cols.append(col)
        else:
            ukv_cols.append(col)

    df['max'] = df[obs_cols].max(axis=1)
    df['min'] = df[obs_cols].min(axis=1)

    # take 10 percent
    df['max_threshold'] = df['max'] + (df['max'] / 100) * 10
    df['min_threshold'] = df['min'] - (df['min'] / 100) * 10

    model_hits_cols = []
    for col in ukv_cols:
        # hits name
        hit_col_name = col + '_hits'
        model_hits_cols.append(hit_col_name)

        # set up dataframe with column of zeros
        df[hit_col_name] = np.zeros(len(df))
        df[hit_col_name][(df[col] >= df['min_threshold']) & (df[col] <= df['max_threshold'])] = 1

    # sum the hits
    hitrate_val = df[model_hits_cols].mean().mean() * 100

    return hitrate_val