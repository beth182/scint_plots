import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches

from scint_flux import look_up


def plot_season_one_panel(season_dict, season_dict_UKV, save_path, average, variable='QH', count_threshold=5):
    """

    :return:
    """

    colour_dict = {'BCT_IMU': 'red', 'SCT_SWT': 'mediumorchid', 'IMU_BTT': 'green', 'BTT_BCT': 'blue'}

    # hard code ylim
    if variable == 'QH':
        ylim = 425
    else:
        assert variable == 'kdown'
        ylim = 900

    all_seasons = ['DJF', 'MAM', 'JJA', 'SON']

    linestyle_dict = {'median': 'o', 'mean': 's', 'UKV_median': ':', 'UKV_mean': '--'}

    for season in all_seasons:

        if season in season_dict.keys():

            fig, ax = plt.subplots(figsize=(4, 4))

            df_season = season_dict[season]
            df_season_UKV = season_dict_UKV[season]

            max_obs_hour = max(df_season.index.hour)
            min_obs_hour = min(df_season.index.hour)

            df_season_UKV['hour'] = df_season_UKV.index.hour

            df_season_UKV = df_season_UKV[
                (df_season_UKV.hour <= max_obs_hour) & (df_season_UKV.hour >= min_obs_hour)].drop(columns=['hour'])

            ax.set_title(season)

            IQR_path_dict_UKV = IQR(df_season_UKV)
            IQR_path_dict = IQR(df_season)

            for path in IQR_path_dict:
                path_num_str = path.split('_')[-1]

                IQR_dict = IQR_path_dict[path]

                if variable == 'QH':
                    IQR_dict_UKV = IQR_path_dict_UKV['BL_H_' + path_num_str]
                else:
                    IQR_dict_UKV = IQR_path_dict_UKV[path]

                pair_id = look_up.scint_path_numbers[int(path.split('_')[-1])]

                if variable == 'kdown':
                    if pair_id == 'BCT_IMU':
                        pass
                    else:

                        # points above threshold
                        ax.scatter(IQR_dict['mean'][IQR_dict['count'] >= count_threshold].index,
                                   IQR_dict['mean'][IQR_dict['count'] >= count_threshold],
                                   color=colour_dict[pair_id], marker=linestyle_dict['mean'], s=15, edgecolor='k',
                                   zorder=3)
                        ax.scatter(IQR_dict['median'][IQR_dict['count'] >= count_threshold].index,
                                   IQR_dict['median'][IQR_dict['count'] >= count_threshold],
                                   color=colour_dict[pair_id], marker=linestyle_dict['median'], s=20, edgecolor='k',
                                   zorder=3)

                        # transparent markers for points bellow threshold
                        ax.scatter(IQR_dict['mean'][IQR_dict['count'] < count_threshold].index,
                                   IQR_dict['mean'][IQR_dict['count'] < count_threshold],
                                   marker=linestyle_dict['mean'], s=15, edgecolor=colour_dict[pair_id], zorder=4,
                                   facecolors='None')
                        ax.scatter(IQR_dict['median'][IQR_dict['count'] < count_threshold].index,
                                   IQR_dict['median'][IQR_dict['count'] < count_threshold],
                                   marker=linestyle_dict['median'], s=20, edgecolor=colour_dict[pair_id], zorder=4,
                                   facecolors='None')

                        # for col in IQR_dict['25']:
                        #     if col not in IQR_dict['mean'][IQR_dict['count'] >= count_threshold].index:
                        #         IQR_dict['25'] = IQR_dict['25'].drop(columns=[col])
                        #         IQR_dict['75'] = IQR_dict['75'].drop(columns=[col])

                        ax.fill_between(IQR_dict['25'].columns, IQR_dict['25'].iloc[0], IQR_dict['75'].iloc[0],
                                        color=colour_dict[pair_id], alpha=0.2, zorder=1)

                else:

                    # points above threshold
                    ax.scatter(IQR_dict['mean'][IQR_dict['count'] >= count_threshold].index,
                               IQR_dict['mean'][IQR_dict['count'] >= count_threshold],
                               color=colour_dict[pair_id], marker=linestyle_dict['mean'], s=15, edgecolor='k', zorder=3)
                    ax.scatter(IQR_dict['median'][IQR_dict['count'] >= count_threshold].index,
                               IQR_dict['median'][IQR_dict['count'] >= count_threshold],
                               color=colour_dict[pair_id], marker=linestyle_dict['median'], s=20, edgecolor='k',
                               zorder=3)

                    # transparent markers for points bellow threshold
                    ax.scatter(IQR_dict['mean'][IQR_dict['count'] < count_threshold].index,
                               IQR_dict['mean'][IQR_dict['count'] < count_threshold],
                               marker=linestyle_dict['mean'], s=15, edgecolor=colour_dict[pair_id], zorder=4,
                               facecolors='None')
                    ax.scatter(IQR_dict['median'][IQR_dict['count'] < count_threshold].index,
                               IQR_dict['median'][IQR_dict['count'] < count_threshold],
                               marker=linestyle_dict['median'], s=20, edgecolor=colour_dict[pair_id], zorder=4,
                               facecolors='None')

                    # for col in IQR_dict['25']:
                    #     if col not in IQR_dict['mean'][IQR_dict['count'] >= count_threshold].index:
                    #         IQR_dict['25'] = IQR_dict['25'].drop(columns=[col])
                    #         IQR_dict['75'] = IQR_dict['75'].drop(columns=[col])

                    ax.fill_between(IQR_dict['25'].columns, IQR_dict['25'].iloc[0], IQR_dict['75'].iloc[0],
                                    color=colour_dict[pair_id], alpha=0.2, zorder=1)

                ax.plot(IQR_dict_UKV['mean'].index, IQR_dict_UKV['mean'], color=colour_dict[pair_id],
                        linestyle=linestyle_dict['UKV_mean'], zorder=2)
                ax.plot(IQR_dict_UKV['median'].index, IQR_dict_UKV['median'], color=colour_dict[pair_id],
                        linestyle=linestyle_dict['UKV_median'], zorder=2)

            ax.get_xaxis().set_major_locator(MaxNLocator(integer=True))

            if variable == 'QH':
                ax.set_ylabel('$Q_{H}$ (W m$^{-2}$)')
            elif variable == 'kdown':
                ax.set_ylabel('$K_{\downarrow}$ (W m$^{-2}$)')

            ax.set_ylim(-10, ylim)
            ax.set_xlim(4.5, 19.5)
            ax.set_xlabel('Hour')

            if season == 'MAM':
                if pair_id == 'IMU_BTT':
                    # manually create legend
                    handles, labels = plt.gca().get_legend_handles_labels()

                    scatter_mean = plt.scatter([1000], [1000], label='LAS Mean', color='grey',
                                               marker=linestyle_dict['mean'], edgecolor='k')
                    scatter_median = plt.scatter([1000], [1000], label='LAS Median', color='grey',
                                                 marker=linestyle_dict['median'], edgecolor='k')
                    scatter_median_hollow = plt.scatter([1000], [1000],
                                                        label='Data count under ' + str(count_threshold),
                                                        facecolors='None',
                                                        marker=linestyle_dict['median'], edgecolor='grey')

                    line_mean_ukv = Line2D([0], [0], label='UKV Mean', color='k', linestyle=linestyle_dict['UKV_mean'])
                    line_median_ukv = Line2D([0], [0], label='UKV Median', color='k',
                                             linestyle=linestyle_dict['UKV_median'])

                    IQR_patch = mpatches.Patch(color='k', label='LAS IQR', alpha=0.2)

                    handles.extend([scatter_mean, scatter_median, scatter_median_hollow, IQR_patch, line_mean_ukv,
                                    line_median_ukv])
                    # plt.legend(handles=handles, loc='center left', bbox_to_anchor=(1, 0.5))

            plt.tight_layout()

            # plt.show()

            path_name_here = look_up.scint_path_numbers[
                int(season_dict[list(season_dict.keys())[0]].drop(columns=[variable + '_12']).columns[0].split('_')[
                        -1])]

            save_path_string = save_path + str(average) + '/'

            plt.savefig(save_path_string + variable + '_' + path_name_here + '_' + season + '_seasonality.png',
                        bbox_inches='tight', dpi=300)


def plot_season(season_dict, save_path, variable='QH'):
    """

    :return:
    """

    colour_dict = {'BCT_IMU': 'red', 'SCT_SWT': 'mediumorchid', 'IMU_BTT': 'green', 'BTT_BCT': 'blue'}

    fig, ax = plt.subplots(1, len(season_dict), figsize=(4 * len(season_dict), 5))

    all_seasons = ['DJF', 'MAM', 'JJA', 'SON']

    axis_count = 0

    # axis limits
    y_lims = []

    for season in all_seasons:

        if season in season_dict.keys():
            df_season = season_dict[season]
            ax[axis_count].set_title(season)

            IQR_path_dict = IQR(df_season)

            for path in IQR_path_dict:

                IQR_dict = IQR_path_dict[path]
                pair_id = look_up.scint_path_numbers[int(path.split('_')[-1])]

                ax[axis_count].plot(IQR_dict['mean'].index, IQR_dict['mean'], color=colour_dict[pair_id])
                ax[axis_count].plot(IQR_dict['median'].index, IQR_dict['median'], color=colour_dict[pair_id],
                                    linestyle=':')
                ax[axis_count].plot(IQR_dict['25'].columns, IQR_dict['25'].iloc[0], color=colour_dict[pair_id],
                                    linestyle='--')
                ax[axis_count].plot(IQR_dict['75'].columns, IQR_dict['75'].iloc[0], colour_dict[pair_id],
                                    linestyle='--')
                ax[axis_count].fill_between(IQR_dict['25'].columns, IQR_dict['25'].iloc[0], IQR_dict['75'].iloc[0],
                                            color=colour_dict[pair_id], alpha=0.1)

                ax[axis_count].get_xaxis().set_major_locator(MaxNLocator(integer=True))

                if axis_count != 0:
                    ax[axis_count].get_yaxis().set_ticks([])
                else:
                    if variable == 'QH':
                        ax[0].set_ylabel('$Q_{H}$ (W m$^{-2}$)')
                    elif variable == 'kdown':
                        ax[0].set_ylabel('$K_{\downarrow}$ (W m$^{-2}$)')

                y_lim_here = IQR_dict['75'].max().max()
                y_lims.append(y_lim_here)

            axis_count += 1

    ylim = max(y_lims) + 10
    for axs in ax:
        axs.set_ylim(0, ylim)
        axs.set_xlim(5, 19)
        axs.set_xlabel('Hour')

    plt.tight_layout()

    # plt.show()
    path_name_here = look_up.scint_path_numbers[
        int(season_dict[list(season_dict.keys())[0]].drop(columns=['QH_12']).columns[0].split('_')[-1])]
    plt.savefig(save_path + path_name_here + '_seasonality.png', bbox_inches='tight', dpi=300)

    print('end')


def IQR(df):
    """

    :return:
    """

    for column in df.columns:
        if column.split('_')[-1] != '12':
            other_col_name = column
        else:
            column_name_12 = column

    df_12 = df.drop(columns=[other_col_name])
    df_other = df.drop(columns=[column_name_12])

    df_path_list = [df_12, df_other]
    dict_path = {}

    for df_path in df_path_list:

        df_day_list = [group[1] for group in df_path.groupby(df_path.index.date)]

        df_av_list = []

        for i, item in enumerate(df_day_list):
            item['hour'] = item.index.strftime('%H').astype(int)

            df_here = item

            df_here = df_here.set_index('hour')
            df_T = df_here.T

            df_T.index = [item.index[0]]
            df_av_list.append(df_T)

        test = pd.concat(df_av_list)
        test_mean = test.mean()

        test_count = test.count()

        test_25 = test.quantile([.25])
        test_75 = test.quantile([.75])

        test_median = test.median()

        dict_path[df_path.columns[0]] = {'mean': test_mean, '25': test_25, '75': test_75, 'median': test_median,
                                         'count': test_count}

    return dict_path


def split_df_into_season(df):
    """

    :return:
    """

    # group dfs by month
    months = {n: g for n, g in df.groupby(pd.Grouper(freq='M'))}

    # get rid of empty months
    for key in list(months):
        if len(months[key]) == 0:
            months.pop(key, None)

    DJF = []
    MAM = []
    JJA = []
    SON = []

    season_dict = {}
    for key in list(months):

        month_num = key.month

        if month_num == 1 or month_num == 2 or month_num == 12:
            DJF.append(months[key])
        elif month_num == 3 or month_num == 4 or month_num == 5:
            MAM.append(months[key])
        elif month_num == 6 or month_num == 7 or month_num == 8:
            JJA.append(months[key])
        else:
            SON.append(months[key])

    if len(DJF) != 0:
        df_DJF = pd.concat(DJF)
        season_dict['DJF'] = df_DJF

    if len(MAM) != 0:
        df_MAM = pd.concat(MAM)
        season_dict['MAM'] = df_MAM

    if len(JJA) != 0:
        df_JJA = pd.concat(JJA)
        season_dict['JJA'] = df_JJA

    if len(SON) != 0:
        df_SON = pd.concat(SON)
        season_dict['SON'] = df_SON

    return season_dict


def drop_unchosen_cols(path_choice, df):
    # drop any path other than the one chosen and BCT_IMU
    for col in df.columns:
        if path_choice == int(col.split('_')[-1]):
            pass
        elif int(col.split('_')[-1]) == 12:
            pass
        else:
            df = df.drop(columns=[col])
    return df
