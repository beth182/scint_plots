import matplotlib.pyplot as plt
from scintools.utils import path_weight
from scintools.utils import constant


def transect_plot(pt, pw_fun=None):
    """Plot the transect, beam and (optional) path weighting function."""

    fig, ax = plt.subplots(constrained_layout=True)

    # plot the path weighting curve
    if pw_fun is not None:
        path_weight_df = path_weight.path_weight(
            fx=pw_fun, n_x=pt.gdf.shape[0])
        ax2 = ax.twinx()
        lns1 = ax2.plot(
            pt.gdf.index * pt.point_res,
            path_weight_df["path_weight"], color="grey", linestyle='--',
            label='Path weighting function')

        ax.spines['right'].set_color('grey')
        ax2.spines['right'].set_color('grey')
        ax2.set_ylabel("Path Weighting")
        ax2.yaxis.label.set_color('grey')
        ax2.tick_params(axis='y', colors='grey')

    # plot the heights
    # ax.plot(self.gdf.index * self.point_res, self.gdf["z_asl_mean"], color='blue')
    # give the variation of building height at each point as width of line
    # ax.fill_between(self.gdf.index * self.point_res, self.gdf["z_asl_min"],
    #                 self.gdf["z_asl_max"], color='blue')

    lns2 = ax.plot(pt.gdf.index * pt.point_res, pt.gdf["z_asl_max"], color='blue', label='Building heights')

    # plot the path
    lns3 = ax.plot(
        pt.gdf.path_length_m, pt.gdf["path_height_asl"], color='red',
        label='LAS path')

    ax.set_xlabel('Horizontal distance (m)')
    ax.set_ylabel('Height (m asl)')

    # add effective beam height label
    ebh = pt.effective_beam_height()
    plt.text(0.7, 0.83, '$z_{fb}$ = %d.2 m agl' % ebh,
             transform=ax.transAxes)

    # added these three lines
    lns = lns2 + lns3
    if pw_fun:
        lns = lns + lns1
    labs = [ln.get_label() for ln in lns]
    ax.legend(lns, labs, frameon=False, prop={'size': 8})

    return (fig, ax)
