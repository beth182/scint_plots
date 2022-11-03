import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def lc_in_sa_stacked_bar(sas_df_in, save_path):
    """
    Takes a dataframe of the land cover fractions present in the peropd's source areas
        And produces a stacked bar chart of them
    :param sas_df_in:
    :return:
    """

    if type(sas_df_in) == str:  # added option for reading in csv files

        sas_df = pd.read_csv(sas_df_in)
        sas_df.index = sas_df['Unnamed: 0']
        sas_df = sas_df.drop('Unnamed: 0', 1)

        sas_df.index = pd.to_datetime(sas_df.index, dayfirst=True)

    else:

        sas_df = sas_df_in

    # reading model weighted lc fraction csv file
    # made from scint_eval ukv_landuse functions file
    csv_path = 'C:/Users/beths/Desktop/LANDING/weighted_lc_ukv_' + sas_df.index[0].strftime('%Y') + sas_df.index[
        0].strftime('%j') + '.csv'
    ukv_df = pd.read_csv(csv_path)

    ukv_df['Unnamed: 0'] = pd.to_datetime(ukv_df['Unnamed: 0'], format='%y%m%d%H')
    ukv_df = ukv_df.rename(columns={'Unnamed: 0': 'Time'})
    ukv_df = ukv_df.set_index('Time')

    # get rid of the masks: must be a better way of doing this
    dict_for_df = {}

    for col in sas_df.columns:

        new_col = []

        for item in sas_df[col]:
            if type(item) != float:
                new_col.append(0)
            else:
                new_col.append(item)

        dict_for_df[col] = new_col

    new_df = pd.DataFrame.from_dict(dict_for_df)
    new_df.index = sas_df.index

    # Box plot
    # take only building, impervious, grass, water
    df_select = new_df[['Building', 'Impervious', 'Water', 'Grass']]

    df_select.index.names = ['Time']
    df_select['Hour'] = df_select.index.hour + 1

    if df_select.index[0].strftime('%j') == '123':
        end_remove = pd.to_datetime('2016-05-02 17:00:00')
        df_select = df_select.loc[(df_select.index < end_remove)]

    elif df_select.index[0].strftime('%j') == '126':
        start_remove = pd.to_datetime('2016-05-05 06:00:00')
        end_remove = pd.to_datetime('2016-05-05 18:00:00')

        df_select = df_select.loc[(df_select.index >= start_remove)]
        df_select = df_select.loc[(df_select.index < end_remove)]

    fig, ax = plt.subplots(1, figsize=(12, 12))

    props_building = dict(boxes='#696969', whiskers="Black", medians="Black", caps="Black")
    props_imperv = dict(boxes="#BEBEBE", whiskers="Black", medians="Black", caps="Black")
    props_water = dict(boxes="#00BFFF", whiskers="Black", medians="Black", caps="Black")
    props_grass = dict(boxes="#7CFC00", whiskers="Black", medians="Black", caps="Black")

    bp_build = df_select.boxplot('Building', 'Hour', ax=ax, color=props_building, patch_artist=True, sym='#696969',
                                 widths=0.95, return_type='dict')
    bp_imp = df_select.boxplot('Impervious', 'Hour', ax=ax, color=props_imperv, patch_artist=True, sym='#BEBEBE',
                               widths=0.95, return_type='dict')
    bp_wat = df_select.boxplot('Water', 'Hour', ax=ax, color=props_water, patch_artist=True, sym='#00BFFF', widths=0.95,
                               return_type='dict')
    bp_gra = df_select.boxplot('Grass', 'Hour', ax=ax, color=props_grass, patch_artist=True, sym='#7CFC00', widths=0.95,
                               return_type='dict')

    [patch.set(alpha=0.6) for patch in bp_build['Building']['boxes']]
    [patch.set(alpha=0.6) for patch in bp_imp['Impervious']['boxes']]
    [patch.set(alpha=0.6) for patch in bp_wat['Water']['boxes']]
    [patch.set(alpha=0.6) for patch in bp_gra['Grass']['boxes']]

    fig.suptitle('')
    ax.set_title('')

    bld_patch = mpatches.Patch(color='#696969', label='Building', alpha=0.6)
    imp_patch = mpatches.Patch(color='#BEBEBE', label='Paved', alpha=0.6)
    water_patch = mpatches.Patch(color='#00BFFF', label='Water', alpha=0.6)
    grass_patch = mpatches.Patch(color='#7CFC00', label='Grass', alpha=0.6)

    ukv_can = ax.scatter(ukv_df.index.hour - (ukv_df.index.hour[0] - 1), ukv_df.canyon * 100, marker='x',
                         color='darkgrey', s=100)
    ukv_roof = ax.scatter(ukv_df.index.hour - (ukv_df.index.hour[0] - 1), ukv_df.roof * 100, marker='x',
                          color='dimgrey', s=100)
    ukv_c3 = ax.scatter(ukv_df.index.hour - (ukv_df.index.hour[0] - 1), ukv_df.C3 * 100, marker='x', color='lawngreen',
                        s=100)
    ukv_lake = ax.scatter(ukv_df.index.hour - (ukv_df.index.hour[0] - 1), ukv_df.lake * 100, marker='x',
                          color='deepskyblue', s=100)

    if sas_df.index[0].strftime('%j') == '123':
        plt.legend(handles=[bld_patch, imp_patch, water_patch, grass_patch], framealpha=1)

    ax.set_ylim(0, 60)

    plt.savefig(save_path + sas_df.index[0].strftime('%j') + '_boxplot.png', bbox_inches='tight', dpi=300)
    print('end')
