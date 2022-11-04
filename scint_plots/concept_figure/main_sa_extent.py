import os

from scint_plots.concept_figure import concept_figure_funs

save_path = os.getcwd().replace('\\', '/') + '/'
concept_figure_funs.run_concept_fig(save_path)

print('end')
