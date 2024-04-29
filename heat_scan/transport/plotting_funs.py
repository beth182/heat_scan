import numpy as np
import xarray as xr

from matplotlib.patches import Path, PathPatch
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

import matplotlib

matplotlib.use('TkAgg')

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


def plt_straight_variable(ds, time=0):
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


def plt_count_over_threshold(ds, threshold):
    """

    :return:
    """
    # ToDo: add to docstring here

    high_vals = xr.where(ds > threshold, 1, 0)  # set all temps over threshold = 1; others to 0
    summed_vals = high_vals.sum(dim='time')

    fig, ax = plt.subplots(1, figsize=(15, 12))
    # ToDo: make variable flexable
    summed_vals.tasmax.plot(ax=ax, cmap='gnuplot')
    white_ocean(ax=ax)
