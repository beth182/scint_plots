# Beth Saunders 03/02/23
# Script to produce a histogram for counting the occurance of hours in each study period day

# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.lines import Line2D

from scint_flux import look_up
from scint_flux.functions import read_calculated_fluxes


def create_hour_csvs(scint_path_list, save_path):
    """

    :return:
    """

    for scint_path in scint_path_list:

        var_list = ['QH']
        time_res = '1min_sa10_mins_ending'

        # read in all files
        # read in csv with days
        DOY_df = pd.read_csv('C:/Users/beths/OneDrive - University of Reading/Paper 2/all_days.csv')
        # take only days of the target path
        scint_path_string = 'P' + str(scint_path)
        df_subset = DOY_df.iloc[np.where(DOY_df[scint_path_string] == 1)[0]]
        df_subset['DOY_string'] = df_subset.year.astype(str) + df_subset.DOY.astype(str)
        df_subset['DOY_string'] = df_subset['DOY_string'].astype(int)
        DOY_list = df_subset.DOY_string.to_list()

        pair_id = look_up.scint_path_numbers[scint_path]

        all_days_hours = []
        for DOY in DOY_list:
            # read the observations
            df = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                                     pair_id=pair_id,
                                                     var_list=var_list,
                                                     time_res=time_res)

            # list of hours present without repeating hours
            hours_present = list(dict.fromkeys(df.QH.dropna().index.hour))

            all_hours_list = []

            # add dt for index
            all_hours_list.append(df.index[0])

            for i in range(0, 24):
                if i in hours_present:
                    all_hours_list.append(1)
                else:
                    all_hours_list.append(0)

            all_days_hours.append(all_hours_list)

            print(DOY)

        hours_df = pd.DataFrame(all_days_hours,
                                columns=['time', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                                         20, 21,
                                         22, 23])

        hours_df = hours_df.set_index('time')
        hours_df['month'] = hours_df.index.month

        # create dfs for each season

        # ALL SEASONS
        all_seasons = hours_df.sum().to_frame().transpose()
        all_seasons.index = ['ALL']
        all_seasons = all_seasons.drop(columns=['month'])

        # DJF
        DJF = hours_df.loc[hours_df['month'].isin([12, 1, 2])].sum().to_frame().transpose()
        DJF.index = ['DJF']
        DJF = DJF.drop(columns=['month'])

        # MAM
        MAM = hours_df.loc[hours_df['month'].isin([3, 4, 5])].sum().to_frame().transpose()
        MAM.index = ['MAM']
        MAM = MAM.drop(columns=['month'])

        # JJA
        JJA = hours_df.loc[hours_df['month'].isin([6, 7, 8])].sum().to_frame().transpose()
        JJA.index = ['JJA']
        JJA = JJA.drop(columns=['month'])

        # SON
        SON = hours_df.loc[hours_df['month'].isin([9, 10, 11])].sum().to_frame().transpose()
        SON.index = ['SON']
        SON = SON.drop(columns=['month'])

        all_df = pd.concat([all_seasons, DJF, MAM, JJA, SON])
        all_df = all_df.drop(columns=[0, 1, 2, 3, 20, 21, 22, 23])

        # set path name
        if scint_path == 15:
            path_name = 'SCT_SWT'
        elif scint_path == 12:
            path_name = 'BCT_IMU'
        elif scint_path == 11:
            path_name = 'BTT_BCT'
        else:
            assert scint_path == 13
            path_name = 'IMU_BTT'
        # save df
        all_df.to_csv(save_path + path_name + '_hours.csv')


def hour_histogram(scint_path_list, save_path,
                   colour_dict={'BCT_IMU': 'red', 'SCT_SWT': 'mediumorchid', 'IMU_BTT': 'green', 'BTT_BCT': 'blue'}):
    """

    :return:
    """

    # construct plot
    fig = plt.figure(figsize=(10, 10))

    scint_path_dict = {11: 'BTT_BCT', 12: 'BCT_IMU', 13: 'IMU_BTT', 15: 'SCT_SWT'}

    season_linestyles = {'ALL': '-', 'DJF': '-.', 'MAM': ':', 'JJA': '--', 'SON': (0, (3, 1, 1, 1, 1, 1))}
    season_markerstyles = {'ALL': 'o', 'DJF': 's', 'MAM': 'P', 'JJA': '^', 'SON': 'x'}
    season_list = ['ALL', 'DJF', 'MAM', 'JJA', 'SON']

    # loop over paths
    for scint_path in scint_path_list:

        path_name = scint_path_dict[scint_path]

        # open csv

        df = pd.read_csv(save_path + path_name + '_hours.csv')
        df = df.rename(columns={'Unnamed: 0': 'season'})
        # set index
        df.index = df['season']
        df = df.drop(columns=['season'])

        # find colour
        colour_here = colour_dict[path_name]

        for season in season_list:

            # check the row isn't 0's
            if df.loc[season].sum() == 0:
                pass
            else:

                plt.plot(df.columns, df.loc[season].replace(0, np.nan),
                         linestyle=season_linestyles[season], marker=season_markerstyles[season],
                         color=colour_here,
                         # label=season
                         )

    # manually create legend for seasons
    handles, labels = plt.gca().get_legend_handles_labels()

    line_ALL = Line2D([0], [0], label='ALL', color='k', linestyle=season_linestyles['ALL'],
                      marker=season_markerstyles['ALL'])
    line_DJF = Line2D([0], [0], label='DJF', color='k', linestyle=season_linestyles['DJF'],
                      marker=season_markerstyles['DJF'])
    line_MAM = Line2D([0], [0], label='MAM', color='k', linestyle=season_linestyles['MAM'],
                      marker=season_markerstyles['MAM'])
    line_JJA = Line2D([0], [0], label='JJA', color='k', linestyle=season_linestyles['JJA'],
                      marker=season_markerstyles['JJA'])
    line_SON = Line2D([0], [0], label='SON', color='k', linestyle=season_linestyles['SON'],
                      marker=season_markerstyles['SON'])

    handles.extend([line_ALL, line_DJF, line_MAM, line_JJA, line_SON])

    plt.legend(handles=handles)

    plt.xlabel('Hour')
    plt.ylabel('Count')

    # plt.show()
    plt.savefig(save_path + 'hour_hist.png', bbox_inches='tight', dpi=300)

    print('end')


# create csv files with the hour values
save_path = os.getcwd().replace('\\', '/') + '/'

# re-run to create csvs again
# create_hour_csvs([11,12,13,15], save_path)

hour_histogram([11, 12, 13, 15], save_path)

print('end')
