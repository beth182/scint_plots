import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from matplotlib.dates import DateFormatter
import pandas as pd
import matplotlib as mpl
import os
from scipy import stats

mpl.rcParams.update({'font.size': 15})

def ts_scatter_plot(df, pair_id, minute_displace=0):
    """

    :return:
    """

    plt.close('all')



    df = df.dropna()


    QH_series = df.QH
    QH_series.index = df.index + dt.timedelta(minutes=minute_displace)

    df_new = pd.concat([QH_series, df.kdown], axis=1).dropna()

    gradient0, intercept0, r_value0, p_value0, std_err0 = stats.linregress(df_new['QH'], df_new['kdown'])
    r_string = 'r = ' + str(round(r_value0, 2))


    """
    fig = plt.figure(figsize=(8, 7))
    ax = plt.subplot(1, 1, 1)

    ax.scatter(df_new['QH'], df_new['kdown'], marker='.', label=r_string)


    # ToDo: fix label format
    ax.set_xlabel('QH (W $m^{-2}$)')
    ax.set_ylabel('Kdown (W $m^{-2}$)')

    ax.set_ylim(0, 900)
    ax.set_xlim(0, 900)

    plt.title(df.index[0].strftime('%Y%j'))

    plt.legend()

    # save plot
    dir_name = './'
    date_string = df['QH'].dropna().index[0].strftime('%Y%j')
    plt.savefig(dir_name + pair_id + '_' + date_string + '_ts_scatter_' + str(minute_displace) + '.png', bbox_inches='tight', dpi=300)
    
    print('end')
    
    """

    return r_value0







