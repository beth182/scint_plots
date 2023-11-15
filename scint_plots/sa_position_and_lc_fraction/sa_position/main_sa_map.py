import os
import matplotlib.pyplot as plt

import scint_fp.functions.plot_functions.plot_sa_lines.sa_lines_funs as sa_lines

doy_choice = 126
# ToDo: move these
sa_dir = 'C:/Users/beths/OneDrive - University of Reading/local_runs_data/fp_output/' + str(doy_choice) + '/hourly/'

save_path = os.getcwd().replace('\\', '/') + '/'

file_list = sa_lines.find_SA_rasters(sa_main_dir=sa_dir)
colour_list = sa_lines.get_colours(cmap=plt.cm.inferno, file_list=file_list)
sa_lines.plot_sa_lines(file_list=file_list, colour_list=colour_list, doy_choice=doy_choice, save_path=save_path)
print('end')
