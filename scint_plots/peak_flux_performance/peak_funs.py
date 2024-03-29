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


def peak_analysis_plot(peak_path_dict, average, save_path):
    """

    :param peak_df:
    :param save_path:
    :return:
    """

    # get extreme vals
    dt_mins = []
    dt_maxs = []
    ax_mins = []
    ax_maxs = []
    for pair_id in peak_path_dict:
        peak_df = peak_path_dict[pair_id]
        dt_mins.append(peak_df.time_delta_qh.min())
        dt_maxs.append(peak_df.time_delta_qh.max())
        ax_mins.append(peak_df.MBE_qh_day.min())
        ax_mins.append(peak_df.value_delta_qh.min())
        ax_maxs.append(peak_df.MBE_qh_day.max())
        ax_maxs.append(peak_df.value_delta_qh.max())

    cbar_min = min(dt_mins)
    cbar_max = max(dt_maxs)
    ax_min = min(ax_mins) - 10
    ax_max = max(ax_maxs) + 10

    # ToDo: move this and every version of this into a lookup
    colour_dict = {'BCT_IMU': 'red', 'SCT_SWT': 'mediumorchid', 'IMU_BTT': 'green', 'BTT_BCT': 'blue'}
    marker_dict = {'BCT_IMU': 'o', 'SCT_SWT': 'v', 'IMU_BTT': 's', 'BTT_BCT': '^'}

    # plt.figure(figsize=(10, 8))
    fig, ax = plt.subplots(1, 2, figsize=(9, 8), gridspec_kw={'width_ratios': [1, 0.1]})

    cmap = cm.get_cmap('PiYG')

    bounds = np.linspace(cbar_min, cbar_max, int(np.abs(cbar_max) + np.abs(cbar_min) + 1))
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    # keep track of pair_id's included
    pair_ids = []

    for pair_id in peak_path_dict:
        peak_df = peak_path_dict[pair_id]

        ye = ax[0].scatter(peak_df.MBE_qh_day, peak_df.value_delta_qh, c=peak_df.time_delta_qh, cmap=cmap, norm=norm,
                           edgecolors=colour_dict[pair_id],
                           marker=marker_dict[pair_id],
                           label=pair_id, zorder=3, linewidth=0.65)

        slope, intercept, r_value, p_value, std_err = linregress(peak_df.MBE_qh_day, peak_df.value_delta_qh)
        string_for_leg = 'y = ' + str(round(slope, 2)) + 'x + ' + str(round(intercept, 1))

        ax[0].plot(np.array([-1000, 1000]), slope * np.array([-1000, 1000]) + intercept, color=colour_dict[pair_id],
                   label=string_for_leg, zorder=2)

        pair_ids.append(pair_id)

    ax[0].plot([-1000, 1000], [-1000, 1000], color='k', linestyle=':', alpha=0.5, label='Identity', zorder=1)

    cax = ax[1]
    cbar = fig.colorbar(mappable=ye, cax=cax)
    cbar.set_ticks(np.arange(cbar_min, cbar_max + 1, step=1))

    cbar.ax.set_ylabel('Time Offset (h)')
    ax[0].set_xlabel('day MBE (W m$^{-2}$)')
    ax[0].set_ylabel('peak BE (W m$^{-2}$)')

    ax[0].set_xlim(ax_min, ax_max)
    ax[0].set_ylim(ax_min, ax_max)

    handles, labels = ax[0].get_legend_handles_labels()

    for i, label in enumerate(labels):
        if label in pair_ids:
            # set scatter points to have black facecolour
            handles[i].set_facecolor('white')

    ax[0].legend(handles=handles, loc='best')

    fig.tight_layout()
    plt.subplots_adjust(wspace=0.02, hspace=0.02)

    # plt.show()
    plt.savefig(save_path + str(average) + '_peak.png', bbox_inches='tight', dpi=300)

    print('end')


def peak_stats(path_dict):
    """

    Returns
    -------

    """

    for pair_id in path_dict.keys():
        print(' ')
        print(pair_id)
        print(' ')

        df = path_dict[pair_id]

        print('len dt 5, 6: ', len(df[df['time_delta_qh'].between(5, 6)]))
        print('len dt 3, 4: ', len(df[df['time_delta_qh'].between(3, 4)]))
        print('len dt 1, 2: ', len(df[df['time_delta_qh'].between(1, 2)]))
        print('len dt 0: ', len(df[df['time_delta_qh'] == 0]))
        print('len dt -2, -1: ', len(df[df['time_delta_qh'].between(-2, -1)]))
        print('len dt -4, -3: ', len(df[df['time_delta_qh'].between(-4, -3)]))
        print('len dt -6, -5: ', len(df[df['time_delta_qh'].between(-6, -5)]))

        # peak MBE
        print('peak MBE: ', df.value_delta_qh.mean())

        # day MBE
        print('DAY MBE: ', df.MBE_qh_day.mean())

    print('end')


def peak_stats_by_season(path_dict):
    """

    :param path_dict:
    :return:
    """

    for pair_id in path_dict.keys():
        print(' ')
        print(pair_id)
        print(' ')

        df = path_dict[pair_id]

        # split into seasons
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

        # print % days positive dt

        print('% of positive dt :')
        print('ALL: ' , len(np.where(df.time_delta_qh > 0)[0]) / len(df) * 100)

        try:
            print('DJF: ', len(np.where(DJF.time_delta_qh > 0)[0]) / len(DJF) * 100)
        except ZeroDivisionError:
            pass
        try:
            print('MAM: ', len(np.where(MAM.time_delta_qh > 0)[0]) / len(MAM) * 100)
        except ZeroDivisionError:
            pass
        try:
            print('JJA: ', len(np.where(JJA.time_delta_qh > 0)[0]) / len(JJA) * 100)
        except ZeroDivisionError:
            pass
        try:
            print('SON: ', len(np.where(SON.time_delta_qh > 0)[0]) / len(SON) * 100)
        except ZeroDivisionError:
            pass

        print(' ')
        print('MBE')

        # peak MBE
        print('DJF peak MBE: ', DJF.value_delta_qh.mean())
        print('DJF DAY MBE: ', DJF.MBE_qh_day.mean())
        print('MAM peak MBE: ', MAM.value_delta_qh.mean())
        print('MAM DAY MBE: ', MAM.MBE_qh_day.mean())
        print('JJA peak MBE: ', JJA.value_delta_qh.mean())
        print('JJA DAY MBE: ', JJA.MBE_qh_day.mean())
        print('SON peak MBE: ', SON.value_delta_qh.mean())
        print('SON DAY MBE: ', SON.MBE_qh_day.mean())

    print('end')
