import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import gridspec
import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib as mpl

from scint_fp.create_input_csvs import wx_u_v_components

mpl.rcParams.update({'font.size': 15})


def stability_and_sa(df_dict):
    """

    Returns
    -------

    """

    # reading the observation nc files
    assert 2016126 in df_dict.keys() and 2016123 in df_dict.keys()
    df_126_10 = df_dict[2016126]['1min_sa10min']
    df_126_60 = df_dict[2016126]['1min']
    df_123_10 = df_dict[2016123]['1min_sa10min']
    df_123_60 = df_dict[2016123]['1min']

    # reading model wind
    df_123_ukv = df_dict[2016123]['UKV']['UKV_wind']
    df_126_ukv = df_dict[2016126]['UKV']['UKV_wind']

    # reading model height
    UKV_126_z = df_dict[2016126]['UKV']['UKV_height']
    UKV_123_z = df_dict[2016123]['UKV']['UKV_height']
    assert UKV_123_z == UKV_126_z

    # average wind dir obs
    # convert wind speed and direction to u & v components, to average, then convert the averages back
    component_df_123_10 = wx_u_v_components.ws_wd_to_u_v(df_123_10['wind_speed_adj'],
                                                         df_123_10['wind_direction_corrected'])
    component_df_123_60 = wx_u_v_components.ws_wd_to_u_v(df_123_60['wind_speed_adj'],
                                                         df_123_60['wind_direction_corrected'])
    component_df_126_10 = wx_u_v_components.ws_wd_to_u_v(df_126_10['wind_speed_adj'],
                                                         df_126_10['wind_direction_corrected'])
    component_df_126_60 = wx_u_v_components.ws_wd_to_u_v(df_126_60['wind_speed_adj'],
                                                         df_126_60['wind_direction_corrected'])

    # 60 mins from hourly SA
    df_123_comp_60 = component_df_123_60.resample('60T', closed='right', label='right').mean()
    df_126_comp_60 = component_df_126_60.resample('60T', closed='right', label='right').mean()

    # 10 min averages
    df_126_comp_10 = component_df_126_10.resample('10T', closed='right', label='right').mean()
    df_123_comp_10 = component_df_123_10.resample('10T', closed='right', label='right').mean()

    # convert back to ws and direction
    av_123_60 = wx_u_v_components.u_v_to_ws_wd(df_123_comp_60['u_component'], df_123_comp_60['v_component'])
    av_126_60 = wx_u_v_components.u_v_to_ws_wd(df_126_comp_60['u_component'], df_126_comp_60['v_component'])

    av_126_10 = wx_u_v_components.u_v_to_ws_wd(df_126_comp_10['u_component'], df_126_comp_10['v_component'])
    av_123_10 = wx_u_v_components.u_v_to_ws_wd(df_123_comp_10['u_component'], df_123_comp_10['v_component'])

    # remove wind speed and direction columns - these have been averaged seperatly
    df_126_60 = df_126_60.drop(['wind_direction_corrected', 'wind_speed_adj'], axis=1)
    df_123_60 = df_123_60.drop(['wind_direction_corrected', 'wind_speed_adj'], axis=1)
    df_126_10 = df_126_10.drop(['wind_direction_corrected', 'wind_speed_adj'], axis=1)
    df_123_10 = df_123_10.drop(['wind_direction_corrected', 'wind_speed_adj'], axis=1)

    # average all vars apart from wind
    df_126_60 = df_126_60.resample('60T', closed='right', label='right').mean()
    df_123_60 = df_123_60.resample('60T', closed='right', label='right').mean()
    df_126_10 = df_126_10.resample('10T', closed='right', label='right').mean()
    df_123_10 = df_123_10.resample('10T', closed='right', label='right').mean()

    # combine the averaged wind df back into the pther averaged df
    df_126_60 = pd.concat([df_126_60, av_126_60], axis=1)
    df_123_60 = pd.concat([df_123_60, av_123_60], axis=1)
    df_126_10 = pd.concat([df_126_10, av_126_10], axis=1)
    df_123_10 = pd.concat([df_123_10, av_123_10], axis=1)

    # reading the sa csv files - for sig v
    footprint_csv_path_126 = 'C:/Users/beths/OneDrive - University of Reading/local_runs_data/fp_output/met_inputs_minutes_126.csv'
    footprint_csv_path_123 = 'C:/Users/beths/OneDrive - University of Reading/local_runs_data/fp_output/met_inputs_minutes_123.csv'
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

    # construct datetime obj for both days with same year day etc.
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

    format_index_123_ukv = df_123_ukv.index.strftime('%H:%M')
    index_list_123_ukv = []
    for i in format_index_123_ukv:
        datetime_object = dt.datetime.strptime(i, '%H:%M')
        index_list_123_ukv.append(datetime_object)
    df_123_ukv.index = index_list_123_ukv

    format_index_126_ukv = df_126_ukv.index.strftime('%H:%M')
    index_list_126_ukv = []
    for i in format_index_126_ukv:
        datetime_object = dt.datetime.strptime(i, '%H:%M')
        index_list_126_ukv.append(datetime_object)
    df_126_ukv.index = index_list_126_ukv

    # Resample sig v to 60 min averages
    sig_v_123_60 = df_123_10.sig_v_123.resample('60T', closed='right', label='right').mean()
    sig_v_126_60 = df_126_10.sig_v_126.resample('60T', closed='right', label='right').mean()

    # find max and min time
    min_time = min(df_123_10.index.min(), df_126_10.index.min(), df_126_60.index.min(), df_123_60.index.min())
    max_time = max(df_123_10.index.max(), df_126_10.index.max(), df_126_60.index.max(), df_123_60.index.max())

    # plotting
    fig = plt.figure(figsize=(15, 12))
    spec = gridspec.GridSpec(ncols=3, nrows=3)

    ax1 = plt.subplot(spec[0])
    ax2 = plt.subplot(spec[1])
    ax3 = plt.subplot(spec[2])
    ax4 = plt.subplot(spec[3])
    ax5 = plt.subplot(spec[4])
    ax6 = plt.subplot(spec[5])

    ax7 = plt.subplot(spec[6])
    ax8 = plt.subplot(spec[7])
    ax9 = plt.subplot(spec[8])

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
    ax3.plot(df_123_60.index, df_123_60.stab_param * -1, color='red', marker='o', label='IOP-1')
    ax3.plot(df_126_60.index, df_126_60.stab_param * -1, color='blue', marker='o', label='IOP-2')


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
    ax6.plot(df_126_10.index, df_126_10.sa_area_km2, color='blue', alpha=0.3, linewidth=0.5, marker='.')
    ax6.plot(df_123_10.index, df_123_10.sa_area_km2, color='red', alpha=0.3, linewidth=0.5, marker='.')
    # hour
    ax6.plot(df_126_60.index, df_126_60.sa_area_km2, color='blue', marker='o')
    ax6.plot(df_123_60.index, df_123_60.sa_area_km2, color='red', marker='o')

    ax6.plot([], [], color='black', marker='o', label='60 min')
    ax6.plot([], [], color='black', alpha=0.3, linewidth=0.5, marker='.', label='10 min')

    ax6.legend()

    ax6.set_ylabel('$SA_{LAS}$ area (km$^{2}$)')

    # wind speed
    # 10 min
    ax7.plot(df_126_10.index, df_126_10.wind_speed_convert, color='blue', alpha=0.3, linewidth=0.5, marker='.')
    ax7.plot(df_123_10.index, df_123_10.wind_speed_convert, color='red', alpha=0.3, linewidth=0.5, marker='.')
    # hour
    ax7.plot(df_126_60.index, df_126_60.wind_speed_convert, color='blue', marker='o')
    ax7.plot(df_123_60.index, df_123_60.wind_speed_convert, color='red', marker='o')

    # UKV
    ax7.plot(df_126_ukv.index, df_126_ukv.wind_speed, color='blue', linestyle='--')
    ax7.plot(df_123_ukv.index, df_123_ukv.wind_speed, color='red', linestyle='--')

    ax7.set_ylabel('u (m s$^{-1}$)')

    # plot model

    # wind direction
    # 10 min
    ax8.plot(df_126_10.index, df_126_10.wind_direction_convert, color='blue', alpha=0.3, linewidth=0.5, marker='.')
    ax8.plot(df_123_10.index, df_123_10.wind_direction_convert, color='red', alpha=0.3, linewidth=0.5, marker='.')
    # hour
    ax8.plot(df_126_60.index, df_126_60.wind_direction_convert, color='blue', marker='o')
    ax8.plot(df_123_60.index, df_123_60.wind_direction_convert, color='red', marker='o')
    # UKV
    ax8.plot(df_126_ukv.index, df_126_ukv.wind_direction, color='blue', linestyle='--')
    ax8.plot(df_123_ukv.index, df_123_ukv.wind_direction, color='red', linestyle='--')

    ax8.plot([], [], color='black', linestyle='--', label='UKV at ' + '{0:.0f}'.format(UKV_123_z) + ' m')
    ax8.legend()

    ax8.set_ylabel('Wind Direction ($^{\circ}$)')

    ax1.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))
    ax2.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))
    ax3.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))
    ax4.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))
    ax5.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))
    ax6.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))
    ax7.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))
    ax8.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))
    ax9.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))

    ax1.xaxis.set_major_formatter(DateFormatter('%H'))
    ax2.xaxis.set_major_formatter(DateFormatter('%H'))
    ax3.xaxis.set_major_formatter(DateFormatter('%H'))
    ax4.xaxis.set_major_formatter(DateFormatter('%H'))
    ax5.xaxis.set_major_formatter(DateFormatter('%H'))
    ax6.xaxis.set_major_formatter(DateFormatter('%H'))
    ax7.xaxis.set_major_formatter(DateFormatter('%H'))
    ax8.xaxis.set_major_formatter(DateFormatter('%H'))
    ax9.xaxis.set_major_formatter(DateFormatter('%H'))

    ax8.set_xlabel('Time (h, UTC)')

    ax9.axis('off')

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
