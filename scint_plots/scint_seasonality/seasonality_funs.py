import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from scint_flux import look_up


def plot_season(season_dict, variable='QH'):
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
                ax[axis_count].plot(IQR_dict['median'].index, IQR_dict['median'], color=colour_dict[pair_id], linestyle=':')
                ax[axis_count].plot(IQR_dict['25'].columns, IQR_dict['25'].iloc[0], color=colour_dict[pair_id], linestyle='--')
                ax[axis_count].plot(IQR_dict['75'].columns, IQR_dict['75'].iloc[0], colour_dict[pair_id], linestyle='--')
                ax[axis_count].fill_between(IQR_dict['25'].columns, IQR_dict['25'].iloc[0], IQR_dict['75'].iloc[0], color=colour_dict[pair_id], alpha=0.1)

                ax[axis_count].get_xaxis().set_major_locator(MaxNLocator(integer=True))

                if axis_count != 0:
                    ax[axis_count].get_yaxis().set_ticks([])
                else:
                    if variable == 'QH':
                        ax[0].set_ylabel('$Q_{H}$ ($W m^{-2}$)')
                    elif variable == 'kdown':
                        ax[0].set_ylabel('$K_{\downarrow}$ ($W m^{-2}$)')


                y_lim_here = IQR_dict['75'].max().max()
                y_lims.append(y_lim_here)

            axis_count += 1


    ylim = max(y_lims) + 10
    for axs in ax:
        axs.set_ylim(0, ylim)
        axs.set_xlim(5, 19)
        axs.set_xlabel('Hour')

    plt.tight_layout()

    plt.show()
    print('end')





def IQR(df):
    """

    :return:
    """

    for column in df.columns:
        if column != 'QH_12':
            other_col_name = column

    df_12 = df.drop(columns=[other_col_name])
    df_other = df.drop(columns=['QH_12'])

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
