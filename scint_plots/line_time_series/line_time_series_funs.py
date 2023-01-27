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
        ax.plot(model_df.BL_H_UKV.dropna(), label='UKV $Q_{H}$')
        ax.plot(model_df.kdown_UKV.dropna(), label='UKV $K_{\downarrow}$')

    ax.set_xlabel('Time (h, UTC)')
    ax.set_ylabel('Flux (W $m^{-2}$)')

    # where QH is not nan
    df_not_nan = df.iloc[np.where(np.isnan(df.QH) == False)[0]]

    ax.set_xlim(min(df_not_nan.index) - dt.timedelta(minutes=10), max(df_not_nan.index) + dt.timedelta(minutes=10))

    plt.legend()

    # plt.gcf().autofmt_xdate()
    ax.xaxis.set_major_formatter(DateFormatter('%H'))

    if df.index[0].strftime('%j') == '126':
        plt.title('Clear')
        ax.set_ylim(0, 1000)

    elif df.index[0].strftime('%j') == '123':
        plt.title('Cloudy')
        ax.set_ylim(0, 1000)


    # save plot
    date_string = df['QH'].dropna().index[0].strftime('%Y%j')

    if model_df == False:
        dir_name = './'

    else:
        main_dir = 'C:/Users/beths/OneDrive - University of Reading/Paper 2/categorize_days/FLUX_PLOTS/'
        dir_name = main_dir + date_string + '/'
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    plt.savefig(dir_name + pair_id + '_' + date_string + '_line_plot.png', bbox_inches='tight', dpi=300)

    print('end')