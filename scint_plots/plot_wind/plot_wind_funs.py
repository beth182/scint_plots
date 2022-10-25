from matplotlib import gridspec
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.dates import DateFormatter
import datetime as dt
import matplotlib as mpl

mpl.rcParams.update({'font.size': 15})

from scint_fp.functions import wx_u_v_components


def plot_wind(df_dict):
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

    df_126_10 = df_126_10.dropna()
    df_126_60 = df_126_60.dropna()
    df_123_10 = df_123_10.dropna()
    df_123_60 = df_123_60.dropna()

    # model stuff
    UKV_126 = df_dict[2016126]['UKV_wind']
    UKV_123 = df_dict[2016123]['UKV_wind']

    UKV_126_z = df_dict[2016126]['UKV_height']
    UKV_123_z = df_dict[2016123]['UKV_height']

    assert UKV_123_z == UKV_126_z

    # construct datetime obj for both days with same year day etc. (for colourbar)
    format_index_UKV_123 = UKV_123.index.strftime('%H:%M')
    index_list_123_ukv = []
    for i in format_index_UKV_123:
        datetime_object = dt.datetime.strptime(i, '%H:%M')
        index_list_123_ukv.append(datetime_object)
    UKV_123.index = index_list_123_ukv

    format_index_UKV_126 = UKV_126.index.strftime('%H:%M')
    index_list_126_ukv = []
    for i in format_index_UKV_126:
        datetime_object = dt.datetime.strptime(i, '%H:%M')
        index_list_126_ukv.append(datetime_object)
    UKV_126.index = index_list_126_ukv

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

    # convert wind speed and direction to u & v components, to average, then convert the averages back
    component_df_123_10 = wx_u_v_components.ws_wd_to_u_v(df_123_10['wind_speed_adj'],
                                                         df_123_10['wind_direction_corrected'])
    component_df_123_60 = wx_u_v_components.ws_wd_to_u_v(df_123_60['wind_speed_adj'],
                                                         df_123_60['wind_direction_corrected'])
    component_df_126_10 = wx_u_v_components.ws_wd_to_u_v(df_126_10['wind_speed_adj'],
                                                         df_126_10['wind_direction_corrected'])
    component_df_126_60 = wx_u_v_components.ws_wd_to_u_v(df_126_60['wind_speed_adj'],
                                                         df_126_60['wind_direction_corrected'])

    # average df
    # 60 mins from hourly SA
    df_123_comp_60 = component_df_123_60.resample('60T', closed='right', label='right').mean()
    df_126_comp_60 = component_df_126_60.resample('60T', closed='right', label='right').mean()

    # 10 min averages
    df_126_comp_5 = component_df_126_10.resample('5T', closed='right', label='right').mean()
    df_123_comp_5 = component_df_123_10.resample('5T', closed='right', label='right').mean()
    df_126_comp_10 = component_df_126_10.resample('10T', closed='right', label='right').mean()
    df_123_comp_10 = component_df_123_10.resample('10T', closed='right', label='right').mean()

    # convert back to ws and direction
    av_123_60 = wx_u_v_components.u_v_to_ws_wd(df_123_comp_60['u_component'], df_123_comp_60['v_component'])
    av_126_60 = wx_u_v_components.u_v_to_ws_wd(df_126_comp_60['u_component'], df_126_comp_60['v_component'])

    av_123_5 = wx_u_v_components.u_v_to_ws_wd(df_123_comp_5['u_component'], df_123_comp_5['v_component'])
    av_126_5 = wx_u_v_components.u_v_to_ws_wd(df_126_comp_5['u_component'], df_126_comp_5['v_component'])

    av_126_10 = wx_u_v_components.u_v_to_ws_wd(df_126_comp_10['u_component'], df_126_comp_10['v_component'])
    av_123_10 = wx_u_v_components.u_v_to_ws_wd(df_123_comp_10['u_component'], df_123_comp_10['v_component'])

    # plot

    fig = plt.figure(figsize=(15, 10))

    spec = gridspec.GridSpec(ncols=2, nrows=2)

    ax1 = plt.subplot(spec[0])
    ax2 = plt.subplot(spec[1])
    ax3 = plt.subplot(spec[2])
    ax4 = plt.subplot(spec[3])

    ax1.title.set_text('Cloudy')
    ax2.title.set_text('Clear')

    # set x lims
    min_time = min(df_126_10.index.min(), df_126_60.index.min(), df_123_10.index.min(), df_123_60.index.min())
    max_time = max(df_126_10.index.max(), df_126_60.index.max(), df_123_10.index.max(), df_123_60.index.max())

    # plot wind speed
    ax1.set_ylabel('Wind Speed (m s$^{-1}$)')
    # cloudy
    ax1.scatter(df_123_10.index, df_123_10['wind_speed_adj'], marker='.', alpha=0.15, color='blue')
    ax1.scatter(av_123_5.index, av_123_5['wind_speed_convert'], marker='o', alpha=0.4, color='green')
    ax1.scatter(av_123_10.index, av_123_10['wind_speed_convert'], marker='^', alpha=0.7, color='red')
    ax1.scatter(av_123_60.index, av_123_60['wind_speed_convert'], marker='x', alpha=1.0, color='purple', s=50)
    # model
    ax1.plot(UKV_123.index, UKV_123.wind_speed, color='blue')

    # clear
    ax2.scatter(df_126_10.index, df_126_10['wind_speed_adj'], marker='.', alpha=0.15, color='blue')
    ax2.scatter(av_126_5.index, av_126_5['wind_speed_convert'], marker='o', alpha=0.4, color='green')
    ax2.scatter(av_126_10.index, av_126_10['wind_speed_convert'], marker='^', alpha=0.7, color='red')
    ax2.scatter(av_126_60.index, av_126_60['wind_speed_convert'], marker='x', alpha=1.0, color='purple', s=50)
    # model
    ax2.plot(UKV_126.index, UKV_126.wind_speed, color='blue')

    ax1.set_xticks([])
    ax2.set_xticks([])
    ax2.set_yticks([])

    ax1.set_ylim(0, 14)
    ax2.set_ylim(0, 14)

    # plot wind direction
    ax3.set_ylabel('Wind Direction ($^{\circ}$)')
    # cloudy
    ax3.scatter(df_123_10.index, df_123_10['wind_direction_corrected'], marker='.', alpha=0.15, color='blue',
                label='1 min')
    ax3.scatter(av_123_5.index, av_123_5['wind_direction_convert'], marker='o', alpha=0.4, color='green', label='5 min')
    ax3.scatter(av_123_10.index, av_123_10['wind_direction_convert'], marker='^', alpha=0.7, color='red',
                label='10 min')
    ax3.scatter(av_123_60.index, av_123_60['wind_direction_convert'], marker='x', alpha=1.0, color='purple', s=50,
                label='60 min')
    # model
    ax3.plot(UKV_123.index, UKV_123.wind_direction, color='blue', label='UKV at ' + '{0:.0f}'.format(UKV_123_z) + ' m')

    # clear
    ax4.scatter(df_126_10.index, df_126_10['wind_direction_corrected'], marker='.', alpha=0.15, color='blue')
    ax4.scatter(av_126_5.index, av_126_5['wind_direction_convert'], marker='o', alpha=0.4, color='green')
    ax4.scatter(av_126_10.index, av_126_10['wind_direction_convert'], marker='^', alpha=0.7, color='red')
    ax4.scatter(av_126_60.index, av_126_60['wind_direction_convert'], marker='x', alpha=1.0, color='purple', s=50)
    # model
    ax4.plot(UKV_126.index, UKV_126.wind_direction, color='blue')

    ax4.set_yticks([])

    ax3.set_ylim(0, 360)
    ax4.set_ylim(0, 360)

    plt.subplots_adjust(wspace=0, hspace=0)

    ax3.yaxis.set_major_locator(MaxNLocator(prune='upper'))
    fig.text(0.5, 0.055, 'Time (h, UTC)', ha='center')
    ax3.xaxis.set_major_formatter(DateFormatter('%H'))
    ax4.xaxis.set_major_formatter(DateFormatter('%H'))

    ax1.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))
    ax2.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))
    ax3.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))
    ax4.set_xlim(min_time - dt.timedelta(minutes=5), max_time + dt.timedelta(minutes=5))

    ax3.legend(frameon=False)

    plt.savefig('./' + 'wind_vars.png', bbox_inches='tight', dpi=300)
    print('end')
