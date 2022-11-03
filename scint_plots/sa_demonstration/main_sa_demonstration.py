import os

from scint_plots.sa_demonstration import sa_demonstration_funs

# panel_number = 1
# panel_number = 2
panel_number = 3

save_path = os.getcwd().replace('\\', '/') + '/'

sa_demonstration_funs.run_panel_figs(panel_number=panel_number, save_path=save_path)

print('end')
