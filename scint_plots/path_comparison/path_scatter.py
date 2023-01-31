# Beth Saunders 31/01/2023
# script to produce a scatter plot of QH from 2 paths

# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


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

def scatter_paths(df_combine):
    """

    :return:
    """
    fig, ax = plt.subplots(1, 4, figsize=(15, 5), gridspec_kw={'width_ratios': [1, 1, 1, 0.1]})

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

    # BCT_IMU VS BTT_BCT
    # weekday
    weekday_label_0 = 'Weekday\nn hours: ' + str(len(df_weekday[['QH_11', 'QH_12']].dropna())) + '\nn days: ' + str(len(
        [group[1] for group in
         df_weekday[['QH_11', 'QH_12']].dropna().groupby(df_weekday[['QH_11', 'QH_12']].dropna().index.date)]))
    ax[0].scatter(df_weekday.QH_11, df_weekday.QH_12, marker='+', c=df_weekday.index.strftime('%j').astype(int),
                       norm=norm, cmap=cmap, label=weekday_label_0, alpha=0.4)
    # weekend
    weekend_label_0 = 'Weekend\nn hours: ' + str(len(df_weekend[['QH_11', 'QH_12']].dropna())) + '\nn days: ' + str(len(
        [group[1] for group in
         df_weekend[['QH_11', 'QH_12']].dropna().groupby(df_weekend[['QH_11', 'QH_12']].dropna().index.date)]))
    ye = ax[0].scatter(df_weekend.QH_11, df_weekend.QH_12, marker='.', c=df_weekend.index.strftime('%j').astype(int),
                  norm=norm, cmap=cmap, label=weekend_label_0)

    ax[0].legend(loc="lower right")

    # BCT_IMU VS SCT_SWT
    # weekday
    weekday_label_1 = 'Weekday\nn hours: ' + str(len(df_weekday[['QH_15', 'QH_12']].dropna())) + '\nn days: ' + str(len(
        [group[1] for group in
         df_weekday[['QH_15', 'QH_12']].dropna().groupby(df_weekday[['QH_15', 'QH_12']].dropna().index.date)]))
    ax[1].scatter(df_weekday.QH_15, df_weekday.QH_12, marker='+', c=df_weekday.index.strftime('%j').astype(int),
                  norm=norm, cmap=cmap, label = weekday_label_1, alpha=0.4)
    # weekend
    weekend_label_1 = 'Weekend\nn hours: ' + str(len(df_weekend[['QH_15', 'QH_12']].dropna())) + '\nn days: ' + str(len(
        [group[1] for group in
         df_weekend[['QH_15', 'QH_12']].dropna().groupby(df_weekend[['QH_15', 'QH_12']].dropna().index.date)]))
    ax[1].scatter(df_weekend.QH_15, df_weekend.QH_12, marker='.', c=df_weekend.index.strftime('%j').astype(int),
                  norm=norm, cmap=cmap, label=weekend_label_1)

    ax[1].legend(loc="lower right")

    # BCT_IMU VS IMU_BTT
    # weekday
    weekday_label_2 = 'Weekday\nn hours: ' + str(len(df_weekday[['QH_13', 'QH_12']].dropna())) + '\nn days: ' + str(len(
        [group[1] for group in
         df_weekday[['QH_13', 'QH_12']].dropna().groupby(df_weekday[['QH_13', 'QH_12']].dropna().index.date)]))
    ax[2].scatter(df_weekday.QH_13, df_weekday.QH_12, marker='+', c=df_weekday.index.strftime('%j').astype(int),
                  norm=norm, cmap=cmap, label=weekday_label_2, alpha=0.4)
    # weekend
    weekend_label_2 = 'Weekend\nn hours: ' + str(len(df_weekend[['QH_13', 'QH_12']].dropna())) + '\nn days: ' + str(len(
        [group[1] for group in
         df_weekend[['QH_13', 'QH_12']].dropna().groupby(df_weekend[['QH_13', 'QH_12']].dropna().index.date)]))
    ax[2].scatter(df_weekend.QH_13, df_weekend.QH_12, marker='.', c=df_weekend.index.strftime('%j').astype(int),
                  norm=norm, cmap=cmap, label=weekend_label_2)

    ax[2].legend(loc="lower right")


    ax[0].set_ylabel('BCT_IMU $Q_{H}$ ($W m^{-2}$)')
    ax[0].set_xlabel('BTT_BCT $Q_{H}$ ($W m^{-2}$)')
    ax[1].set_xlabel('SCT_SWT $Q_{H}$ ($W m^{-2}$)')
    ax[2].set_xlabel('IMU_BTT $Q_{H}$ ($W m^{-2}$)')

    ax_x_max = df_combine.max().max() + 10
    ax_y_max = df_combine.QH_12.max().max() + 10

    ax_min = 0
    ax[0].set_xlim(ax_min, ax_x_max)
    ax[1].set_xlim(ax_min, ax_x_max)
    ax[2].set_xlim(ax_min, ax_x_max)

    ax[0].set_ylim(ax_min, ax_y_max)
    ax[1].set_ylim(ax_min, ax_y_max)
    ax[2].set_ylim(ax_min, ax_y_max)

    ax[0].plot((ax_min, ax_y_max), (ax_min, ax_y_max), color='k')
    ax[1].plot((ax_min, ax_y_max), (ax_min, ax_y_max), color='k')
    ax[2].plot((ax_min, ax_y_max), (ax_min, ax_y_max), color='k')

    cax = ax[3]
    cbar = fig.colorbar(mappable=ye, cax=cax, format='%.0f')
    cbar.ax.set_title('DOY')

    fig.tight_layout()

    # plt.show()
    plt.savefig('C:/Users/beths/Desktop/LANDING/scatter.png', bbox_inches='tight')

df_combine = read_all_scint_data()

# temp investigation
for group in df_combine[['QH_11']].dropna().groupby(df_combine[['QH_11']].dropna().index.date):
    print(group[0].strftime('%Y%j'))



scatter_paths(df_combine)

print('end')
