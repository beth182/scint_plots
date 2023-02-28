# Beth Saunders 26/01/2023
# script to plot stacked bar of UKV grid landcover fractions

# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from model_eval_tools import look_up

# user choice
grid_number = 21

# ToDo: move the scripts used to make these csv files over to here from Model_eval

# save path for plot
save_path = os.getcwd().replace('\\', '/') + '/'

# existing csv file location
# ToDo: move to here
csv_dir = 'C:/Users/beths/OneDrive - University of Reading/landuse/site grids/10-tile landuse (Maggie_new)/landuse_csv_files/'

# use lookup to know which grid number is which site and letter in CSV
# ToDo: save site + letter to number reference locally
grid_name = look_up.grid_dict_lc[grid_number][0]
site_name, grid_letter = grid_name.split(' ')

csv_file_name = site_name + '_10T.csv'
csv_file_path = csv_dir + csv_file_name

# pandas read site file
site_df = pd.read_csv(csv_file_path).set_index('GRID')

# combine veg into one type
site_df['Veg'] = site_df['broadleaf'] + site_df['needleleaf'] + site_df['C3'] + site_df['C4'] + site_df['shrubs']

# drop the cols that make up veg
site_df = site_df.drop(['broadleaf', 'needleleaf', 'C3', 'C4', 'shrubs', 'ice'], axis=1)

# re-order columns so veg is before impervious
site_df = site_df[['lake', 'Veg', 'soil', 'canyon', 'roof']]

# pandas df for just the target grid from letter
# grid_df = site_df.iloc[np.where(site_df.index == grid_letter)[0]]
grid_df = site_df.loc[grid_letter]

# plot
series_labels = ['Water', 'Vegetation', 'Soil', 'Impervious', 'Building']
colors = [[(0/256, 191/256, 255/256)], [(202/256, 255/256, 112/256)], 'sienna', [(211/256, 211/256, 211/256)], [(105/256, 105/256, 105/256)]]

f, ax = plt.subplots(figsize=(10, 10))

data = list(grid_df.values)
ny = len(data)
data = np.array(data)

ind = list(range(ny))
axes = []
cum_size = np.zeros(ny)

for i, row_data in enumerate(data):

    axes.append(ax.bar(ind, row_data, bottom=cum_size, color=colors[i], width=1.0,
                       label=series_labels[i]))

    cum_size += row_data

    ax.axes.get_xaxis().set_visible(False)

    xbuffer = 0
    ax.set_xlim(-xbuffer, len(ind) - 1 + xbuffer)
    ax.set_ylim(0, 1)

    ax.axes.get_yaxis().set_visible(False)

# plt.legend(bbox_to_anchor=(1.0, 0.5))

# save plot
# plt.show()
plt.savefig(save_path + str(grid_number) + '_ukv_lc.png', bbox_inches='tight', dpi=300)
print('end')