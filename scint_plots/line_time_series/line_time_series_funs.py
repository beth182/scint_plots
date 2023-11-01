import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from matplotlib.dates import DateFormatter
import pandas as pd
import matplotlib as mpl
import os

mpl.rcParams.update({'font.size': 15})


def times_series_line_QH_KDOWN(df, pair_id, model_df=False):
    """
    TIME SERIES OF Q AND KDOWN LINE PLOT
    :return:
    """
    plt.close('all')

    fig = plt.figure(figsize=(8, 7))
    ax = plt.subplot(1, 1, 1)

    ax.plot(df['QH'], label='$Q_{H}$', linewidth=1)
    ax.plot(df['kdown'], label='$K_{\downarrow}$', linewidth=1)

    if type(model_df) == pd.core.frame.Series or type(model_df) == pd.core.frame.DataFrame:
        # push the index of kdown forward 15 min
        # ToDo: make sure that this is time adjustment is always just made for the pre-made dfs
        kdown_UKV_df = model_df.kdown_UKV.dropna()
        kdown_UKV_df.index = model_df.kdown_UKV.dropna().index + dt.timedelta(minutes=15)

        ax.plot(model_df.BL_H_UKV.dropna(), label='UKV $Q_{H}$')
        ax.plot(kdown_UKV_df, label='UKV $K_{\downarrow}$')

    ax.set_xlabel('Time (h, UTC)')
    ax.set_ylabel('Flux (W $m^{-2}$)')

    # where QH is not nan
    df_not_nan = df.iloc[np.where(np.isnan(df.QH) == False)[0]]

    ax.set_xlim(min(df_not_nan.index) - dt.timedelta(minutes=10), max(df_not_nan.index) + dt.timedelta(minutes=10))

    # plt.legend()
    plt.legend(loc='upper left', )

    # plt.gcf().autofmt_xdate()

    ax.xaxis.set_major_formatter(DateFormatter('%H'))

    if df.index[0].strftime('%Y%j') == '2016126':
        plt.title('Clear')
        ax.set_ylim(0, 1000)

    elif df.index[0].strftime('%Y%j') == '2016123':
        plt.title('Cloudy')
        ax.set_ylim(0, 1000)

    else:
        plt.title(df.index[0].strftime('%Y%j'))

    # save plot
    date_string = df['QH'].dropna().index[0].strftime('%Y%j')

    # ToDo: a proper solution for here
    dir_name = './'
    """
    if type(model_df) == bool:
        if model_df == False:
            dir_name = './'
        else:
            raise ValueError('Type of model df has gone wrong.')

    else:
        main_dir = 'C:/Users/beths/OneDrive - University of Reading/Paper 2/FLUX_PLOTS/'
        dir_name = main_dir + date_string + '/'
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    """

    plt.savefig(dir_name + pair_id + '_' + date_string + '_line_plot.png', bbox_inches='tight', dpi=300)

    print('end')


def times_series_line_QH_KDOWN_UM100(df, pair_id, UM_100=False):
    """
    TIME SERIES OF Q AND KDOWN LINE PLOT
    :return:
    """
    plt.close('all')

    fig = plt.figure(figsize=(8, 7))
    ax = plt.subplot(1, 1, 1)

    ax.plot(df['QH'], label='$Q_{H}$', linewidth=1, alpha=0.5, color='orange')

    # label='UKV $Q_{H}$'

    ax.set_xlabel('Time (h, UTC)')
    ax.set_ylabel('Flux (W $m^{-2}$)')

    # where QH is not nan
    df_not_nan = df.iloc[np.where(np.isnan(df.QH) == False)[0]]

    ax.set_xlim(min(df_not_nan.index) - dt.timedelta(minutes=10), max(df_not_nan.index) + dt.timedelta(minutes=10))

    if UM_100:
        # read the premade csv
        UM100_csv_path = 'D:/Documents/scint_UM100/scint_UM100/data_retreval/BCT_IMU_134_UM100_QH_100m.csv'
        UM_100_df = pd.read_csv(UM100_csv_path)

        UM_100_df.index = UM_100_df.hour.astype('timedelta64[h]') + df.index[0]

        ax.plot(UM_100_df.weighted_av_a.dropna(), label='W UM100 $Q_{H}$', color='red')
        ax.plot(UM_100_df.av_a.dropna(), label='NW UM100 $Q_{H}$', color='red', linestyle='--')

        # UM300

        # read the premade csv
        UM300_csv_path = 'D:/Documents/scint_UM100/scint_UM100/data_retreval/BCT_IMU_134_UM100_QH_300m.csv'
        UM_300_df = pd.read_csv(UM300_csv_path)

        UM_300_df.index = UM_300_df.hour.astype('timedelta64[h]') + df.index[0]

        ax.plot(UM_300_df.weighted_av_a.dropna(), label='W UM300 $Q_{H}$', color='purple')
        ax.plot(UM_300_df.av_a.dropna(), label='NW UM300 $Q_{H}$', color='purple', linestyle='--')

        # UKV
        # read the premade csv
        UMukv_csv_path = 'D:/Documents/scint_UM100/scint_UM100/data_retreval/BCT_IMU_134_UM100_QH_ukv.csv'
        UM_ukv_df = pd.read_csv(UMukv_csv_path)

        UM_ukv_df.index = UM_ukv_df.hour.astype('timedelta64[h]') + df.index[0]

        ax.plot(UM_ukv_df.weighted_av_a.dropna(), label='W UKV $Q_{H}$', color='blue')
        ax.plot(UM_ukv_df.av_a.dropna(), label='NW UKV $Q_{H}$', color='blue', linestyle='--')

    # plt.legend()
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # plt.gcf().autofmt_xdate()
    ax.xaxis.set_major_formatter(DateFormatter('%H'))

    if df.index[0].strftime('%Y%j') == '2016126':
        plt.title('Clear')
        ax.set_ylim(0, 1000)

    elif df.index[0].strftime('%Y%j') == '2016123':
        plt.title('Cloudy')
        ax.set_ylim(0, 1000)

    else:
        plt.title(df.index[0].strftime('%Y%j'))

    # save plot
    date_string = df['QH'].dropna().index[0].strftime('%Y%j')

    # ToDo: a proper solution for here
    dir_name = './'
    """
    if type(model_df) == bool:
        if model_df == False:
            dir_name = './'
        else:
            raise ValueError('Type of model df has gone wrong.')

    else:
        main_dir = 'C:/Users/beths/OneDrive - University of Reading/Paper 2/FLUX_PLOTS/'
        dir_name = main_dir + date_string + '/'
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    """

    plt.savefig(dir_name + pair_id + '_' + date_string + '_UM100_line_plot.png', bbox_inches='tight', dpi=300)

    print('end')


def times_series_line_QH_KDOWN_REVIEW_EXAMPLE(DOY_dict, pair_id, model_df=False):
    """
    TIME SERIES OF Q AND KDOWN LINE PLOT
    :return:
    """
    plt.close('all')

    fig = plt.figure(figsize=(8, 7))
    ax = plt.subplot(1, 1, 1)



    ax.plot(DOY_dict[2016126]['1']['QH'], label='$Q_{H}$ 1min', linewidth=1, alpha=0.5)
    ax.plot(DOY_dict[2016126]['1']['kdown'], label='$K_{\downarrow}$', linewidth=1)


    ax.scatter(DOY_dict[2016126]['2'].index, DOY_dict[2016126]['2']['QH'], label='2min', marker= '.', color='green')

    ax.scatter(DOY_dict[2016126]['3'].index, DOY_dict[2016126]['3']['QH'], label='3min', marker='+', color='purple')

    ax.scatter(DOY_dict[2016126]['5'].index, DOY_dict[2016126]['5']['QH'], label='5min', marker='x', color='darkblue')

    ax.scatter(DOY_dict[2016126]['10'].index, DOY_dict[2016126]['10']['QH'], label='10min', marker='o', color='red')


    ax.scatter(DOY_dict[2016126]['2'].index, DOY_dict[2016126]['2']['kdown'], marker= '.', color='green')

    ax.scatter(DOY_dict[2016126]['3'].index, DOY_dict[2016126]['3']['kdown'], marker='+', color='purple')

    ax.scatter(DOY_dict[2016126]['5'].index, DOY_dict[2016126]['5']['kdown'], marker='x', color='darkblue')

    ax.scatter(DOY_dict[2016126]['10'].index, DOY_dict[2016126]['10']['kdown'], marker='o', color='red')








    ax.set_xlabel('Time')
    ax.set_ylabel('Flux (W $m^{-2}$)')



    # CHANGE HERE
    # ax.set_xlim(min(DOY_dict[2016126]['1'].index) - dt.timedelta(minutes=10), max(DOY_dict[2016126]['1'].index) + dt.timedelta(minutes=10))

    ax.set_xlim(DOY_dict[2016126]['1'].iloc[np.where(np.logical_and(DOY_dict[2016126]['1'].index.hour>=13, DOY_dict[2016126]['1'].index.hour<=15))[0]].index[0],
                DOY_dict[2016126]['1'].iloc[np.where(np.logical_and(DOY_dict[2016126]['1'].index.hour>=13, DOY_dict[2016126]['1'].index.hour<=15))[0]].index[-1])

    # plt.legend()
    plt.legend(loc='best')

    # plt.gcf().autofmt_xdate()

    # CHANGE HERE
    # ax.xaxis.set_major_formatter(DateFormatter('%H'))
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))


    plt.title('Clear')
    ax.set_ylim(0, 1000)


    # save plot
    date_string = DOY_dict[2016126]['1']['QH'].dropna().index[0].strftime('%Y%j')

    # ToDo: a proper solution for here
    dir_name = './'
    """
    if type(model_df) == bool:
        if model_df == False:
            dir_name = './'
        else:
            raise ValueError('Type of model df has gone wrong.')

    else:
        main_dir = 'C:/Users/beths/OneDrive - University of Reading/Paper 2/FLUX_PLOTS/'
        dir_name = main_dir + date_string + '/'
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    """

    plt.show()

    plt.savefig(dir_name + pair_id + '_' + date_string + '_line_plot.png', bbox_inches='tight', dpi=300)

    print('end')
