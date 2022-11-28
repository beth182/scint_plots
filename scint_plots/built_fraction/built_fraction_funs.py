import os.path
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable

mpl.rcParams.update({'font.size': 15})


def add_lc_to_df(df):
    """
    Read landcover csv - with fractions in each timesteps SA - and combine with with the df of obs variables.
    :param df:
    :return:
    """

    # define csv path based on DOY
    # ToDo: move csv to this location - in the same dir
    # ToDo: check every instance of this csv - to make sure the move doesn't effect something else
    lc_csv_path = 'C:/Users/beths/Desktop/LANDING/mask_tests/' + df.index[0].strftime('%j') + '_10_mins.csv'

    # make sure file exists
    assert os.path.isfile(lc_csv_path)

    # read csv
    lc_df = pd.read_csv(lc_csv_path)
    lc_df.index = lc_df['Unnamed: 0']
    lc_df = lc_df.drop('Unnamed: 0', 1)

    try:
        lc_df.index = pd.to_datetime(lc_df.index, format='%d/%m/%Y %H:%M')
    except ValueError:
        lc_df.index = pd.to_datetime(lc_df.index, format='%Y-%m-%d %H:%M:%S')

    minutes = 10
    freq_string = str(minutes) + 'Min'

    group_times_lc = lc_df.groupby(pd.Grouper(freq=freq_string, label='left')).first()

    lc_outputs_df = pd.DataFrame({'Building': [], 'Impervious': [], 'Water': [], 'Grass': [],
                                  'Deciduous': [], 'Evergreen': [], 'Shrub': []})

    for i, row in group_times_lc.iterrows():
        time = i

        # time_array = np.array([time + dt.timedelta(minutes=i) for i in range(minutes)])
        time_array = np.array(
            [(time + dt.timedelta(minutes=1) - dt.timedelta(minutes=minutes)) + dt.timedelta(minutes=i) for i in
             range(minutes)])

        Building = lc_df['Building'][np.where(lc_df.index == time)[0]]
        Impervious = lc_df['Impervious'][np.where(lc_df.index == time)[0]]
        Water = lc_df['Water'][np.where(lc_df.index == time)[0]]
        Grass = lc_df['Grass'][np.where(lc_df.index == time)[0]]
        Deciduous = lc_df['Deciduous'][np.where(lc_df.index == time)[0]]
        Evergreen = lc_df['Evergreen'][np.where(lc_df.index == time)[0]]
        Shrub = lc_df['Shrub'][np.where(lc_df.index == time)[0]]

        df_dict = {'time': time_array}

        lc_types = ['Building', 'Impervious', 'Water', 'Grass', 'Deciduous', 'Evergreen', 'Shrub']

        for lc_type in lc_types:

            lc_type_series = lc_df[lc_type][np.where(lc_df.index == time)[0]]

            if len(lc_type_series) == 0:
                nan_series = pd.Series([np.nan])
                lc_type_series = lc_type_series.append(nan_series)
            else:
                if type(lc_type_series.values[0]) == str:
                    lc_type_series.values[0] = 0

            try:
                df_dict[lc_type] = np.ones(len(time_array)) * lc_type_series.values[0]
            except:
                print('end')

        period_df = pd.DataFrame(df_dict)
        period_df = period_df.set_index('time')

        lc_outputs_df = lc_outputs_df.append(period_df)

    lc_outputs_df['sum'] = lc_outputs_df.sum(axis=1)
    lc_outputs_df['Urban'] = lc_outputs_df['Building'] + lc_outputs_df['Impervious']

    df_combine = df.merge(lc_outputs_df, how='inner', left_index=True, right_index=True)

    return df_combine


def plot_built_fraction(DOY_dict):
    """

    :return:
    """

    assert 2016126 in DOY_dict.keys() and 2016123 in DOY_dict.keys()

    output_dict = {}

    for DOY in DOY_dict.keys():

        # set up keys in dict
        output_dict[DOY] = {}

        # read model keys
        UKV_kdown_df = DOY_dict[DOY]['UKV_kdown']
        UKV_QH_df = DOY_dict[DOY]['UKV_QH']
        ukv_lc_df = DOY_dict[DOY]['ukv_lc']

        # convert ukv lc df to datetime index
        ukv_lc_df.index = pd.to_datetime(ukv_lc_df.index, format='%y%m%d%H')
        # add urban column to ukv lc df
        ukv_lc_df['Urban'] = ukv_lc_df['roof'] + ukv_lc_df['canyon']

        # push back kdown (15 min average time starting) by 15 mins to match QH time (instantaneous on the hour)
        UKV_kdown_df.index = UKV_kdown_df.index - dt.timedelta(minutes=15)

        # combine UKV QH, kdown and lc
        UKV_df = pd.concat([pd.Series.to_frame(UKV_QH_df.WAverage).rename(columns={'WAverage': 'QH'}),
                            pd.Series.to_frame(UKV_kdown_df.WAverage).rename(columns={'WAverage': 'kdown'}),
                            ukv_lc_df], axis=1)

        # read obs key
        obs_df = DOY_dict[DOY]['obs']

        # normalise obs QH by kdown
        obs_df['QH_norm'] = obs_df.QH / obs_df.kdown

        # normalise model QH by kdown
        UKV_df['QH_norm'] = UKV_df.QH / UKV_df.kdown

        # group 1-min obs together to be able to do stats (IQR mean median etc)
        time_grouper = pd.Grouper(freq='10T', closed='left', label='left', offset='1min')
        time_groups = obs_df.groupby(time_grouper)

        start_times = []
        x_vals = []
        y_vals = []
        IQR25_vals = []
        IQR75_vals = []
        means_kdown = []

        for start_time, time_group in time_groups:

            time_group['x_axis_vals'] = time_group['Urban']
            x_axis_vals = time_group['x_axis_vals']

            # check that all 10 min fraction vals in the column are the same
            if len(x_axis_vals) == 0:
                continue
            elif x_axis_vals.isnull().all():
                continue
            else:
                assert (x_axis_vals[0] == x_axis_vals).all()

            x_axis_val = x_axis_vals[0]

            time_group['y_axis_vals'] = time_group['QH_norm']
            y_axis_vals = time_group['y_axis_vals']

            median = y_axis_vals.median()

            IQR_25 = y_axis_vals.quantile(.25)
            IQR_75 = y_axis_vals.quantile(.75)

            mean_kdown = np.nanmean(time_group['kdown'])

            start_times.append(start_time)
            x_vals.append(x_axis_val)
            y_vals.append(median)
            IQR25_vals.append(IQR_25)
            IQR75_vals.append(IQR_75)
            means_kdown.append(mean_kdown)

        # restrict the times to the middle of the day (10 to 14)
        start_dt = dt.datetime(obs_df.index[0].year, obs_df.index[0].month, obs_df.index[0].day, 10)
        end_dt = dt.datetime(obs_df.index[0].year, obs_df.index[0].month, obs_df.index[0].day, 14)
        # obs
        start_times = np.asarray(start_times)
        where_index = np.where((start_times >= start_dt) & (start_times <= end_dt))[0]

        # model
        where_index_mod = np.where((UKV_df.index.hour >= start_dt.hour) & (UKV_df.index.hour <= end_dt.hour))[0]
        mod_select = UKV_df.iloc[where_index_mod]

        start_times_select = np.asarray(start_times)[where_index]

        x_vals_select = np.asarray(x_vals)[where_index]
        y_vals_select = np.asarray(y_vals)[where_index]

        IQR25_vals_select = np.asarray(IQR25_vals)[where_index]

        IQR75_vals_select = np.asarray(IQR75_vals)[where_index]

        mean_kdown_select = np.asarray(means_kdown)[where_index]

        # save outputs to dict
        output_dict[DOY]['mean_kdown_select'] = mean_kdown_select
        output_dict[DOY]['mod_select'] = mod_select
        output_dict[DOY]['start_times_select'] = start_times_select
        output_dict[DOY]['x_vals_select'] = x_vals_select
        output_dict[DOY]['IQR25_vals_select'] = IQR25_vals_select
        output_dict[DOY]['IQR75_vals_select'] = IQR75_vals_select
        output_dict[DOY]['obs_df'] = obs_df
        output_dict[DOY]['y_vals_select'] = y_vals_select

    plot_function_built_fraction(output_dict)


def plot_function_built_fraction(output_dict):
    """
    Function to produce built fraction plot given inputs from plot_built_fraction function.
    :return:
    """

    fig, ax = plt.subplots(figsize=(7, 7))
    cmap = cm.get_cmap('rainbow')

    smallest_kdown = min(min(output_dict[2016123]['mean_kdown_select']), min(output_dict[2016126]['mean_kdown_select']),
                         output_dict[2016123]['mod_select'].kdown.min(), output_dict[2016126]['mod_select'].kdown.min())

    largest_kdown = max(max(output_dict[2016123]['mean_kdown_select']), max(output_dict[2016126]['mean_kdown_select']),
                        output_dict[2016123]['mod_select'].kdown.max(), output_dict[2016126]['mod_select'].kdown.max())

    bounds = np.linspace(smallest_kdown, largest_kdown, len(output_dict[2016123]['start_times_select']) + 1)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    smap = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)

    for DOY in output_dict.keys():

        mean_kdown_select = output_dict[DOY]['mean_kdown_select']
        x_vals_select = output_dict[DOY]['x_vals_select']
        IQR25_vals_select = output_dict[DOY]['IQR25_vals_select']
        IQR75_vals_select = output_dict[DOY]['IQR75_vals_select']
        obs_df = output_dict[DOY]['obs_df']
        y_vals_select = output_dict[DOY]['y_vals_select']
        mod_select = output_dict[DOY]['mod_select']

        list_of_rgba = smap.to_rgba(mean_kdown_select)

        for i in range(0, len(mean_kdown_select)):
            ax.vlines(x_vals_select[i], IQR25_vals_select[i], IQR75_vals_select[i], color=list_of_rgba[i], zorder=1)

        if obs_df.index[0].strftime('%j') == '126':

            # use white scatter marks - so lines don't appear through marker
            # facecolor didn't work...
            white_block = ax.scatter(x_vals_select, y_vals_select,
                                     c='white', marker="$\u25B2$", s=80, zorder=2)

            s = ax.scatter(x_vals_select, y_vals_select,
                           c=mean_kdown_select, marker="$\u25B3$", cmap=cmap, norm=norm, label='Clear Obs', s=80,
                           zorder=3)

            white_block_UKV = ax.scatter(mod_select.Urban * 100, mod_select.QH / mod_select.kdown,
                                         c='white', marker="$\u25A0$", s=80, zorder=2)

            ax.scatter(mod_select.Urban * 100, mod_select.QH / mod_select.kdown,
                       c=mod_select.kdown, marker="$\u25A1$", cmap=cmap, norm=norm, label='Clear UKV', s=80,
                       zorder=3)


        else:
            assert obs_df.index[0].strftime('%j') == '123'

            s = ax.scatter(x_vals_select, y_vals_select, c=mean_kdown_select, marker='^', cmap=cmap, norm=norm,
                           edgecolor='k', label='Cloudy Obs', s=80)

            ax.scatter(mod_select.Urban * 100, mod_select.QH / mod_select.kdown, c=mod_select.kdown, marker='s',
                       cmap=cmap, norm=norm, edgecolor='k', label='Cloudy UKV', s=80)

    plt.legend()

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cbar = fig.colorbar(mappable=s, cax=cax, orientation="vertical", format='%.0f')
    cax.set_ylabel('$K_{\downarrow}$ (W m$^{-2}$)', rotation=270, labelpad=20)

    ax.set_xlabel('Built Fraction')
    ax.set_ylabel('$Q_{H}$ / $K_{\downarrow}$')

    # save fig
    plt.savefig('./built_fraction.png', bbox_inches='tight', dpi=300)
