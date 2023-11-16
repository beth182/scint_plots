import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.dates as mdates
import datetime as dt
from matplotlib import cm
import matplotlib as mpl
from scipy import stats

mpl.rcParams.update({'font.size': 13})


def setup_sa_frequency(DOY_dict):
    """

    :param DOY_dict:
    :return:
    """

    assert 2016126 in DOY_dict.keys()
    assert 2016123 in DOY_dict.keys()

    DOY_df_dict = {}

    for DOY in DOY_dict.keys():

        # set up dict
        DOY_df_dict[DOY] = {}

        df_10_min_sa = DOY_dict[DOY]['1min_sa10min'].dropna()
        df_60_min_sa = DOY_dict[DOY]['1min'].dropna()

        # rename cols
        df_10_min_sa = df_10_min_sa.rename(columns={'QH': 'QH_10', 'z_f': 'z_f_10'})
        df_60_min_sa = df_60_min_sa.rename(columns={'QH': 'QH_60', 'z_f': 'z_f_60'})

        # combine into one df
        df = pd.concat([df_10_min_sa, df_60_min_sa], axis=1)

        # format index - setting both days as the same date - for the colour bar on the plot
        # all that matters is hour and minute
        format_index = df.index.strftime('%H:%M')

        index_list = []
        # construct datetime obj for both days with same year day etc. (for colourbar)
        for i in format_index:
            datetime_object = dt.datetime.strptime(i, '%H:%M')
            index_list.append(datetime_object)

        df.index = index_list

        # group times into 10 min grous
        time_grouper = pd.Grouper(freq='10T', closed='left', label='left', offset='1min')
        time_groups = df.groupby(time_grouper)

        start_times = []
        x_vals = []
        y_vals = []
        IQR25_vals = []
        IQR75_vals = []
        mean_fluxs = []

        # interquartile ranges
        for start_time, time_group in time_groups:

            time_group['x_axis_vals'] = (time_group['z_f_10'] - time_group['z_f_60']) / time_group[
                'z_f_60']
            x_axis_vals = time_group['x_axis_vals']
            x_axis_vals = x_axis_vals.dropna()

            # check that all 10 min zf vals in the column are the same
            if len(x_axis_vals) == 0:
                continue
            else:
                assert (x_axis_vals[0] == x_axis_vals).all()

            x_axis_val = x_axis_vals[0]

            time_group['y_axis_vals'] = (time_group['QH_10'] - time_group['QH_60']) / time_group['QH_60']
            y_axis_vals = time_group['y_axis_vals']

            median = y_axis_vals.median()

            IQR_25 = y_axis_vals.quantile(.25)
            IQR_75 = y_axis_vals.quantile(.75)

            mean_flux = np.nanmean(time_group['QH_10'])

            start_times.append(start_time)
            x_vals.append(x_axis_val)
            y_vals.append(median)
            IQR25_vals.append(IQR_25)
            IQR75_vals.append(IQR_75)
            mean_fluxs.append(mean_flux)

        bellow_75_index = np.where(np.asarray(mean_fluxs) < 75)[0]

        DOY_df_dict[DOY]['df'] = df
        DOY_df_dict[DOY]['mean_fluxs'] = mean_fluxs
        DOY_df_dict[DOY]['x_vals'] = x_vals
        DOY_df_dict[DOY]['y_vals'] = y_vals
        DOY_df_dict[DOY]['bellow_75_index'] = bellow_75_index
        DOY_df_dict[DOY]['start_times'] = start_times
        DOY_df_dict[DOY]['IQR25_vals'] = IQR25_vals
        DOY_df_dict[DOY]['IQR75_vals'] = IQR75_vals

    plot_sa_freq(DOY_df_dict)


def plot_sa_freq(DOY_df_dict):
    """

    :return:
    """

    # combine df
    combine_df = pd.concat([DOY_df_dict[2016123]['df'], DOY_df_dict[2016126]['df']], axis=1)

    # plot
    fig, ax = plt.subplots(figsize=(7, 7))

    # identity line
    plt.plot((DOY_df_dict[2016126]['df']['z_f_10'] - DOY_df_dict[2016126]['df']['z_f_60']) / DOY_df_dict[2016126]['df'][
        'z_f_60'],
             (DOY_df_dict[2016126]['df']['z_f_10'] - DOY_df_dict[2016126]['df']['z_f_60']) / DOY_df_dict[2016126]['df'][
                 'z_f_60'],
             color='k', linewidth='0.5')

    plt.axhline(y=0, color='grey', linestyle=':', linewidth=0.5)
    plt.axvline(x=0, color='grey', linestyle=':', linewidth=0.5)

    cmap = cm.get_cmap('rainbow')

    earliest_time = min([DOY_df_dict[2016123]['start_times'][0], DOY_df_dict[2016126]['start_times'][0]])
    latest_time = max([DOY_df_dict[2016123]['start_times'][-1], DOY_df_dict[2016126]['start_times'][-1]])

    bounds = np.linspace(mdates.date2num(earliest_time), mdates.date2num(latest_time),
                         len(DOY_df_dict[2016123]['start_times']) + 1)

    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    smap = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)

    list_of_rgba_126 = smap.to_rgba(mdates.date2num(DOY_df_dict[2016126]['start_times']))
    list_of_rgba_123 = smap.to_rgba(mdates.date2num(DOY_df_dict[2016123]['start_times']))

    # IQR
    for i in range(0, len(DOY_df_dict[2016123]['start_times'])):
        ax.vlines(DOY_df_dict[2016123]['x_vals'][i], DOY_df_dict[2016123]['IQR25_vals'][i],
                  DOY_df_dict[2016123]['IQR75_vals'][i], color=list_of_rgba_123[i], zorder=1)

    for i in range(0, len(DOY_df_dict[2016126]['start_times'])):
        ax.vlines(DOY_df_dict[2016126]['x_vals'][i], DOY_df_dict[2016126]['IQR25_vals'][i],
                  DOY_df_dict[2016126]['IQR75_vals'][i], color=list_of_rgba_126[i], zorder=1)

    # times where QH is larger than threshold value
    # cloudy
    # clear
    ax.scatter(np.asarray(DOY_df_dict[2016126]['x_vals'])[DOY_df_dict[2016126]['bellow_75_index']],
               np.asarray(DOY_df_dict[2016126]['y_vals'])[DOY_df_dict[2016126]['bellow_75_index']],
               facecolors='none', edgecolors='k', marker='$\u25cf$', zorder=2, s=300,  alpha=0.7)

    ax.scatter(np.asarray(DOY_df_dict[2016123]['x_vals'])[DOY_df_dict[2016123]['bellow_75_index']],
               np.asarray(DOY_df_dict[2016123]['y_vals'])[DOY_df_dict[2016123]['bellow_75_index']],
               facecolors='none', edgecolors='k', marker='$\u25cf$', zorder=2, s=300, alpha=0.7,
               label='$\overline{Q_{H,LAS}^{10 min}}$ < 75 $W$ $m^{-2}$')


    # markers
    # cloudy
    s = ax.scatter(DOY_df_dict[2016123]['x_vals'], DOY_df_dict[2016123]['y_vals'],
                   c=mdates.date2num(DOY_df_dict[2016123]['start_times']), marker='$\u25cf$', cmap=cmap, norm=norm,
                   edgecolor='k', label='IOP-1', s=80, zorder=3)

    # clear
    s2 = ax.scatter(DOY_df_dict[2016126]['x_vals'], DOY_df_dict[2016126]['y_vals'],
                    c=mdates.date2num(DOY_df_dict[2016126]['start_times']), marker='$\u25cb$', cmap=cmap, norm=norm,
                    label='IOP-2', zorder=5, s=80)

    # use white scatter marks - so lines don't appear through marker
    # facecolor didn't work...
    white_block = ax.scatter(DOY_df_dict[2016126]['x_vals'], DOY_df_dict[2016126]['y_vals'],
                             c='white', marker="$\u25cf$", zorder=4, s=70)

    x_vals_both = DOY_df_dict[2016123]['x_vals'] + DOY_df_dict[2016126]['x_vals']
    y_vals_both = DOY_df_dict[2016123]['y_vals'] + DOY_df_dict[2016126]['y_vals']
    gradient, intercept, r_value, p_value, std_err = stats.linregress(x_vals_both, y_vals_both)

    string_for_label = 'm = ' + '%s' % float('{0:.5f}'.format(gradient)) + '\n c = ' + '%s' % float(
        '{0:.5f}'.format(intercept))
    mn = np.min(x_vals_both)
    mx = np.max(x_vals_both)
    x1 = np.linspace(mn, mx, 500)
    y1 = gradient * x1 + intercept
    plt.plot(x1, y1, '--r', label=string_for_label)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)

    cbar = fig.colorbar(mappable=s2, cax=cax, orientation="vertical")

    cbar.set_ticks(mdates.date2num(combine_df.index[np.where(combine_df.index.minute == 0)]))

    cbar.ax.set_yticklabels(
        [mdates.num2date(i).strftime('%H') for i in cbar.get_ticks()])  # set ticks of your format
    cbar.set_label('Time (h, UTC)')

    ax.set_ylabel('($Q_{H,LAS}^{10min}$ - $Q_{H,LAS}^{hour}$) / $Q_{H,LAS}^{hour}$')
    ax.set_xlabel('($z_{f}^{10min}$ - $z_{f}^{hour}$) / $z_{f}^{hour}$')

    leg = ax.legend(frameon=False, fontsize='medium')

    t1, t2, t3, t4 = leg.get_texts()
    # here we create the distinct instance
    t1._fontproperties = t2._fontproperties.copy()
    t1.set_size('small')

    # save plot
    plt.savefig('./' + 'sa_frequency.png', bbox_inches='tight', dpi=300)
    print('end')
