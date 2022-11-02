import os
import matplotlib.pyplot as plt

from scint_plots.sa_position_and_lc_fraction import sa_map_funs

doy_choice = 123
# ToDo: move these
sa_dir = 'C:/Users/beths/Desktop/LANDING/fp_output/' + str(doy_choice) + '/hourly/'

save_path = os.getcwd().replace('\\', '/') + '/'

file_list = sa_map_funs.find_SA_rasters(sa_main_dir=sa_dir)
colour_list = sa_map_funs.get_colours(cmap=plt.cm.inferno, file_list=file_list)
sa_map_funs.plot_sa_lines(file_list=file_list, colour_list=colour_list, doy_choice=doy_choice, save_path=save_path)
print('end')
