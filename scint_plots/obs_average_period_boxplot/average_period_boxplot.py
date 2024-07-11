import pandas as pd
from scint_flux.functions import read_calculated_fluxes
from scint_flux import look_up
import matplotlib.pyplot as plt
import seaborn
import matplotlib as mpl

mpl.rcParams.update({'font.size': 15})

scint_path = 12
DOY_list = [2016123]

var_list = ['QH', 'kdown']

pair_id = look_up.scint_path_numbers[scint_path]

target_hour = 14

for DOY in DOY_list:

    # read in all the files

    # 1
    df_1 = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                               pair_id=pair_id,
                                               var_list=var_list,
                                               time_res='1min_sa10min' + '_PERIOD_VAR_' + str(1))

    # 2
    df_2 = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                               pair_id=pair_id,
                                               var_list=var_list,
                                               time_res='1min_sa10min' + '_PERIOD_VAR_' + str(2))

    # 3
    df_3 = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                               pair_id=pair_id,
                                               var_list=var_list,
                                               time_res='1min_sa10min' + '_PERIOD_VAR_' + str(3))

    # 5
    df_5 = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                               pair_id=pair_id,
                                               var_list=var_list,
                                               time_res='1min_sa10min' + '_PERIOD_VAR_' + str(5))

    # 10
    df_10 = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                                pair_id=pair_id,
                                                var_list=var_list,
                                                time_res='1min_sa10min' + '_PERIOD_VAR_' + str(10))

    # 15
    df_15 = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                                pair_id=pair_id,
                                                var_list=var_list,
                                                time_res='1min_sa10min' + '_PERIOD_VAR_' + str(15))

    # 20
    df_20 = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                                pair_id=pair_id,
                                                var_list=var_list,
                                                time_res='1min_sa10min' + '_PERIOD_VAR_' + str(20))

    # 30
    df_30 = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                                pair_id=pair_id,
                                                var_list=var_list,
                                                time_res='1min_sa10min' + '_PERIOD_VAR_' + str(30))

    # 60
    df_60 = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                                pair_id=pair_id,
                                                var_list=var_list,
                                                time_res='1min' + '_PERIOD_VAR_' + str(60))

    # whole time period

    cdf = pd.concat(
        [df_60.assign(Average='60'), df_30.assign(Average='30'), df_20.assign(Average='20'), df_15.assign(Average='15'),
         df_10.assign(Average='10'),
         df_5.assign(Average='5'), df_3.assign(Average='3'), df_2.assign(Average='2'), df_1.assign(Average='1')])

    # cdf = cdf[~cdf.index.duplicated()]

    # cdf = df_1.assign(Average=1)

    cdf['hour'] = cdf.index.hour

    plt.figure(figsize=(20, 10))

    seaborn.boxplot(x="hour",
                    y="QH",
                    hue="Average",
                    data=cdf.sort_values(by='Average', key=lambda col: col.astype(int)).reset_index(drop=True),
                    width=1,
                    palette="rainbow_r",
                    showmeans=True,
                    meanline=True,
                    meanprops=dict(color="white"),
                    flierprops={'marker': '.', 'markerfacecolor': 'grey', 'markeredgecolor': 'grey'},
                    whis=[0, 100])

    if DOY == 2016126:
        plt.xlim(6.4, 17.48)
    else:
        assert DOY == 2016123
        plt.xlim(5.4, 17.2)

    if DOY == 2016123:
        title_string = 'IOP-1'
    else:
        assert DOY == 2016126
        title_string = 'IOP-2'

    plt.ylabel("$Q_{H,LAS}$ (W m$^{-2})$")

    plt.xlabel('Time (h, UTC)')

    plt.legend(title='Averaging period (min)')

    plt.title(title_string)

    # plt.show()
    plt.savefig('./time_series_bp_' + str(DOY) + '.png', bbox_inches='tight', dpi=300)

    print('end')
