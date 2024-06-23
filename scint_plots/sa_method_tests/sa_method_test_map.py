import os
import matplotlib.pyplot as plt

import scint_fp.functions.plot_functions.plot_sa_lines.sa_lines_funs as sa_lines



current_dir = os.getcwd().replace('\\', '/') + '/'


sa_test_dir = current_dir + 'SA_examples_to_plot/'

file_list = sa_lines.find_SA_rasters(sa_main_dir=sa_test_dir)

colour_list = ['red', 'red', 'blue', 'blue']

custom_linetype = ['-', '--', '-', '--']

custom_marker = ['x', 'o', 'x', 'o']

custom_labels = ['IOP-1 EC-fp varying', 'IOP-1 EC-fp constant', 'IOP-2 EC-fp varying', 'IOP-2 EC-fp constant']

sa_lines.plot_sa_lines(file_list=file_list, colour_list=colour_list, doy_choice=False, save_path=current_dir, custom_labels=custom_labels, custom_linetype=custom_linetype, custom_marker=custom_marker)

print('end')

