import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib.lines import Line2D

mpl.rcParams.update({'font.size': 15})

from scint_flux.functions import read_calculated_fluxes


def plot_difference(DOY_dict):
    assert 2016123 in DOY_dict.keys()
    assert 2016126 in DOY_dict.keys()

    DOY_df_dict = {}

    for DOY in DOY_dict.keys():
        # unwrap the data
        obs = DOY_dict[DOY]['obs']
        UKV = DOY_dict[DOY]['UKV_QH'].WAverage

        # time average the observations
        # obs_av = read_calculated_fluxes.time_averages_of_obs(obs, 'QH', on_hour=True)

        # combine obs and model
        df = pd.concat([obs, UKV.rename('UKV')], axis=1).dropna()

        # take differences
        df['diff_1'] = (df.UKV - df.QH_obs_1) / np.abs(df.QH_obs_1)
        df['diff_5'] = (df.UKV - df.QH_obs_5) / np.abs(df.QH_obs_5)
        df['diff_10'] = (df.UKV - df.QH_obs_10) / np.abs(df.QH_obs_10)
        df['diff_60'] = (df.UKV - df.QH_obs_60) / np.abs(df.QH_obs_60)

        # print averages for reference
        print(' ')
        print('DOY: ', DOY)
        print('average diff 1: ', np.average(np.abs(df.diff_1)))
        print('average diff 5: ', np.average(np.abs(df.diff_5)))
        print('average diff 10: ', np.average(np.abs(df.diff_10)))
        print('average diff 60: ', np.average(np.abs(df.diff_60)))

        DOY_df_dict[DOY] = df

    # Make plot
    plt.close('all')
    plt.figure(figsize=(10, 8))
    ax = plt.subplot(1, 1, 1)

    # 1 mins
    plt.plot(DOY_df_dict[2016123].index.hour.values, DOY_df_dict[2016123].diff_1.values, marker='x', color='blue', linestyle='dotted')
    plt.plot(DOY_df_dict[2016126].index.hour.values, DOY_df_dict[2016126].diff_1.values, marker='o', color='blue')

    # 5 mins
    plt.plot(DOY_df_dict[2016123].index.hour.values, DOY_df_dict[2016123].diff_5.values, marker='x', color='green',
             linestyle='dotted')
    plt.plot(DOY_df_dict[2016126].index.hour.values, DOY_df_dict[2016126].diff_5.values, marker='o', color='green')

    # 10 mins
    plt.plot(DOY_df_dict[2016123].index.hour.values, DOY_df_dict[2016123].diff_10.values, marker='x', color='red', linestyle='dotted')
    plt.plot(DOY_df_dict[2016126].index.hour.values, DOY_df_dict[2016126].diff_10.values, marker='o', color='red')

    # 60 mins
    plt.plot(DOY_df_dict[2016123].index.hour.values, DOY_df_dict[2016123].diff_60.values, marker='x', color='purple',
             linestyle='dotted')
    plt.plot(DOY_df_dict[2016126].index.hour.values, DOY_df_dict[2016126].diff_60.values, marker='o', color='purple')

    # plt.gcf().autofmt_xdate()
    # ax.xaxis.set_major_formatter(DateFormatter('%H'))

    plt.ylabel('($UKV_{surface}$ - $Q_{H,LAS}$) / $Q_{H,LAS}$')
    plt.xlabel('Time (h, UTC)')

    plt.axhline(y=0, color='k', linestyle='-', linewidth=0.8)

    # construct legend manually
    handles, labels = plt.gca().get_legend_handles_labels()
    cloudy_line = Line2D([0], [0], label='IOP-1', color='black', linestyle='dotted', marker='x')
    clear_line = Line2D([0], [0], label='IOP-2', color='black', marker='o')
    av1_line = Line2D([0], [0], label='1 min', color='blue')
    av5_line = Line2D([0], [0], label='5 min', color='green')
    av10_line = Line2D([0], [0], label='10 min', color='red')
    av60_line = Line2D([0], [0], label='60 min', color='purple')
    handles.extend([cloudy_line, clear_line, av1_line, av5_line, av10_line, av60_line])

    plt.legend(handles=handles, fontsize=15)

    # save plot
    plt.savefig('./' + 'model_performance.png', bbox_inches='tight', dpi=300)
    print('end')
