import numpy as np
import pandas as pd


def combine(df_list, on_hour=True):
    new_df_list = []

    for df in df_list:

        time_delta = df.index[1] - df.index[0]
        minutes = time_delta.seconds // 60

        var_df_list = []

        for col_name in df.columns:

            df_QH = df[col_name]
            df_QH.name = col_name + '_obs_' + str(minutes)

            if on_hour == True:
                df_QH = df_QH.iloc[np.where([i.minute == 0 for i in df_QH.index])[0]]

            var_df_list.append(df_QH)

        all_var_df = pd.concat(var_df_list, axis=1)

        new_df_list.append(all_var_df)

    combine_df = pd.concat(new_df_list, axis=1)

    return combine_df
