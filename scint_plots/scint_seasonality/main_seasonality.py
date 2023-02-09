# imports
import os

from scint_plots.path_comparison import path_scatter



save_path = os.getcwd().replace('\\', '/') + '/'

# read the premade scint data csv files
df = path_scatter.read_all_scint_data(['QH'], csv_dir=save_path + '../path_comparison/')

print('end')