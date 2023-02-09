# imports
import pandas as pd
import numpy as np
import os
import datetime as dt

from scint_flux import look_up


def read_preprocessed_lc_csv(scint_path,
                             DOY_list,
                             save_path):
    # read a given set of day's sa-weighted lc fractions, and return them as one df

    pair_id = look_up.scint_path_numbers[scint_path]
    # lc csv dir location
    lc_csv_dir = save_path + 'sa_lc_fractions/' + pair_id + '/'

    lc_types = ['Building', 'Impervious', 'Water', 'Grass', 'Deciduous', 'Evergreen', 'Shrub']

    DOY_df_list = []

    for DOY in DOY_list:

        dt_obj = dt.datetime.strptime(str(DOY), '%Y%j')
        DOY_str = dt_obj.strftime('%j')
        year_str = dt_obj.strftime('%Y')

        # construct file path
        file_name = pair_id + '_' + year_str + DOY_str + '_weighted_sa_lc.csv'
        file_path = lc_csv_dir + file_name

        # make sure file exists
        assert os.path.isfile(file_path)

        # read file
        DOY_lc_df = pd.read_csv(file_path)
        DOY_lc_df = DOY_lc_df.rename(columns={'Unnamed: 0': 'time'})
        DOY_lc_df.index = DOY_lc_df['time']
        DOY_lc_df = DOY_lc_df.drop('time', 1)
        DOY_lc_df.index = pd.to_datetime(DOY_lc_df.index, format='%Y-%m-%d %H:%M:%S')

        # replace mask with 0
        lc_outputs_df = pd.DataFrame({'Building': [], 'Impervious': [], 'Water': [], 'Grass': [],
                                      'Deciduous': [], 'Evergreen': [], 'Shrub': []})

        for i, row in DOY_lc_df.iterrows():

            time = i

            Building = DOY_lc_df['Building'][np.where(DOY_lc_df.index == time)[0]]
            Impervious = DOY_lc_df['Impervious'][np.where(DOY_lc_df.index == time)[0]]
            Water = DOY_lc_df['Water'][np.where(DOY_lc_df.index == time)[0]]
            Grass = DOY_lc_df['Grass'][np.where(DOY_lc_df.index == time)[0]]
            Deciduous = DOY_lc_df['Deciduous'][np.where(DOY_lc_df.index == time)[0]]
            Evergreen = DOY_lc_df['Evergreen'][np.where(DOY_lc_df.index == time)[0]]
            Shrub = DOY_lc_df['Shrub'][np.where(DOY_lc_df.index == time)[0]]

            df_dict = {'time': [time]}

            for lc_type in lc_types:

                lc_type_series = DOY_lc_df[lc_type][np.where(DOY_lc_df.index == time)[0]]

                if len(lc_type_series) == 0:
                    nan_series = pd.Series([np.nan])
                    lc_type_series = lc_type_series.append(nan_series)
                else:
                    if type(lc_type_series.values[0]) == str:
                        lc_type_series.values[0] = 0

                try:
                    df_dict[lc_type] = 1 * lc_type_series.values[0]
                except:
                    print('end')

            period_df = pd.DataFrame(df_dict)
            period_df = period_df.set_index('time')

            lc_outputs_df = lc_outputs_df.append(period_df)

        lc_outputs_df['sum'] = lc_outputs_df.sum(axis=1)
        lc_outputs_df['Urban'] = lc_outputs_df['Building'] + lc_outputs_df['Impervious']

        DOY_df_list.append(lc_outputs_df)

    df = pd.concat(DOY_df_list)

    return df


def read_preprocessed_scint_csv(scint_path,
                                DOY_list,
                                save_path):
    # take the subset of days from the pre made csvs with hourly obs data - that have been read in to save time

    # ToDo: compare this version with the one in path comparison - scatter
    # ToDo: consider moving these to generic location
    pre_made_csv_dir = save_path + '../path_comparison/'

    # select the target path
    path_data_filepath = pre_made_csv_dir + 'path_' + str(scint_path) + '_vals.csv'

    # read the csv
    scint_df = pd.read_csv(path_data_filepath)
    scint_df['time'] = pd.to_datetime(scint_df['time'], format='%Y-%m-%d %H:%M:%S')
    scint_df = scint_df.set_index('time')

    # take just the days in the DOY list
    df_DOY_list = []
    for DOY in DOY_list:
        dt_obj = dt.datetime.strptime(str(DOY), '%Y%j')
        next_day = dt_obj + dt.timedelta(days=1)

        mask = (scint_df.index >= dt_obj) & (scint_df.index < next_day)
        df_DOY = scint_df.loc[mask]

        df_DOY_list.append(df_DOY)

    df = pd.concat(df_DOY_list)

    return df
