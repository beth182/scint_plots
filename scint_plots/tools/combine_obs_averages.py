import numpy as np
import pandas as pd


def combine(df_list, on_hour=True):
    new_df_list = []

    for df in df_list:

        time_delta = df.index[1] - df.index[0]
        minutes = time_delta.seconds // 60

        df_QH = df.QH
        df_QH.name = 'obs_' + str(minutes)

        if on_hour == True:
            df_QH = df_QH.iloc[np.where([i.minute == 0 for i in df_QH.index])[0]]

        new_df_list.append(df_QH)

    combine_df = pd.concat(new_df_list, axis=1).dropna()

    return combine_df
