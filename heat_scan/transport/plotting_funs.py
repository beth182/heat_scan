import numpy as np
import xarray as xr

from matplotlib.patches import Path, PathPatch
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

import matplotlib

matplotlib.use('TkAgg')
matplotlib.rcParams.update({'font.size': 15})

from heat_scan.tools import constants


def white_ocean(ax):
    """
    Source: https://stackoverflow.com/questions/48620803/fill-oceans-in-basemap
    :param ax:
    :return:
    """

    # ToDo: add to docstring here

    m = Basemap()
    m.drawcoastlines()

    # making the ocean white
    # getting the limits of the map:
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    map_edges = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])
    # getting all polygons used to draw the coastlines of the map
    polys = [p.boundary for p in m.landpolygons]
    # combining with map edges
    polys = [map_edges] + polys[:]
    # creating a PathPatch
    codes = [
        [Path.MOVETO] + [Path.LINETO for p in p[1:]]
        for p in polys
    ]
    polys_lin = [v for p in polys for v in p]
    codes_lin = [c for cs in codes for c in cs]
    path = Path(polys_lin, codes_lin)
    patch = PathPatch(path, facecolor='white', lw=0)
    # masking the data:
    ax.add_patch(patch)

    return ax


def plt_straight_variable(ds, year, save_path, time=0):
    """
    Plot a given variable at a time
    :return:
    """
    # ToDo: add to docstring here

    # ToDo: make time changable in a way that makes sense

    fig, ax = plt.subplots(1, figsize=(15, 12))
    # ToDo: add check to see if variable is a temperature in kelvin before this step?
    # ToDo: make variable flexable
    deg_c = ds.tasmax.isel(time=time) - constants.convert_kelvin
    deg_c.plot(ax=ax)
    white_ocean(ax=ax)

    plt.savefig(save_path + '/plots/' + 'tasmax_in_' + str(year) + '.png', bbox_inches='tight', dpi=300)


def plt_count_over_threshold(ds, threshold, year, save_path):
    """

    :return:
    """
    # ToDo: add to docstring here

    high_vals = xr.where(ds > threshold, 1, 0)  # set all temps over threshold = 1; others to 0
    summed_vals = high_vals.sum(dim='time')

    # replace any 0 values with nan
    summed_vals = summed_vals.where(summed_vals > 0)

    fig, ax = plt.subplots(1, figsize=(15, 12))

    # set colourbar
    cmap = matplotlib.cm.plasma
    # make nan black
    cmap.set_bad('black', 1.)

    # ToDo: make variable flexable
    summed_vals.tasmax.plot(ax=ax, cmap=cmap, cbar_kwargs={'label': "# of days", "location": "bottom", 'pad': -0.2}, vmin=1, vmax=365)
    white_ocean(ax=ax)

    plt.title('Number of days in ' + str(year) + ' where Daily Maximum Near-Surface Air Temperature > ' + str(
        threshold - constants.convert_kelvin) + '$^{\circ}$C')

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    plt.savefig(save_path + '/plots/' + 'days_over_' + str(int(threshold - constants.convert_kelvin)) + '_in_' + str(year) + '.png', bbox_inches='tight', dpi=300)

    print('end')
