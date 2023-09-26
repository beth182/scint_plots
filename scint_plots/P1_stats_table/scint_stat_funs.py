# IMPORTS
import numpy as np

from scint_flux.functions import read_calculated_fluxes

def stats_of_the_obs_fluxes(df):
    """
    This is currently a repeat of scint_eval -> quick_look -> stats_of_the_fluxes,
    but currently being improved upon here.
    Need to go back and get rid of repeat.
    Returns
    -------

    """

    QH_avs = read_calculated_fluxes.time_averages_of_obs(df, 'QH')
    kdown_avs = read_calculated_fluxes.time_averages_of_obs(df, 'kdown')

    # PERIOD ANALYZED
    # get start and end time by reading off the beigining and end index of QH, kdown dfs,
    # e.g.
    # on command line, do:
    # QH_avs.obs_1.dropna()
    # and take the first and last minute
    print('PERIOD ANALYSED')
    print(QH_avs.obs_1.dropna().index[0], QH_avs.obs_1.dropna().index[-1])

    # NUMBER
    # get lengths of all df here by doing len(df) etc.
    print(' ')
    print('NUMBER QH')
    print(len(QH_avs.obs_1.dropna()))
    print(len(QH_avs.obs_5.dropna()))
    print(len(QH_avs.obs_10.dropna()))
    print(len(QH_avs.obs_60.dropna()))

    # constrict kdown to be the same start/ end time as obs
    kdown = kdown_avs.obs_1.dropna()
    QH = QH_avs.obs_1.dropna()
    kdown_time_match = kdown[(kdown.index >= QH.index[0]) & (kdown.index <= QH.index[-1])]

    # avs matching qh start and stop time
    kdown_time_match_avs = kdown_avs[(kdown_avs.index >= QH.index[0]) & (kdown_avs.index <= QH.index[-1])]
    # NUMBER
    print('NUMBER KDOWN')
    print(len(kdown_time_match_avs.obs_1.dropna()))
    print(len(kdown_time_match_avs.obs_5.dropna()))
    print(len(kdown_time_match_avs.obs_10.dropna()))
    print(len(kdown_time_match_avs.obs_60.dropna()))

    # MEAN LAS
    # overal 1 min mean
    mean_QH = QH.mean()
    mean_kdown = kdown_time_match.mean()
    print(' ')
    print('LAS MEAN')
    print('QH: ', mean_QH)
    print('KDOWN: ', mean_kdown)


    # standard deviations
    print(' ')
    QH_std = QH.resample('10T', closed='right', label='right').std()
    kdown_std = kdown_time_match.resample('10T', closed='right', label='right').std()

    print('STD')
    print('MAX QH')
    max_QH_std = QH_std.max()
    max_QH_std_time = QH_std.index[np.where(QH_std == max_QH_std)[0]]
    print(max_QH_std, ' at ', max_QH_std_time)

    print('MAX KDOWN')
    max_kdown_std = kdown_std.max()
    max_kdown_std_time = kdown_std.index[np.where(kdown_std == max_kdown_std)[0]]
    print(max_kdown_std, ' at ', max_kdown_std_time)

    print('MIN QH')
    min_QH_std = QH_std.min()
    min_QH_std_time = QH_std.index[np.where(QH_std == min_QH_std)[0]]
    print(min_QH_std, ' at ', min_QH_std_time)

    print('MIN KDOWN')
    min_kdown_std = kdown_std.min()
    min_kdown_std_time = kdown_std.index[np.where(kdown_std == min_kdown_std)[0]]
    print(min_kdown_std, ' at ', min_kdown_std_time)

    # mean standard deviation across the day
    QH_std_mean = QH_std.mean()
    print('MEAN QH')
    print(QH_std_mean)
    kdown_std_mean = kdown_std.mean()
    print('MEAN KDOWN')
    print(kdown_std_mean)

    print('end')