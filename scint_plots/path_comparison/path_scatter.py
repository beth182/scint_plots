# Beth Saunders 31/01/2023
# script to produce a scatter plot of QH from 2 paths

# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
from scipy import stats

mpl.rcParams.update({'font.size': 15})


def read_all_scint_data():
    """

    :return:
    """

    # read in locally saved files
    path_list = [11, 12, 13, 15]

    path_df_dict = {}
    for path in path_list:
        df = pd.read_csv('./path_' + str(path) + '_vals.csv')
        df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
        df = df.set_index('time')

        # just take the QH col
        df_qh = df[['QH']]
        # rename QH col to be the path + QH
        df_qh = df_qh.rename(columns={'QH': 'QH_' + str(path)})

        # append to dict
        path_df_dict[path] = df_qh

    # combine all paths into one df
    df_combine = pd.concat([path_df_dict[11], path_df_dict[12], path_df_dict[13], path_df_dict[15]], axis=1)

    return df_combine


def rmse(obs, mod):
    # ROOT MEAN SQUARE ERROR FUNCTION
    differencesrmse = mod - obs
    differences_squared = differencesrmse ** 2
    mean_of_differences_squared = differences_squared.mean()
    rmse_val = np.sqrt(mean_of_differences_squared)
    return rmse_val


def scatter_paths(df_combine, save_path):
    """

    :return:
    """
    fig, ax = plt.subplots(1, 4, figsize=(16, 6), gridspec_kw={'width_ratios': [1, 1, 1, 0.1]})

    cmap = mpl.cm.get_cmap('viridis')

    doys = df_combine.index.strftime('%j').astype(int)
    earliest_time = doys.min()
    latest_time = doys.max()
    bounds = np.linspace(earliest_time, latest_time, 30)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    # weekday or weekend?

    df_combine['weekday'] = df_combine.index.weekday

    weekend_index = np.where(df_combine.weekday > 5)[0]
    weekday_index = np.where(df_combine.weekday <= 5)[0]

    assert len(weekend_index) + len(weekday_index) == len(df_combine)

    df_weekend = df_combine.iloc[weekend_index]
    df_weekday = df_combine.iloc[weekday_index]

    # limits of axis
    ax_max = df_combine.max().max() + 10
    ax_min = 0

    # BCT_IMU VS IMU_BTT

    # stats
    # all df
    all_df_0 = df_combine[['QH_13', 'QH_12']].dropna()
    gradient0, intercept0, r_value0, p_value0, std_err0 = stats.linregress(all_df_0.QH_13, all_df_0.QH_12)
    x1_all = np.linspace(ax_min, ax_max, 500)
    y10 = gradient0 * x1_all + intercept0
    ax[0].plot(x1_all, y10, linestyle='--', color='grey', zorder=4)

    # text
    line_string_0 = 'y = ' + str(round(gradient0, 2)) + 'x + ' + str(round(intercept0, 2))
    r_squ_0 = r_value0 ** 2
    rmse_0 = rmse(all_df_0.QH_13, all_df_0.QH_12)

    label_string_0 = line_string_0 + '\n' + '$r^{2}$: ' + str(round(r_squ_0, 2)) + '\n' + 'RMSE: ' + str(round(rmse_0, 2))
    ax[0].text(.01, .99, label_string_0, ha='left', va='top', transform=ax[0].transAxes, color='grey', fontsize=14)


    # weekday
    weekday_label_0 = 'Weekday\nhours: ' + str(len(df_weekday[['QH_13', 'QH_12']].dropna())) + '\ndays: ' + str(len(
        [group[1] for group in
         df_weekday[['QH_13', 'QH_12']].dropna().groupby(df_weekday[['QH_13', 'QH_12']].dropna().index.date)]))
    ax[0].scatter(df_weekday.QH_13, df_weekday.QH_12, marker='+', c=df_weekday.index.strftime('%j').astype(int),
                  norm=norm, cmap=cmap, label=weekday_label_0, alpha=0.6, zorder=2)
    # weekend
    weekend_label_0 = 'Weekend\nhours: ' + str(len(df_weekend[['QH_13', 'QH_12']].dropna())) + '\ndays: ' + str(len(
        [group[1] for group in
         df_weekend[['QH_13', 'QH_12']].dropna().groupby(df_weekend[['QH_13', 'QH_12']].dropna().index.date)]))
    ax[0].scatter(df_weekend.QH_13, df_weekend.QH_12, marker='.', c=df_weekend.index.strftime('%j').astype(int),
                  norm=norm, cmap=cmap, label=weekend_label_0, zorder=3)

    ax[0].legend(loc="lower right", frameon=False)
    ax[0].set_xlabel('IMU_BTT $Q_{H}$ ($W m^{-2}$)')

    ax[0].spines['bottom'].set_color('green')
    ax[0].tick_params(axis='x', colors='green')
    ax[0].xaxis.label.set_color('green')

    # BCT_IMU VS BTT_BCT

    # stats
    # all df
    all_df_1 = df_combine[['QH_11', 'QH_12']].dropna()
    gradient1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(all_df_1.QH_11, all_df_1.QH_12)
    y11 = gradient1 * x1_all + intercept1
    ax[1].plot(x1_all, y11, linestyle='--', color='grey', zorder=4)

    # text
    line_string_1 = 'y = ' + str(round(gradient1, 2)) + 'x + ' + str(round(intercept1, 2))
    r_squ_1 = r_value1 ** 2
    rmse_1 = rmse(all_df_1.QH_11, all_df_1.QH_12)

    label_string_1 = line_string_1 + '\n' + '$r^{2}$: ' + str(round(r_squ_1, 2)) + '\n' + 'RMSE: ' + str(round(rmse_1, 2))
    ax[1].text(.01, .99, label_string_1, ha='left', va='top', transform=ax[1].transAxes, color='grey', fontsize=14)

    # weekday
    weekday_label_1 = 'Weekday\nhours: ' + str(len(df_weekday[['QH_11', 'QH_12']].dropna())) + '\ndays: ' + str(len(
        [group[1] for group in
         df_weekday[['QH_11', 'QH_12']].dropna().groupby(df_weekday[['QH_11', 'QH_12']].dropna().index.date)]))
    ax[1].scatter(df_weekday.QH_11, df_weekday.QH_12, marker='+', c=df_weekday.index.strftime('%j').astype(int),
                  norm=norm, cmap=cmap, label=weekday_label_1, alpha=0.6, zorder=2)
    # weekend
    weekend_label_1 = 'Weekend\nhours: ' + str(len(df_weekend[['QH_11', 'QH_12']].dropna())) + '\ndays: ' + str(len(
        [group[1] for group in
         df_weekend[['QH_11', 'QH_12']].dropna().groupby(df_weekend[['QH_11', 'QH_12']].dropna().index.date)]))
    ye = ax[1].scatter(df_weekend.QH_11, df_weekend.QH_12, marker='.', c=df_weekend.index.strftime('%j').astype(int),
                       norm=norm, cmap=cmap, label=weekend_label_1, zorder=3)

    ax[1].legend(loc="lower right", frameon=False)
    ax[1].set_xlabel('BTT_BCT $Q_{H}$ ($W m^{-2}$)')

    ax[1].set_yticklabels([])

    ax[1].spines['bottom'].set_color('blue')
    ax[1].tick_params(axis='x', colors='blue')
    ax[1].xaxis.label.set_color('blue')

    # BCT_IMU VS SCT_SWT

    # stats
    # all df
    all_df_2 = df_combine[['QH_15', 'QH_12']].dropna()
    gradient2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(all_df_2.QH_15, all_df_2.QH_12)
    y12 = gradient2 * x1_all + intercept2
    ax[2].plot(x1_all, y12, linestyle='--', color='grey', zorder=4)

    # text
    line_string_2 = 'y = ' + str(round(gradient2, 2)) + 'x + ' + str(round(intercept2, 2))
    r_squ_2 = r_value2 ** 2
    rmse_2 = rmse(all_df_2.QH_15, all_df_2.QH_12)

    label_string_2 = line_string_2 + '\n' + '$r^{2}$: ' + str(round(r_squ_2, 2)) + '\n' + 'RMSE: ' + str(round(rmse_2, 2))
    ax[2].text(.01, .99, label_string_2, ha='left', va='top', transform=ax[2].transAxes, color='grey', fontsize=14)

    # weekday
    weekday_label_2 = 'Weekday\nhours: ' + str(len(df_weekday[['QH_15', 'QH_12']].dropna())) + '\ndays: ' + str(len(
        [group[1] for group in
         df_weekday[['QH_15', 'QH_12']].dropna().groupby(df_weekday[['QH_15', 'QH_12']].dropna().index.date)]))
    ax[2].scatter(df_weekday.QH_15, df_weekday.QH_12, marker='+', c=df_weekday.index.strftime('%j').astype(int),
                  norm=norm, cmap=cmap, label=weekday_label_2, alpha=0.6, zorder=2)
    # weekend
    weekend_label_2 = 'Weekend\nhours: ' + str(len(df_weekend[['QH_15', 'QH_12']].dropna())) + '\ndays: ' + str(len(
        [group[1] for group in
         df_weekend[['QH_15', 'QH_12']].dropna().groupby(df_weekend[['QH_15', 'QH_12']].dropna().index.date)]))
    ax[2].scatter(df_weekend.QH_15, df_weekend.QH_12, marker='.', c=df_weekend.index.strftime('%j').astype(int),
                  norm=norm, cmap=cmap, label=weekend_label_2, zorder=3)

    ax[2].legend(loc="lower right", frameon=False)
    ax[2].set_xlabel('SCT_SWT $Q_{H}$ ($W m^{-2}$)')

    ax[2].set_yticklabels([])

    ax[2].spines['bottom'].set_color('mediumorchid')
    ax[2].tick_params(axis='x', colors='mediumorchid')
    ax[2].xaxis.label.set_color('mediumorchid')

    ax[0].set_ylabel('BCT_IMU $Q_{H}$ ($W m^{-2}$)')

    ax[0].spines['left'].set_color('red')
    ax[0].tick_params(axis='y', colors='red')
    ax[0].yaxis.label.set_color('red')
    ax[1].spines['left'].set_color('red')
    ax[1].tick_params(axis='y', colors='red')
    ax[2].spines['left'].set_color('red')
    ax[2].tick_params(axis='y', colors='red')

    ax[0].set_xlim(ax_min, ax_max)
    ax[1].set_xlim(ax_min, ax_max)
    ax[2].set_xlim(ax_min, ax_max)

    ax[0].set_ylim(ax_min, ax_max)
    ax[1].set_ylim(ax_min, ax_max)
    ax[2].set_ylim(ax_min, ax_max)

    ax[0].plot((ax_min, ax_max), (ax_min, ax_max), color='k', zorder=1)
    ax[1].plot((ax_min, ax_max), (ax_min, ax_max), color='k', zorder=1)
    ax[2].plot((ax_min, ax_max), (ax_min, ax_max), color='k', zorder=1)

    cax = ax[3]
    cbar = fig.colorbar(mappable=ye, cax=cax, format='%.0f')
    cbar.ax.set_title('DOY')

    fig.tight_layout()
    plt.subplots_adjust(wspace=0.02, hspace=0.02)

    # plt.show()
    plt.savefig(save_path + 'scatter.png', bbox_inches='tight', dpi=300)


df_combine = read_all_scint_data()

save_path = os.getcwd().replace('\\', '/') + '/'
scatter_paths(df_combine, save_path)

print('end')
