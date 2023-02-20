import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cm
from scipy.stats import linregress
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator

mpl.rcParams.update({'font.size': 15})

from scint_flux.functions import read_calculated_fluxes


def peak_BE(df, scint_path):
    """
    Get the peak bias error and time offset between obs and UKV
    Returns
    -------

    """

    # loop over all days in df
    df_DOY_list = []
    for group in df.groupby(df.index.date):
        day_df = group[1]

        obs_QH_col_name = 'QH_' + str(scint_path)
        obs_kdown_col_name = 'kdown_' + str(scint_path)
        UKV_QH_col_name = 'UKV_QH_' + str(scint_path)
        UKV_kdown_col_name = 'UKV_kdown_' + str(scint_path)

        # calculate MBE of day
        MBE_QH = (day_df[obs_QH_col_name] - day_df[UKV_QH_col_name]).mean()
        MBE_kdown = (day_df[obs_kdown_col_name] - day_df[UKV_kdown_col_name]).mean()

        # observation peaks
        # QH
        QH_obs_df = df_peak(day_df, obs_QH_col_name)
        # kdwn
        Kdn_obs_df = df_peak(day_df, obs_kdown_col_name)

        # model peaks
        # peak UKV Kdn
        UKV_kdn_df = df_peak(day_df, UKV_kdown_col_name)
        # peak UKV QH
        UKB_QH_df = df_peak(day_df, UKV_QH_col_name)

        df_combine = pd.concat([QH_obs_df, Kdn_obs_df, UKV_kdn_df, UKB_QH_df])

        # take difference in time
        time_delta_qh = df_combine.loc[obs_QH_col_name].time - df_combine.loc[UKV_QH_col_name].time
        time_delta_kdn = df_combine.loc[obs_kdown_col_name].time - df_combine.loc[UKV_kdown_col_name].time

        # total minutes difference
        delta_minutes_qh = time_delta_qh.total_seconds() / 60 / 60
        delta_minutes_kdown = time_delta_kdn.total_seconds() / 60 / 60

        # take difference in value
        val_delta_qh = df_combine.loc[obs_QH_col_name].value - df_combine.loc[UKV_QH_col_name].value
        val_delta_kdn = df_combine.loc[obs_kdown_col_name].value - df_combine.loc[UKV_kdown_col_name].value

        # create a dataframe of differences to return
        peak_df = pd.DataFrame.from_dict({'time_delta_qh': [delta_minutes_qh], 'time_delta_kdn': [delta_minutes_kdown],
                                          'value_delta_qh': [val_delta_qh], 'value_delta_kdn': [val_delta_kdn],
                                          'MBE_qh_day': MBE_QH, 'MBE_kdn_day': MBE_kdown})

        # DOY for index
        DOY = int(QH_obs_df.loc[obs_QH_col_name].time.strftime('%Y%j'))

        peak_df.index = [DOY]

        df_DOY_list.append(peak_df)

    df_all = pd.concat(df_DOY_list)

    return df_all


def df_peak(df, column_name):
    """
    Find peak value and time of a dataframe
    """

    var = df[column_name].dropna()

    peak_time = var.iloc[np.where(var == var.max())[0]].index
    peak_val = var.max()

    # create df

    return_df = pd.DataFrame.from_dict({'time': peak_time, 'value': peak_val})

    if len(return_df) != 1:
        # when more than one peak, take the first one only
        return_df = return_df.loc[0:0]

    return_df.index = [column_name]

    return return_df


def peak_analysis_plot(peak_df, pair_id, average, save_path):
    """

    :param peak_df:
    :param save_path:
    :return:
    """

    plt.figure(figsize=(12, 10))

    cmap = cm.get_cmap('rainbow')

    if average == 60:

        axlim_min = -300
        axlim_max = 300

        smallest_dt = -6
        largest_dt = 6
    else:
        raise ValueError('average lims not set yet')

    bounds = np.linspace(smallest_dt, largest_dt, np.abs(largest_dt) + np.abs(smallest_dt) + 1)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    plt.scatter(peak_df.MBE_qh_day, peak_df.value_delta_qh, c=peak_df.time_delta_qh, cmap=cmap, norm=norm)
    cbar = plt.colorbar()
    cbar.set_ticks(np.arange(smallest_dt, largest_dt + 1, step=1))

    slope, intercept, r_value, p_value, std_err = linregress(peak_df.MBE_qh_day, peak_df.value_delta_qh)
    string_for_leg = 'm = ' + str(round(slope, 2)) + '\n' + 'c = ' + str(round(intercept, 2))

    plt.plot(np.unique(peak_df.MBE_qh_day),
             np.poly1d(np.polyfit(peak_df.MBE_qh_day, peak_df.value_delta_qh, 1))(np.unique(peak_df.MBE_qh_day)),
             color='blue', linestyle='--', alpha=0.5, label=string_for_leg)

    plt.plot([min(peak_df.MBE_qh_day), max(peak_df.MBE_qh_day)], [min(peak_df.MBE_qh_day), max(peak_df.MBE_qh_day)],
             color='k', linestyle=':', alpha=0.5, label='Identity')

    cbar.ax.set_ylabel('Time Offset (h)')
    plt.xlabel('day MBE (W $m^{-2}$)')
    plt.ylabel('peak BE (W $m^{-2}$)')

    plt.xlim(axlim_min, axlim_max)
    plt.ylim(axlim_min, axlim_max)

    plt.legend()

    # plt.show()
    plt.savefig(save_path + pair_id + '_' + str(average) + '_peak.png', bbox_inches='tight', dpi=300)

    print('end')


# def peak_rolling_mean(df, column_name, window_size=10):
#     """
#     Find the observation peak value and time
#     """
#
#     obs_var = df[column_name].dropna()
#
#     # rolling mean
#     obs_rolling_mean = obs_var.rolling(window=window_size).mean()
#
#     # peak time
#     peak_time = obs_rolling_mean.iloc[np.where(obs_rolling_mean == obs_rolling_mean.max())[0]].index
#
#     return peak_time


def read_peak_csvs(pair_id):
    """

    Returns
    -------

    """

    # open pandas df from csv file
    df = pd.read_csv(
        'C:/Users/beths/OneDrive - University of Reading/Paper 2/categorize_days/peak_analysis/peak_analysis_' + pair_id + '.csv')
    df = df.rename(columns={'Unnamed: 0': 'DOY'})
    df = df.set_index('DOY')

    # total days
    print('len days: ', len(df))

    assert len(np.where(df.time_delta_qh == 0)[0]) + len(np.where(df.time_delta_qh > 0)[0]) + len(
        np.where(df.time_delta_qh < 0)[0]) == len(df)

    # total negative t delta
    print('len negative dt: ', len(np.where(df.time_delta_qh < 0)[0]))

    # total number of positive t delta
    print('len positive dt: ', len(np.where(df.time_delta_qh > 0)[0]))

    # total number of 0 t delta
    print('len 0 dt: ', len(np.where(df.time_delta_qh == 0)[0]))

    # precentage of negative dt from total days
    print('% of negative dt :', len(np.where(df.time_delta_qh < 0)[0]) / len(df) * 100)

    # most frequant t delta
    print('most common t delta: ',
          df['time_delta_qh'].value_counts().sort_values(ascending=False)[df.time_delta_qh.mode()])

    # peak MBE
    print('peak MBE: ', df.value_delta_qh.mean())

    # day MBE
    print('DAY MBE: ', df.MBE_qh_day.mean())


def peak_stats_by_season(pair_id):
    # open pandas df from csv file
    df = pd.read_csv(
        'C:/Users/beths/OneDrive - University of Reading/Paper 2/categorize_days/peak_analysis/peak_analysis_' + pair_id + '.csv')
    df = df.rename(columns={'Unnamed: 0': 'DOY'})
    df = df.set_index('DOY')

    # split into seasons

    # convert index to datetime

    # add month column
    df['month'] = pd.to_datetime(df.index, format='%Y%j').month

    DJF = df.iloc[np.asarray(
        list(np.where(df.month == 1)[0]) + list(np.where(df.month == 2)[0]) + list(np.where(df.month == 12)[0]))]

    MAM = df.iloc[np.asarray(
        list(np.where(df.month == 3)[0]) + list(np.where(df.month == 4)[0]) + list(np.where(df.month == 5)[0]))]

    JJA = df.iloc[np.asarray(
        list(np.where(df.month == 6)[0]) + list(np.where(df.month == 7)[0]) + list(np.where(df.month == 8)[0]))]

    SON = df.iloc[np.asarray(
        list(np.where(df.month == 9)[0]) + list(np.where(df.month == 10)[0]) + list(np.where(df.month == 11)[0]))]

    assert len(DJF) + len(MAM) + len(JJA) + len(SON) == len(df)

    # print len days in each season
    print('len days by season:')
    print('DJF: ', len(DJF))
    print('MAM: ', len(MAM))
    print('JJA: ', len(JJA))
    print('SON: ', len(SON))
    print(' ')

    # print % days negative dt

    print('% of negative dt :')

    try:
        print('DJF: ', len(np.where(DJF.time_delta_qh < 0)[0]) / len(DJF) * 100)
    except ZeroDivisionError:
        pass

    try:
        print('MAM: ', len(np.where(MAM.time_delta_qh < 0)[0]) / len(MAM) * 100)
    except ZeroDivisionError:
        pass

    try:
        print('JJA: ', len(np.where(JJA.time_delta_qh < 0)[0]) / len(JJA) * 100)
    except ZeroDivisionError:
        pass

    try:
        print('SON: ', len(np.where(SON.time_delta_qh < 0)[0]) / len(SON) * 100)
    except ZeroDivisionError:
        pass

    print('end')


if __name__ == "__main__":
    # read_peak_csvs('IMU_BTT')
    peak_stats_by_season('BCT_IMU')
