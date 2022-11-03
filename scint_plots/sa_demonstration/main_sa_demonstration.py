import os

from scint_plots.sa_demonstration import sa_demonstration_funs

save_path = os.getcwd().replace('\\', '/') + '/'

# run one based on choice
# """
# choice one
# panel_number = 1
panel_number = 2
# panel_number = 3

sa_demonstration_funs.run_panel_figs(panel_number=panel_number, save_path=save_path)
# """

# run all
"""
for i in range(1, 4):

    sa_demonstration_funs.run_panel_figs(panel_number=i, save_path=save_path)

"""
print('end')
