import pandas as pd
import matplotlib.pyplot as plt

def plot_season(season_dict):
    """

    :return:
    """

    fig, ax = plt.subplots(1, len(season_dict), figsize=(4*len(season_dict), 6))



    print('end')




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
