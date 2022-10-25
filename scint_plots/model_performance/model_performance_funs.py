import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
        obs_av = read_calculated_fluxes.time_averages_of_obs(obs, 'QH', on_hour=True)

        # combine obs and model
        df = pd.concat([obs_av, UKV.rename('UKV')], axis=1).dropna()

        # take differences
        df['diff_1'] = (df.UKV - df.obs_1) / np.abs(df.obs_1)
        df['diff_5'] = (df.UKV - df.obs_5) / np.abs(df.obs_5)
        df['diff_10'] = (df.UKV - df.obs_10) / np.abs(df.obs_10)
        df['diff_60'] = (df.UKV - df.obs_60) / np.abs(df.obs_60)

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
    plt.plot(DOY_df_dict[2016123].index.hour, DOY_df_dict[2016123].diff_1, marker='x', label='Cloudy 1', color='black',
             linestyle='dotted')
    plt.plot(DOY_df_dict[2016126].index.hour, DOY_df_dict[2016126].diff_1, marker='o', label='Clear 1', color='black')

    # 5 mins
    plt.plot(DOY_df_dict[2016123].index.hour, DOY_df_dict[2016123].diff_5, marker='x', label='Cloudy 5', color='green',
             linestyle='dotted')
    plt.plot(DOY_df_dict[2016126].index.hour, DOY_df_dict[2016126].diff_5, marker='o', label='Clear 5', color='green')

    # 10 mins
    plt.plot(DOY_df_dict[2016123].index.hour, DOY_df_dict[2016123].diff_10, marker='x', label='Cloudy 10', color='red',
             linestyle='dotted')
    plt.plot(DOY_df_dict[2016126].index.hour, DOY_df_dict[2016126].diff_10, marker='o', label='Clear 10', color='red')

    # 60 mins
    plt.plot(DOY_df_dict[2016123].index.hour, DOY_df_dict[2016123].diff_60, marker='x', label='Cloudy 60',
             color='purple', linestyle='dotted')
    plt.plot(DOY_df_dict[2016126].index.hour, DOY_df_dict[2016126].diff_60, marker='o', label='Clear 60',
             color='purple')

    # plt.gcf().autofmt_xdate()
    # ax.xaxis.set_major_formatter(DateFormatter('%H'))

    plt.ylabel('(UKV-$Q_{H}^{surf}$ - LAS-$Q_{H}$) / LAS-$Q_{H}$')
    plt.xlabel('Time (h, UTC)')

    plt.axhline(y=0, color='k', linestyle='-', linewidth=0.8)

    plt.legend(fontsize=15)

    # save plot
    plt.savefig('./' + 'model_performance.png', bbox_inches='tight', dpi=300)
    print('end')
