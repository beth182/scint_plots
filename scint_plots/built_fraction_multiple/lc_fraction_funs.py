# imports
import pandas as pd
import numpy as np
import os
import datetime as dt

from scint_flux import look_up


def combine_scint_and_lc():
    # combine lc fraction csv's and pre-read hourly data csvs
    print('end')


def read_preprocessed_lc_csv(scint_path,
                             DOY_list,
                             save_path):
    # read a given set of day's sa-weighted lc fractions, and return them as one df

    print('end')


def read_preprocessed_scint_csv(scint_path,
                                DOY_list,
                                save_path):
    # take the subset of days from the pre made csvs with hourly obs data - that have been read in to save time

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


# user choice
scint_path = 15

save_path = save_path = os.getcwd().replace('\\', '/') + '/'

# read in all files
# read in csv with days
DOY_df = pd.read_csv('C:/Users/beths/OneDrive - University of Reading/Paper 2/days_to_be_read_in.csv')
# DOY_df = pd.read_csv('C:/Users/beths/OneDrive - University of Reading/Paper 2/all_days.csv')
# take only days of the target path
scint_path_string = 'P' + str(scint_path)
df_subset = DOY_df.iloc[np.where(DOY_df[scint_path_string] == 1)[0]]
df_subset['DOY_string'] = df_subset.year.astype(str) + df_subset.DOY.astype(str)
df_subset['DOY_string'] = df_subset['DOY_string'].astype(int)
DOY_list = df_subset.DOY_string.to_list()

# ToDo: replace this temp line to take whole dataset
DOY_list = DOY_list[:2]

lc_df = read_preprocessed_lc_csv(scint_path=scint_path, DOY_list=DOY_list, save_path=save_path)

# scint_df = read_preprocessed_scint_csv(scint_path=scint_path, DOY_list=DOY_list, save_path=save_path)
