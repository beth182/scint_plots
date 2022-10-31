import os.path
import pandas as pd
import numpy as np
import datetime as dt


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

    # assert 2016126 in DOY_dict.keys() and 2016123 in DOY_dict.keys()

    for DOY in DOY_dict.keys():
        UKV_kdown_df = DOY_dict[DOY]['UKV_kdown']
        UKV_QH_df = DOY_dict[DOY]['UKV_QH']
        obs_df = DOY_dict[DOY]['obs']
        ukv_lc_df = DOY_dict[DOY]['ukv_lc']

        # convert ukv lc df to datetime index
        ukv_lc_df.index = pd.to_datetime(ukv_lc_df.index, format='%y%m%d%H')
        # add urban column to ukv lc df
        ukv_lc_df['Urban'] = ukv_lc_df['roof'] + ukv_lc_df['canyon']

        # ToDo: got to here
        print('end')
