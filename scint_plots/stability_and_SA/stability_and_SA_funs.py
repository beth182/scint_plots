import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import gridspec
import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib as mpl

mpl.rcParams.update({'font.size': 15})


def stability_and_sa(obs_df):
    """

    Returns
    -------

    """

    # reading the observation nc files
    assert 2016126 in obs_df.keys() and 2016123 in obs_df.keys()
    df_126_10 = obs_df[2016126]['1min_sa10min']
    df_126_60 = obs_df[2016126]['1min']
    df_123_10 = obs_df[2016123]['1min_sa10min']
    df_123_60 = obs_df[2016123]['1min']

    df_126_60 = df_126_60.resample('60T', closed='right', label='right').mean()
    df_123_60 = df_123_60.resample('60T', closed='right', label='right').mean()

    df_126_10 = df_126_10.resample('10T', closed='right', label='right').mean()
    df_123_10 = df_123_10.resample('10T', closed='right', label='right').mean()

    # reading the sa csv files - for sig v
    footprint_csv_path_126 = 'C:/Users/beths/Desktop/LANDING/fp_output/met_inputs_minutes_126.csv'
    footprint_csv_path_123 = 'C:/Users/beths/Desktop/LANDING/fp_output/met_inputs_minutes_123.csv'
    csv_df_123 = pd.read_csv(footprint_csv_path_123)
    csv_df_126 = pd.read_csv(footprint_csv_path_126)
    try:
        csv_df_123['Unnamed: 0'] = pd.to_datetime(csv_df_123['Unnamed: 0'], format='%Y-%m-%d %H:%M:%S')
    except ValueError:
        csv_df_123['Unnamed: 0'] = pd.to_datetime(csv_df_123['Unnamed: 0'], format='%d/%m/%Y %H:%M')
    try:
        csv_df_126['Unnamed: 0'] = pd.to_datetime(csv_df_126['Unnamed: 0'], format='%Y-%m-%d %H:%M:%S')
    except ValueError:
        csv_df_126['Unnamed: 0'] = pd.to_datetime(csv_df_126['Unnamed: 0'], format='%d/%m/%Y %H:%M')

    csv_df_123.index = csv_df_123['Unnamed: 0']
    csv_df_123 = csv_df_123.drop('Unnamed: 0', 1)
    csv_df_126.index = csv_df_126['Unnamed: 0']
    csv_df_126 = csv_df_126.drop('Unnamed: 0', 1)

    csv_df_123 = csv_df_123[['sig_v']]
    csv_df_126 = csv_df_126[['sig_v']]
    csv_df_123.columns = ['sig_v_123']
    csv_df_126.columns = ['sig_v_126']

    df_123_10 = pd.concat([df_123_10, csv_df_123], axis=1).dropna()
    df_126_10 = pd.concat([df_126_10, csv_df_126], axis=1).dropna()

    df_123_60 = df_123_60.dropna()
    df_126_60 = df_126_60.dropna()

    # construct datetime obj for both days with same year day etc. (for colourbar)
    format_index_123_10 = df_123_10.index.strftime('%H:%M')
    index_list_123_10 = []
    for i in format_index_123_10:
        datetime_object = dt.datetime.strptime(i, '%H:%M')
        index_list_123_10.append(datetime_object)
    df_123_10.index = index_list_123_10

    format_index_126_10 = df_126_10.index.strftime('%H:%M')
    index_list_126_10 = []
    for i in format_index_126_10:
        datetime_object = dt.datetime.strptime(i, '%H:%M')
        index_list_126_10.append(datetime_object)
    df_126_10.index = index_list_126_10

    format_index_123_60 = df_123_60.index.strftime('%H:%M')
    index_list_123_60 = []
    for i in format_index_123_60:
        datetime_object = dt.datetime.strptime(i, '%H:%M')
        index_list_123_60.append(datetime_object)
    df_123_60.index = index_list_123_60

    format_index_126_60 = df_126_60.index.strftime('%H:%M')
    index_list_126_60 = []
    for i in format_index_126_60:
        datetime_object = dt.datetime.strptime(i, '%H:%M')
        index_list_126_60.append(datetime_object)
    df_126_60.index = index_list_126_60

    # Resample sig v to 60 min averages
    sig_v_123_60 = df_123_10.sig_v_123.resample('60T', closed='right', label='right').mean()
    sig_v_126_60 = df_126_10.sig_v_126.resample('60T', closed='right', label='right').mean()

    # find max and min time
    min_time = min(df_123_10.index.min(), df_126_10.index.min(), df_126_60.index.min(), df_123_60.index.min())
    max_time = max(df_123_10.index.max(), df_126_10.index.max(), df_126_60.index.max(), df_123_60.index.max())

    # plotting
    fig = plt.figure(figsize=(15, 8))
    spec = gridspec.GridSpec(ncols=3, nrows=2)

    ax1 = plt.subplot(spec[0])
    ax2 = plt.subplot(spec[1])
    ax3 = plt.subplot(spec[2])
    ax4 = plt.subplot(spec[3])
    ax5 = plt.subplot(spec[4])
    ax6 = plt.subplot(spec[5])

    # sigv
    ax1.plot(df_126_10.index, df_126_10.sig_v_126, marker='.', linewidth=0.5, color='blue', alpha=0.3)
    ax1.plot(df_123_10.index, df_123_10.sig_v_123, marker='.', linewidth=0.5, color='red', alpha=0.3)

    ax1.plot(sig_v_126_60.index, sig_v_126_60, marker='o', color='blue')
    ax1.plot(sig_v_123_60.index[:-1], sig_v_123_60[:-1], marker='o', color='red')

    ax1.set_ylabel('$\sigma_{v}$ (m s$^{-1}$)')

    # ustar
    # 10min
    ax2.plot(df_126_10.index, df_126_10.ustar, color='blue', alpha=0.3, linewidth=0.5, marker='.')
    ax2.plot(df_123_10.index, df_123_10.ustar, color='red', alpha=0.3, linewidth=0.5, marker='.')
    # hour
    ax2.plot(df_126_60.index, df_126_60.ustar, color='blue', marker='o')
    ax2.plot(df_123_60.index, df_123_60.ustar, color='red', marker='o')

    ax2.set_ylabel('u$_{*}$ (m s$^{-1}$)')

    # stab param
    # 10min
    ax3.plot(df_126_10.index, df_126_10.stab_param * -1, color='blue', alpha=0.3, linewidth=0.5, marker='.')
    ax3.plot(df_123_10.index, df_123_10.stab_param * -1, color='red', alpha=0.3, linewidth=0.5, marker='.')
    # hour
    ax3.plot(df_126_60.index, df_126_60.stab_param * -1, color='blue', marker='o', label='Clear')
    ax3.plot(df_123_60.index, df_123_60.stab_param * -1, color='red', marker='o', label='Cloudy')

    ax3.set_ylabel('- z$_{f}$/L', labelpad=-5)
    ax3.set_yscale('log')
    ax3.set_ylim(ax3.get_ylim()[::-1])
    ax3.legend()

    # z0
    # 10min
    ax4.plot(df_126_10.index, df_126_10.z_0, color='blue', alpha=0.3, linewidth=0.5, marker='.')
    ax4.plot(df_123_10.index, df_123_10.z_0, color='red', alpha=0.3, linewidth=0.5, marker='.')
    # hour
    ax4.plot(df_126_60.index, df_126_60.z_0, color='blue', marker='o')
    ax4.plot(df_123_60.index, df_123_60.z_0, color='red', marker='o')

    ax4.set_ylabel('z$_{0}$ (m)')

    # zf
    # 10 min
    ax5.plot(df_126_10.index, df_126_10.z_f, color='blue', alpha=0.3, linewidth=0.5, marker='.')
    ax5.plot(df_123_10.index, df_123_10.z_f, color='red', alpha=0.3, linewidth=0.5, marker='.')
    # hour
    ax5.plot(df_126_60.index, df_126_60.z_f, color='blue', marker='o')
    ax5.plot(df_123_60.index, df_123_60.z_f, color='red', marker='o')

    ax5.set_ylabel('z$_{f}$ (m)')

    # sa area
    # 10 min
    ax6.plot(df_126_10.index, df_126_10.sa_area_km2, color='blue', alpha=0.3, linewidth=0.5, marker='.', label='10 min')
    ax6.plot(df_123_10.index, df_123_10.sa_area_km2, color='red', alpha=0.3, linewidth=0.5, marker='.')
    # hour
    ax6.plot(df_126_60.index, df_126_60.sa_area_km2, color='blue', marker='o', label='60 min')
    ax6.plot(df_123_60.index, df_123_60.sa_area_km2, color='red', marker='o')

    ax6.legend()

    ax6.set_ylabel('SA area (km$^{2}$)')

    ax1.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))
    ax2.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))
    ax3.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))
    ax4.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))
    ax5.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))
    ax6.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))

    ax1.xaxis.set_major_formatter(DateFormatter('%H'))
    ax2.xaxis.set_major_formatter(DateFormatter('%H'))
    ax3.xaxis.set_major_formatter(DateFormatter('%H'))
    ax4.xaxis.set_major_formatter(DateFormatter('%H'))
    ax5.xaxis.set_major_formatter(DateFormatter('%H'))
    ax6.xaxis.set_major_formatter(DateFormatter('%H'))

    ax5.set_xlabel('Time (h, UTC)')

    fig.subplots_adjust(wspace=0.28, hspace=0)

    # plt.show()
    plt.savefig('./stab_and_SA_vars.png', bbox_inches='tight', dpi=300)

    """
    # Getting intensity of instability
    df_126_10.stab_param.max()  # -0.94
    df_126_10.stab_param.min()  # -6244.50

    df_123_10.stab_param.max()  # -0.11
    df_123_10.stab_param.min()  # -1.69
    """

    """
    # Getting magnitude of friction velocity
    df_126_10.ustar.max()  # 0.56
    df_123_10.ustar.max()  # 0.92
    """

    """
    # Getting SIG V
    df_126_10.sig_v_126.max()  # 2.36
    df_126_10.sig_v_126.min()  # 0.20

    df_123_10.sig_v_123.max()  # 1.90
    df_123_10.sig_v_123.min()  # 0.36
    """

    print('end')
