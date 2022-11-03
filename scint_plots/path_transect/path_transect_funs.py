import tempfile
import rasterio
from os import path
import warnings
import rasterstats
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import integrate

mpl.rcParams.update({'font.size': 13})

from scintools.utils import path_weight
from scintools.utils import constant


class ScintillometerTransect:
    """An object that represents a ScintillometerPair transect."""

    def __init__(self, path_transect_gdf, sample_area, point_res, dsm_file):
        self.gdf = path_transect_gdf
        self.sample_area = sample_area
        self.point_res = point_res
        self.dsm_file = dsm_file

    def effective_beam_height(self, height_stat="mean", pw_fun=path_weight.bessel_approx):
        """
        Calculate effective beam height above ground level.

        Across the path length, the path height above ground is weighted and
        integrated. Here the influences of stability are assumed negligible.

        Parameters
        ----------
        height_stat
           One of "min", "mean", "max" of ScintillometerTransect heights
        pw_fun
           Path weighting function
        Returns
        -------
        float
            Effective beam height above ground level (m)
        """
        height_stat_str = constant.height_stat_str + height_stat + '_bdsm'
        path_weight_df = path_weight.path_weight(fx=pw_fun, n_x=self.gdf.shape[0])

        path_height_agl = self.gdf["path_height_asl"] - self.gdf[height_stat_str]
        path_height_agl[path_height_agl < 0] = 0
        path_height_weighted_integrated = integrate.trapz(
            path_height_agl * path_weight_df["path_weight"])
        z_eff = (path_height_weighted_integrated /
                 integrate.trapz(path_weight_df["path_distance"]))

        return z_eff


def path_transect(pair, dsm_file, dem_file, point_res):
    """Return a ScintillometerTransect from a ScintillometerPair.

    Description:todo

    Parameters
    ----------
    dsm_file : str
        Digital surface model file name, used to extract heights.
    dem_file : str
            Digital elevation model file name, used to extract terrain heights
    point_res : int or float
        Distance between points along the transect.

    Returns
    -------
    ScintillometerTransect
        DESCRIPTION:todo.

    """
    src = rasterio.open(dsm_file)
    src_dem = rasterio.open(dem_file)

    # check that dem and dsm have the same crs
    assert src.crs == src_dem.crs

    self = pair.to_crs(src.crs)
    temp_dir = tempfile.TemporaryDirectory()
    path_points_df = self.path_points(point_res)
    path_buffer_df = path_points_df.buffer(
        point_res / 2).reset_index(drop=True)
    shp_filename_tmp = path.join(temp_dir.name, "circle_path")
    path_buffer_df.to_file(shp_filename_tmp)

    warnings.filterwarnings("ignore")

    zonal_stats_array = rasterstats.zonal_stats(shp_filename_tmp, dsm_file, all_touched=True)

    zonal_stats_array_dem = rasterstats.zonal_stats(shp_filename_tmp, dem_file, all_touched=True)

    warnings.filterwarnings("default")

    zonal_stats_df_bdsm = pd.DataFrame(zonal_stats_array)
    zonal_stats_df_bdsm.columns = zonal_stats_df_bdsm.columns + '_bdsm'

    zonal_stats_df_dem = pd.DataFrame(zonal_stats_array_dem)
    zonal_stats_df_dem.columns = zonal_stats_df_dem.columns + '_dem'

    zonal_stats_df = pd.concat([zonal_stats_df_bdsm, zonal_stats_df_dem], axis=1)
    zonal_stats_df.columns = constant.height_stat_str + zonal_stats_df.columns

    temp_dir.cleanup()

    path_transect = pd.concat([path_points_df.reset_index(drop=True), zonal_stats_df], axis=1)

    return ScintillometerTransect(path_transect, path_buffer_df, point_res, dsm_file)


def transect_plot(pt, pw_fun=None):
    """Plot the transect, beam and (optional) path weighting function."""

    fig, ax = plt.subplots(figsize=(10, 7))

    # plot the path weighting curve
    if pw_fun is not None:
        path_weight_df = path_weight.path_weight(
            fx=pw_fun, n_x=pt.gdf.shape[0])
        ax2 = ax.twinx()
        pwf_line = ax2.plot(
            pt.gdf.index * pt.point_res,
            path_weight_df["path_weight"], color="blue", linestyle='--',
            label='Path weighting function')

        ax.spines['right'].set_color('grey')
        ax2.spines['right'].set_color('grey')
        ax2.set_ylabel("Path Weighting")
        ax2.yaxis.label.set_color('grey')
        ax2.tick_params(axis='y', colors='grey')

    bld_line = ax.plot(pt.gdf.index * pt.point_res, pt.gdf["z_asl_max_bdsm"], color='dimgrey', label='Building heights')
    ground_line = ax.plot(pt.gdf.index * pt.point_res, pt.gdf["z_asl_max_dem"], color='sienna', label='Ground height')

    ax.fill_between(pt.gdf.index * pt.point_res, pt.gdf["z_asl_max_bdsm"], pt.gdf["z_asl_max_dem"], color='grey', alpha=0.5)
    ax.fill_between(pt.gdf.index * pt.point_res, 0, pt.gdf["z_asl_max_dem"], color='sienna', alpha=0.5)

    # plot the path
    path_line = ax.plot(
        pt.gdf.path_length_m, pt.gdf["path_height_asl"], color='red',
        label='LAS path')

    ax.set_xlabel('Horizontal distance (m)')
    ax.set_ylabel('Height (m asl)')

    # add effective beam height label
    ebh = pt.effective_beam_height()
    plt.text(0.7, 0.75, '$z_{fb}$ = %d.2 m agl' % ebh,
             transform=ax.transAxes)

    # added these three lines
    lns = bld_line + ground_line + path_line

    if pw_fun:
        lns = lns + pwf_line
    labs = [ln.get_label() for ln in lns]
    ax.legend(lns, labs, frameon=False)

    plt.show()
    print('end')

