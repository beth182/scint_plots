# imports
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy as np
from matplotlib import gridspec
import pandas as pd
import datetime as dt
import matplotlib as mpl

mpl.rcParams.update({'font.size': 15})


def variation_in_grids(model_df, model_site_dict):
    """
    Defines thickness of line in detailed time series by calculating the differences between model grids
    :return:
    """

    max_vals = []
    min_vals = []
    n_grids = []

    times_list = model_df.index

    for i, time in enumerate(times_list):

        time_string = time.strftime("%y%m%d%H")

        try:
            grid_list = model_site_dict[time_string]
        except KeyError:
            grid_list = []

        n_model_grids = len(grid_list)

        vals_list = []

        for grid_string in grid_list:
            grid = int(grid_string)

            val = model_df[grid][i]
            vals_list.append(val)

        if vals_list == []:
            max_val = np.nan
            min_val = np.nan
        else:
            max_val = max(vals_list)
            min_val = min(vals_list)

        max_vals.append(max_val)
        min_vals.append(min_val)

        n_grids.append(n_model_grids)

    return max_vals, min_vals, n_grids


def detailed_time_series(obs_df,
                         ukv_df,
                         model_site_dict,
                         variable='H',
                         BL_H_z=0,
                         number_grids_axes=False,
                         ukv_df_all_grids=False,
                         model_site_dict_all=False):
    """

    :return:
    """

    ukv_df = ukv_df.dropna()

    if variable == 'H':
        label_string = '$Q_{H}$ (W m$^{-2})$'
    elif variable == 'kdown':
        label_string = '$K_{\downarrow}$ (W m$^{-2}$)'
    else:
        raise ValueError('variable chosen not an option')

    mpl.rcParams.update({'font.size': 22})
    plt.close('all')

    if variable != 'H':
        number_grids_axes = False

    if number_grids_axes == True:
        fig = plt.figure(figsize=(10, 10))
        spec = gridspec.GridSpec(ncols=1, nrows=2,
                                 height_ratios=[4, 1])
    else:
        fig = plt.figure(figsize=(10, 8.5))
        spec = gridspec.GridSpec(ncols=1, nrows=1)

    ax1 = fig.add_subplot(spec[0])

    # obs_df = obs_df.dropna()

    if variable == 'H':
        # five_min = obs_df.resample('5T', closed='right', label='right').mean()
        # ten_min = obs_df.resample('10T', closed='right', label='right').mean()
        # sixty_min = obs_df.resample('60T', closed='right', label='right').mean()

        minute_match = 0

    else:

        # # as-is
        # # '''
        # five_min = obs_df.resample('5T', closed='right', label='right').mean()
        # ten_min = obs_df.resample('10T', closed='right', label='right').mean()
        # sixty_min = obs_df.resample('60T', closed='right', label='right').mean()
        #
        # # if variable == 'kdown':
        # #     sixty_min.index = sixty_min.index - dt.timedelta(minutes=45)
        # #     ten_min.index = ten_min.index + dt.timedelta(minutes=5)
        # #
        # #     minute_match = 15
        # # else:
        # #     minute_match = 0

        minute_match = 0

        # '''
        # OR
        # shifted averages
        '''
        five_min = obs_df.resample('5T', closed='right', label='right').mean()
        ten_min = obs_df.resample('10T', closed='right', label='right', offset='5T').mean()
        sixty_min = obs_df.resample('60T', closed='right', label='right', offset = '15T').mean()

        minute_match = 15

        '''

    hour_1min = obs_df['obs_1'][np.where([i.minute == minute_match for i in obs_df.index])[0]]
    hour_5min = obs_df['obs_5'][np.where([i.minute == minute_match for i in obs_df.index])[0]]
    hour_10min = obs_df['obs_10'][np.where([i.minute == minute_match for i in obs_df.index])[0]]
    hour_60min = obs_df['obs_60'][np.where([i.minute == minute_match for i in obs_df.index])[0]]

    # hour_1min = obs_df[df_col][np.where([i.minute == minute_match for i in obs_df.index])[0]]
    # hour_5min = five_min[df_col][np.where([i.minute == minute_match for i in five_min.index])[0]]
    # hour_10min = ten_min[df_col][np.where([i.minute == minute_match for i in ten_min.index])[0]]
    # hour_60min = sixty_min[df_col][np.where([i.minute == minute_match for i in sixty_min.index])[0]]

    # if variable == 'kdown':
    #     if type(ukv_df_all_grids) == pd.core.frame.DataFrame:
    #         max_grid_vals_all, min_grid_vals_all, n_grids_all = variation_in_grids(ukv_df_all_grids,
    #                                                                                model_site_dict_all)
    #
    #         ax1.fill_between(ukv_df_all_grids.index, max_grid_vals_all, min_grid_vals_all,
    #                          color='paleturquoise',
    #                          alpha=0.6, label='UKV grid-box range: 42 grid-boxes')
    #     else:
    #         pass

    max_grid_vals, min_grid_vals, n_grids = variation_in_grids(ukv_df, model_site_dict)

    # ax1.fill_between(ukv_df.index, max_grid_vals, min_grid_vals, color='pink', alpha=0.8, label='UKV grid-box range in SA analysis')
    ax1.fill_between(ukv_df.index, max_grid_vals, min_grid_vals, color='pink', alpha=0.8, label='UKV grid-box range in $SA_{LAS}$')

    # ax1.plot(ukv_df.index, ukv_df['WAverage'], label='UKV grid-box average with LAS-SA weighting @ surface', color='red', marker='.')

    ax1.plot(ukv_df.index, ukv_df['WAverage'], label='UKV$_{surf}$: $SA_{LAS}$', color='red', marker='.')

    if variable == 'kdown':
        grid_box_letter = 'D'  # where KSSW is
    if variable == 'H':
        grid_box_letter = 'A'  # where the centre coord of the path is



    # ax1.plot(ukv_df.index, ukv_df[13], label='UKV @ surface: grid-box ' + grid_box_letter, color='green', marker='.')
    ax1.plot(ukv_df.index, ukv_df[13], label='UKV$_{surf}$: grid-box ' + grid_box_letter, color='green', marker='.')

    # if I am including the BL_H grid
    try:
        # ukv_level = ax1.plot(ukv_df.index, ukv_df['BL_H'], label='UKV @ ' + str(int(BL_H_z)) + ' m agl: grid-box ' + grid_box_letter, color='blue', marker='.')

        ukv_level = ax1.plot(ukv_df.index, ukv_df['BL_H'], label='UKV$_{level}$ @ ' + str(int(BL_H_z)) + ' m agl: grid-box ' + grid_box_letter, color='blue', marker='.')

    except KeyError:
        pass

    obs_all = ax1.plot(obs_df.index, obs_df['obs_1'], linestyle='None', marker='.', color='grey', alpha=0.5,
             label="1 min obs")

    obs_1 = ax1.plot(hour_1min.index, hour_1min.values, linestyle='None', marker='o', color='k', markersize=8,
                     label="1 min obs on hour")

    obs_5 = ax1.plot(hour_5min.index, hour_5min.values, linestyle='None', marker='o', color='green', markersize=8,
                     label="5 min obs on hour")

    obs_10 = ax1.plot(hour_10min.index, hour_10min.values, linestyle='None', marker='^', color='red', markersize=8,
                      label="10 min obs on hour")

    obs_60 = ax1.plot(hour_60min.index, hour_60min.values, linestyle='None', marker='x', color='purple', markersize=8,
                      label="60 min obs")

    plt.grid(False)

    ax1.set_ylabel(label_string)

    if variable == 'kdown':
        ax1.set_xlim([ukv_df.index[0] - dt.timedelta(minutes=30), ukv_df.index[-1]])
        ax1.set_ylim(0, 1000)
    else:
        ax1.set_xlim([ukv_df.index[0] - dt.timedelta(minutes=15), ukv_df.index[-1] + dt.timedelta(minutes=15)])
        ax1.set_ylim(0, 600)

    # get handles and labels
    handles, labels = plt.gcf().get_axes()[0].get_legend_handles_labels()

    # specify order of items in legend
    if variable == 'H':
        order = [0, 1, 2, 8, 3, 4, 5, 6, 7]

    elif variable == 'kdown':
        if type(ukv_df_all_grids) == pd.core.frame.DataFrame:
            order = [0, 1, 2, 7, 8, 3, 4, 5, 6]
        else:
            order = [0, 1, 7, 2, 3, 4, 5, 6]

    # add legend to plot
    # ax1.legend([handles[idx] for idx in order], [labels[idx] for idx in order], loc='center left', bbox_to_anchor=(1, 0.5))


    # legend for obs on panel (a) - kdown cloudy day
    if variable == 'kdown':
        if obs_df.index[0].strftime('%Y%j') == '2016123':

            ax1.legend([handles[idx] for idx in order][3:], [labels[idx] for idx in order][3:], fontsize=15)  # [3:] just obs handles



    # legend for model kdown on panel (b) - kdown clear day
    if variable == 'kdown':
        if obs_df.index[0].strftime('%Y%j') == '2016126':

            ax1.legend([handles[idx] for idx in order][:3], [labels[idx] for idx in order][:3], fontsize=15)  # [:3] just model handles

            # ax1.legend(fontsize=15, loc=(0.16, 0.05))

    # add legend if H cloudy day
    if variable == 'H':
        if obs_df.index[0].strftime('%Y%j') == '2016123':


            ax1.legend([handles[idx] for idx in order][:-5], [labels[idx] for idx in order][:-5],fontsize=15)  # [:-5] just model handles

            # # Fix legend
            # hand, labl = ax1.get_legend_handles_labels()
            # handout = []
            # lablout = []
            # for h, l in zip(hand, labl):
            #     if l == 'Centre grid-box UKV-flux @ ' + str(BL_H_z) + ' m':
            #         lablout.append(l)
            #         handout.append(h)
            # ax1.legend(handout, lablout, fontsize=15)


    if number_grids_axes == True:

        ax1.set_xticks([])

        ax2 = fig.add_subplot(spec[1])

        ax2.set_xlim([ukv_df.index[0] - dt.timedelta(minutes=15), ukv_df.index[-1] + dt.timedelta(minutes=15)])

        ax2.plot(ukv_df.index, n_grids, marker='x', linestyle='None', color='k')
        ax2.set_xlabel('Time (h, UTC)')
        ax2.xaxis.set_major_formatter(DateFormatter('%H'))
        ax2.set_ylabel("# of grids in SA")
        # plt.gcf().autofmt_xdate()

    else:
        ax1.xaxis.set_major_formatter(DateFormatter('%H'))
        ax1.set_xlabel('Time (h, UTC)')
        # plt.gcf().autofmt_xdate()

    if variable == 'kdown':
        from matplotlib.ticker import MaxNLocator
        ax1.yaxis.set_major_locator(MaxNLocator(prune='upper'))

    plt.tight_layout()

    plt.savefig('./' + obs_df.index[0].strftime('%Y%j') + '_' + str(variable) + '_detail_time_series.png',
                bbox_inches='tight', dpi=300)
    print('Saved here:' + './' + obs_df.index[0].strftime('%Y%j') + '_' + str(variable) + '_detail_time_series.png')
