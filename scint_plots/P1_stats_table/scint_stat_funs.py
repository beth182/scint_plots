# IMPORTS
import numpy as np
import pandas as pd
import datetime as dt

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


def stats_of_model(df, UKV_df_QH, UKV_df_kdown):
    # Average the obs
    # time average the obs
    QH_avs = read_calculated_fluxes.time_averages_of_obs(df, 'QH', on_hour=True)
    kdown_avs = read_calculated_fluxes.time_averages_of_obs(df, 'kdown')

    print(' ')
    print('UKV mean')
    print('QH')
    print(UKV_df_QH.WAverage.mean())
    print('KDOWN')
    print(UKV_df_kdown.WAverage.mean())

    compare_1_QH = pd.concat([QH_avs.obs_1, UKV_df_QH.WAverage], axis=1).dropna()
    compare_5_QH = pd.concat([QH_avs.obs_5, UKV_df_QH.WAverage], axis=1).dropna()
    compare_10_QH = pd.concat([QH_avs.obs_10, UKV_df_QH.WAverage], axis=1).dropna()
    compare_60_QH = pd.concat([QH_avs.obs_60, UKV_df_QH.WAverage], axis=1).dropna()

    kdown_60 = kdown_avs.obs_60.dropna()
    kdown_60.index = kdown_60.index - dt.timedelta(minutes=45)
    kdown_10 = kdown_avs.obs_10.dropna()
    kdown_10.index = kdown_10.index + dt.timedelta(minutes=5)
    kdown_5 = kdown_avs.obs_5.dropna()
    kdown = kdown_avs.obs_1.dropna()

    # find common times - can't do this within the built function - as for the model eval purposes, kdown averages are
    # different
    compare_1_kdown = pd.concat([kdown.iloc[np.where([i.minute == 15 for i in kdown.index])[0]], UKV_df_kdown.WAverage],
                                axis=1).dropna()
    compare_5_kdown = pd.concat(
        [kdown_5.iloc[np.where([i.minute == 15 for i in kdown_5.index])[0]], UKV_df_kdown.WAverage], axis=1).dropna()
    compare_10_kdown = pd.concat(
        [kdown_10.iloc[np.where([i.minute == 15 for i in kdown_10.index])[0]], UKV_df_kdown.WAverage], axis=1).dropna()
    compare_60_kdown = pd.concat(
        [kdown_60.iloc[np.where([i.minute == 15 for i in kdown_60.index])[0]], UKV_df_kdown.WAverage], axis=1).dropna()

    # absolute difference
    compare_1_QH['abs_diff'] = np.abs(compare_1_QH.obs_1 - compare_1_QH.WAverage)
    compare_5_QH['abs_diff'] = np.abs(compare_5_QH.obs_5 - compare_5_QH.WAverage)
    compare_10_QH['abs_diff'] = np.abs(compare_10_QH.obs_10 - compare_10_QH.WAverage)
    compare_60_QH['abs_diff'] = np.abs(compare_60_QH.obs_60 - compare_60_QH.WAverage)

    compare_1_kdown['abs_diff'] = np.abs(compare_1_kdown.obs_1 - compare_1_kdown.WAverage)
    compare_5_kdown['abs_diff'] = np.abs(compare_5_kdown.obs_5 - compare_5_kdown.WAverage)
    compare_10_kdown['abs_diff'] = np.abs(compare_10_kdown.obs_10 - compare_10_kdown.WAverage)
    compare_60_kdown['abs_diff'] = np.abs(compare_60_kdown.obs_60 - compare_60_kdown.WAverage)

    # difference
    compare_1_QH['difference'] = compare_1_QH.obs_1 - compare_1_QH.WAverage
    compare_5_QH['difference'] = compare_5_QH.obs_5 - compare_5_QH.WAverage
    compare_10_QH['difference'] = compare_10_QH.obs_10 - compare_10_QH.WAverage
    compare_60_QH['difference'] = compare_60_QH.obs_60 - compare_60_QH.WAverage

    compare_1_kdown['difference'] = compare_1_kdown.obs_1 - compare_1_kdown.WAverage
    compare_5_kdown['difference'] = compare_5_kdown.obs_5 - compare_5_kdown.WAverage
    compare_10_kdown['difference'] = compare_10_kdown.obs_10 - compare_10_kdown.WAverage
    compare_60_kdown['difference'] = compare_60_kdown.obs_60 - compare_60_kdown.WAverage

    # Mean Bias error
    MBE_QH_1 = compare_1_QH.difference.mean()
    MBE_QH_5 = compare_5_QH.difference.mean()
    MBE_QH_10 = compare_10_QH.difference.mean()
    MBE_QH_60 = compare_60_QH.difference.mean()

    print(' ')
    print('MBE')
    print('QH')
    print(MBE_QH_1)
    print(MBE_QH_5)
    print(MBE_QH_10)
    print(MBE_QH_60)

    MBE_kdown_1 = compare_1_kdown.difference.mean()
    MBE_kdown_5 = compare_5_kdown.difference.mean()
    MBE_kdown_10 = compare_10_kdown.difference.mean()
    MBE_kdown_60 = compare_60_kdown.difference.mean()

    print('KDOWN')
    print(MBE_kdown_1)
    print(MBE_kdown_5)
    print(MBE_kdown_10)
    print(MBE_kdown_60)

    # maximum difference
    print(' ')
    print('Max diff in kdown 1 min: ',
          compare_1_kdown.iloc[np.where(compare_1_kdown.abs_diff == compare_1_kdown.abs_diff.max())[0]].difference[0])
    print('at: ',
          compare_1_kdown.iloc[np.where(compare_1_kdown.abs_diff == compare_1_kdown.abs_diff.max())[0]].index[0])

    print('Max diff in kdown 5 min: ',
          compare_5_kdown.iloc[np.where(compare_5_kdown.abs_diff == compare_5_kdown.abs_diff.max())[0]].difference[0])
    print('at: ',
          compare_5_kdown.iloc[np.where(compare_5_kdown.abs_diff == compare_5_kdown.abs_diff.max())[0]].index[0])

    print('Max diff in kdown 10 min: ',
          compare_10_kdown.iloc[np.where(compare_10_kdown.abs_diff == compare_10_kdown.abs_diff.max())[0]].difference[
              0])
    print('at: ',
          compare_10_kdown.iloc[np.where(compare_10_kdown.abs_diff == compare_10_kdown.abs_diff.max())[0]].index[0])

    print('Max diff in kdown 60 min: ',
          compare_60_kdown.iloc[np.where(compare_60_kdown.abs_diff == compare_60_kdown.abs_diff.max())[0]].difference[
              0])
    print('at: ',
          compare_60_kdown.iloc[np.where(compare_60_kdown.abs_diff == compare_60_kdown.abs_diff.max())[0]].index[0])

    print(' ')
    print('Max diff in QH 1 min: ',
          compare_1_QH.iloc[np.where(compare_1_QH.abs_diff == compare_1_QH.abs_diff.max())[0]].difference[0])
    print('at: ', compare_1_QH.iloc[np.where(compare_1_QH.abs_diff == compare_1_QH.abs_diff.max())[0]].index[0])

    print('Max diff in QH 5 min: ',
          compare_5_QH.iloc[np.where(compare_5_QH.abs_diff == compare_5_QH.abs_diff.max())[0]].difference[0])
    print('at: ', compare_5_QH.iloc[np.where(compare_5_QH.abs_diff == compare_5_QH.abs_diff.max())[0]].index[0])

    print('Max diff in QH 10 min: ',
          compare_10_QH.iloc[np.where(compare_10_QH.abs_diff == compare_10_QH.abs_diff.max())[0]].difference[0])
    print('at: ', compare_10_QH.iloc[np.where(compare_10_QH.abs_diff == compare_10_QH.abs_diff.max())[0]].index[0])

    print('Max diff in QH 60 min: ',
          compare_60_QH.iloc[np.where(compare_60_QH.abs_diff == compare_60_QH.abs_diff.max())[0]].difference[0])
    print('at: ', compare_60_QH.iloc[np.where(compare_60_QH.abs_diff == compare_60_QH.abs_diff.max())[0]].index[0])

    print(' ')
    print('MAE')
    print('QH MAE 1 min: ', compare_1_QH.abs_diff.mean())
    print('QH MAE 5 min: ', compare_5_QH.abs_diff.mean())
    print('QH MAE 10 min: ', compare_10_QH.abs_diff.mean())
    print('QH MAE 60 min: ', compare_60_QH.abs_diff.mean())

    print(' ')

    print('KDOWN MAE 1 min: ', compare_1_kdown.abs_diff.mean())
    print('KDOWN MAE 5 min: ', compare_5_kdown.abs_diff.mean())
    print('KDOWN MAE 10 min: ', compare_10_kdown.abs_diff.mean())
    print('KDOWN MAE 60 min: ', compare_60_kdown.abs_diff.mean())

    # MAE between model surface and model level closest to zf
    print(' ')
    print('MAE between model surface and model level closest to zf')
    UKV_df_QH['AE'] = np.abs(UKV_df_QH.WAverage - UKV_df_QH.BL_H)
    print(UKV_df_QH.AE.mean())

    print(' ')
    print('max MAE between model surface and model level closest to zf')
    print(UKV_df_QH.AE.max(), ' at ', UKV_df_QH.iloc[np.where(UKV_df_QH.AE == UKV_df_QH.AE.max())[0]].index[0])

    print(' ')
    print('min MAE between model surface and model level closest to zf')
    print(UKV_df_QH.AE.min(), ' at ', UKV_df_QH.iloc[np.where(UKV_df_QH.AE == UKV_df_QH.AE.min())[0]].index[0])

    # MAE between the model surface SA anal and surface centre gridbox
    print(' ')
    print('MAE between the model surface SA anal and surface centre gridbox')
    UKV_df_QH['AE_surf'] = np.abs(UKV_df_QH.WAverage - UKV_df_QH[13])
    print(UKV_df_QH.AE_surf.mean())

    print(' ')
    print('max MAE between the model surface SA anal and surface centre gridbox')
    print(UKV_df_QH.AE_surf.max(), ' at ', UKV_df_QH.iloc[np.where(UKV_df_QH.AE_surf == UKV_df_QH.AE_surf.max())[0]].index[0])

    print(' ')
    print('min MAE between the model surface SA anal and surface centre gridbox')
    print(UKV_df_QH.AE_surf.min(), ' at ', UKV_df_QH.iloc[np.where(UKV_df_QH.AE_surf == UKV_df_QH.AE_surf.min())[0]].index[0])

    print('end')
