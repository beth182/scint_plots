import os
import glob

from scint_plots.sa_position_and_lc_fraction import lc_boxplot_funs
from scint_plots.sa_position_and_lc_fraction import create_sa_lc_csv

# CHOICES
doy_choice = 126
av_period = '10_mins'

save_path = os.getcwd().replace('\\', '/') + '/'
csv_file_name = str(doy_choice) + '_' + av_period + '.csv'
csv_file_path = save_path + csv_file_name

# check to see if the csv file exists
if os.path.isfile(csv_file_path):
    sas_df = csv_file_path
else:
    # create the dataframe
    # ToDo: move this: where the SA's are located
    main_dir = 'C:/Users/beths/Desktop/LANDING/fp_output/' + str(doy_choice) + '/' + av_period + '/'
    os.chdir(main_dir)
    file_list = []
    for file in glob.glob("*.tif"):
        file_list.append(main_dir + file)

    sas_df = create_sa_lc_csv.lc_fract_multiple_sas(sa_list=file_list, save_path=save_path)

    # save the df as a csv
    sas_df.to_csv(save_path + csv_file_name)

lc_boxplot_funs.lc_in_sa_stacked_bar(sas_df)
print('end')
