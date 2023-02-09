# imports
import pandas as pd
import numpy as np
import os
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

mpl.rcParams.update({'font.size': 15})


def plot_built_fraction_4(path_dict, save_path):
    """

    :param df:
    :return:
    """

    # set up figure
    fig, ax = plt.subplots(figsize=(15, 8))

    # get colorbar bounds

    smallest_kdowns = []
    largest_kdowns = []
    smallest_DOYs = []
    largest_DOYs = []

    for path in path_dict:
        df = path_dict[path]

        # subset df where kdown is bellow 100
        target_df = df.iloc[np.where(df.kdown >= 200)[0]][['QH', 'kdown', 'Urban']].dropna()

        smallest_kdown_path = target_df.kdown.min()  # largest radiation value
        largest_kdown_path = target_df.kdown.max()  # smallest radiation value
        smallest_kdowns.append(smallest_kdown_path)
        largest_kdowns.append(largest_kdown_path)

        smallest_doy_path = target_df.index.strftime('%j').astype(int).min()  # smallest DOY
        largest_doy_path = target_df.index.strftime('%j').astype(int).max()  # largest DOY

        smallest_DOYs.append(smallest_doy_path)
        largest_DOYs.append(largest_doy_path)


    smallest_kdown = min(smallest_kdowns)  # largest radiation value
    largest_kdown = max(largest_kdowns)  # smallest radiation value
    smallest_DOY = min(smallest_DOYs)  # smallest DOY
    largest_DOY = max(largest_DOYs)  # largest DOY


    # set up colour bars
    example_path = list(path_dict.keys())[0]
    example_df = path_dict[example_path]
    example_target_df = example_df.iloc[np.where(example_df.kdown >= 200)[0]][['QH', 'kdown', 'Urban']].dropna()

    # set up colourbar: DOY
    cmap_DOY = cm.get_cmap('rainbow')
    bounds_DOY = np.linspace(smallest_DOY, largest_DOY, 256)
    norm_DOY = mpl.colors.BoundaryNorm(bounds_DOY, cmap_DOY.N)
    smap_DOY = mpl.cm.ScalarMappable(norm=norm_DOY, cmap=cmap_DOY)
    # invisable plot
    s_DOY = ax.scatter(example_target_df.Urban, example_target_df.QH / example_target_df.kdown,
                       c=example_target_df.index.strftime('%j').astype(int),
                       cmap=cmap_DOY, norm=norm_DOY, zorder=0, alpha=0)
    cbar_DOY = fig.colorbar(mappable=s_DOY, orientation="vertical", format='%.0f', pad=-0.03)
    cbar_DOY.set_label('DOY')
    cbar_DOY.set_alpha(1)
    cbar_DOY.draw_all()


    # set up colourbar: radiation
    cmap_kdown = cm.get_cmap('gnuplot')
    bounds_kdown = np.linspace(smallest_kdown, largest_kdown, 256)
    norm_kdown = mpl.colors.BoundaryNorm(bounds_kdown, cmap_kdown.N)

    # invisable plot
    s_kdown = ax.scatter(example_target_df.Urban, example_target_df.QH / example_target_df.kdown, c=example_target_df.kdown,
                         cmap=cmap_kdown, norm=norm_kdown, zorder=0, alpha=0)

    cbar_kdown = fig.colorbar(mappable=s_kdown, orientation="vertical", format='%.0f', pad=0.01)
    cbar_kdown.set_label('$K_{\downarrow}$ (W m$^{-2}$)')

    cbar_kdown.set_alpha(1)
    cbar_kdown.draw_all()

    linestyle_dict = {'BCT_IMU': '-', 'SCT_SWT': '--', 'BTT_BCT': ':', 'IMU_BTT': '-.'}

    for path in path_dict:

        linestyle = linestyle_dict[path]

        df = path_dict[path]

        # subset df where kdown is bellow 100
        target_df = df.iloc[np.where(df.kdown >= 200)[0]][['QH', 'kdown', 'Urban']].dropna()

        # make sure df is in chronological order
        target_df = target_df.sort_index()

        # get individual days into groups
        groups = target_df.groupby([target_df.index.date])


        for i, group in groups:
            # set group's colour
            colour = smap_DOY.to_rgba(int(i.strftime('%j')))

            # set centre point (daily average)
            av_qh = group.QH.mean()
            av_kdown = group.kdown.mean()
            av_built = group.Urban.mean()

            # plot daily average
            ax.scatter(av_built, av_qh / av_kdown, c=av_kdown, cmap=cmap_kdown, norm=norm_kdown, zorder=3, marker='o',
                       edgecolor='k')

            for index, row in group.iterrows():
                x = [av_built, row.Urban]
                y = [av_qh / av_kdown, row.QH / row.kdown]
                ax.plot(x, y, c=colour, alpha=0.4, zorder=1, linestyle=linestyle)

            # each individual hour
            ax.scatter(group.Urban, group.QH / group.kdown, c=group.kdown, cmap=cmap_kdown, norm=norm_kdown,
                       zorder=2, marker='.', alpha=1)



    handles, labels = plt.gca().get_legend_handles_labels()

    for path in path_dict:

        line = Line2D([0], [0], label=path, color='k', linestyle=linestyle_dict[path])
        handles.extend([line])

    plt.legend(handles=handles)


    ax.set_xlabel('Built frac')
    ax.set_ylabel('QH/Kdn')

    plt.tight_layout()

    # plt.show()
    plt.savefig(save_path + 'all_paths' + '_built_fraction.png', bbox_inches='tight', dpi=300)

    print('end')







    print('end')



def plot_built_fraction_3(df, pair_id, save_path):
    """

    :param df:
    :return:
    """

    # subset df where kdown is bellow 100
    target_df = df.iloc[np.where(df.kdown >= 200)[0]][['QH', 'kdown', 'Urban']].dropna()

    # make sure df is in chronological order
    target_df = target_df.sort_index()

    # set up figure
    fig, ax = plt.subplots(figsize=(15, 8))

    # get individual days into groups
    groups = target_df.groupby([target_df.index.date])

    # set up colourbar: DOY
    smallest_doy = target_df.index.strftime('%j').astype(int).min()  # smallest DOY
    largest_doy = target_df.index.strftime('%j').astype(int).max()  # largest DOY
    # smallest_doy = 1  # smallest DOY
    # largest_doy = 366  # largest DOY

    cmap_DOY = cm.get_cmap('rainbow')
    bounds_DOY = np.linspace(smallest_doy, largest_doy, len(groups) + 1)
    norm_DOY = mpl.colors.BoundaryNorm(bounds_DOY, cmap_DOY.N)

    smap_DOY = mpl.cm.ScalarMappable(norm=norm_DOY, cmap=cmap_DOY)
    # invisable plot
    s_DOY = ax.scatter(target_df.Urban, target_df.QH / target_df.kdown, c=target_df.index.strftime('%j').astype(int),
                       cmap=cmap_DOY, norm=norm_DOY, zorder=0, alpha=0)
    cbar_DOY = fig.colorbar(mappable=s_DOY, orientation="vertical", format='%.0f', pad=-0.03)
    cbar_DOY.set_label('DOY')
    cbar_DOY.set_alpha(1)
    cbar_DOY.draw_all()

    # set up colourbar: radiation
    smallest_kdown = target_df.kdown.min()  # largest radiation value
    largest_kdown = target_df.kdown.max()  # smallest radiation value
    cmap_kdown = cm.get_cmap('gnuplot')
    bounds_kdown = np.linspace(smallest_kdown, largest_kdown, 256)
    norm_kdown = mpl.colors.BoundaryNorm(bounds_kdown, cmap_kdown.N)

    # invisable plot
    s_kdown = ax.scatter(target_df.Urban, target_df.QH / target_df.kdown, c=target_df.kdown,
                         cmap=cmap_kdown, norm=norm_kdown, zorder=0, alpha=0)

    cbar_kdown = fig.colorbar(mappable=s_kdown, orientation="vertical", format='%.0f', pad=0.01)
    cbar_kdown.set_label('$K_{\downarrow}$ (W m$^{-2}$)')

    cbar_kdown.set_alpha(1)
    cbar_kdown.draw_all()

    for i, group in groups:
        # set group's colour
        colour = smap_DOY.to_rgba(int(i.strftime('%j')))

        # set centre point (daily average)
        av_qh = group.QH.mean()
        av_kdown = group.kdown.mean()
        av_built = group.Urban.mean()

        # plot daily average
        ax.scatter(av_built, av_qh / av_kdown, c=av_kdown, cmap=cmap_kdown, norm=norm_kdown, zorder=3, marker='o',
                   edgecolor='k')

        for index, row in group.iterrows():
            x = [av_built, row.Urban]
            y = [av_qh / av_kdown, row.QH / row.kdown]
            ax.plot(x, y, c=colour, alpha=0.4, zorder=1)

        # each individual hour
        ax.scatter(group.Urban, group.QH / group.kdown, c=group.kdown, cmap=cmap_kdown, norm=norm_kdown,
                   zorder=2, marker='.', alpha=1)

    ax.set_xlabel('Built frac')
    ax.set_ylabel('QH/Kdn')

    plt.tight_layout()

    # plt.show()
    plt.savefig(save_path + pair_id + '_built_fraction.png', bbox_inches='tight', dpi=300)

    print('end')


def plot_built_fraction_2(df):
    """
    Scatter of hours AND day averages
    where data is only taken when kdn is above 200
    :param df:
    :return:
    """

    # subset df where kdown is bellow 100
    target_df = df.iloc[np.where(df.kdown >= 200)[0]][['QH', 'kdown', 'Urban']].dropna()

    # get individual days
    groups = target_df.groupby([target_df.index.date])

    qh_list = []
    kdwn_list = []
    urban_list = []

    for i, group in groups:
        av_qh = group.QH.mean()
        av_kdown = group.kdown.mean()
        av_built = group.Urban.mean()

        qh_list.append(av_qh)
        kdwn_list.append(av_kdown)
        urban_list.append(av_built)

    day_kdowns = np.array(kdwn_list)
    day_qhs = np.array(qh_list)

    fig, ax = plt.subplots(figsize=(7, 7))

    cmap = cm.get_cmap('rainbow')

    smallest_kdown = target_df.kdown.min()
    largest_kdown = target_df.kdown.max()

    bounds = np.linspace(smallest_kdown, largest_kdown, 256)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    s = ax.scatter(target_df.Urban, target_df.QH / target_df.kdown,
                   c=target_df.kdown, cmap=cmap, norm=norm, zorder=1, marker='.', label='Individual hour')

    ax.scatter(urban_list, day_qhs / day_kdowns, c=day_kdowns, cmap=cmap, norm=norm, zorder=2, marker='o',
               edgecolor='k', label='Day av')

    plt.legend()
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cbar = fig.colorbar(mappable=s, cax=cax, orientation="vertical", format='%.0f')
    cax.set_ylabel('$K_{\downarrow}$ (W m$^{-2}$)', rotation=270, labelpad=20)

    ax.set_xlabel('Built frac')
    ax.set_ylabel('QH/Kdn')

    print('end')


def plot_built_fraction_1(df):
    """
    # ToDo: rename these functions ocne one has been decided upon
    ONE POINT FOR EACH DAY
    HOURS JUST BETWEEN 10 AND TWO
    :return:
    """

    # values just between 10 and two - one point per day

    # get individual days
    groups = df.groupby([df.index.date])

    qh_list = []
    kdwn_list = []
    urban_list = []

    for i, group in groups:
        # take times between 10 and 2
        middle_of_day_df = group.loc[group.index.hour.isin([10, 11, 12, 13, 14])]

        av_qh = middle_of_day_df.QH.mean()
        av_kdown = middle_of_day_df.kdown.mean()
        av_built = middle_of_day_df.Urban.mean()

        qh_list.append(av_qh)
        kdwn_list.append(av_kdown)
        urban_list.append(av_built)

    kdown = np.array(kdwn_list)
    qh = np.array(qh_list)

    fig, ax = plt.subplots(figsize=(7, 7))
    cmap = cm.get_cmap('rainbow')

    smallest_kdown = kdown.min()

    largest_kdown = kdown.max()

    bounds = np.linspace(smallest_kdown, largest_kdown, len(qh) + 1)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    s = ax.scatter(urban_list, qh / kdown,
                   c=kdown, cmap=cmap, norm=norm, label='Clear Obs', s=80,
                   zorder=3)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cbar = fig.colorbar(mappable=s, cax=cax, orientation="vertical", format='%.0f')
    cax.set_ylabel('$K_{\downarrow}$ (W m$^{-2}$)', rotation=270, labelpad=20)

    ax.set_xlabel('Built frac')
    ax.set_ylabel('QH/kdn')

    plt.show()

    print('end')
