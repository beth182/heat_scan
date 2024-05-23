import numpy as np
import xarray as xr

from matplotlib.patches import Path, PathPatch
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import matplotlib

matplotlib.use('TkAgg')
matplotlib.rcParams.update({'font.size': 15})

from heat_scan.tools import constants


def white_ocean(ax, countries=False):
    """
    Source: https://stackoverflow.com/questions/48620803/fill-oceans-in-basemap
    :param ax:
    :return:
    """

    # ToDo: add to docstring here

    m = Basemap(ax=ax)
    m.drawcoastlines()
    if countries:
        m.drawcountries()

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
    deg_c.plot(ax=ax, cbar_kwargs={"location": "bottom", 'pad': -0.2})
    white_ocean(ax=ax)

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    # ToDo: add model to dave string here

    plt.savefig(save_path + '/plots/' + 'tasmax_in_' + str(year) + '_time_' + str(int(time)) + '.png',
                bbox_inches='tight', dpi=300)


def plt_count_over_threshold(ds, threshold, year, save_path, region=False, **kwargs):
    """

    :return:
    """
    # ToDo: add to docstring here

    # ToDo: repreat here: moved to fun in LCR
    high_vals = xr.where(ds > threshold + constants.convert_kelvin, 1, 0)  # set all temps over threshold = 1; others to 0
    summed_vals = high_vals.sum(dim='time')

    # replace any 0 values with nan
    summed_vals = summed_vals.where(summed_vals > 0)

    if type(year) == list:
        summed_vals = summed_vals / len(year)

    # fig, (ax, cax) = plt.subplots(nrows=2, figsize=(15, 12), gridspec_kw={"height_ratios":[1, 0.05]})
    fig, ax = plt.subplots(1, figsize=(15, 12))

    # set colourbar
    cmap = matplotlib.cm.plasma
    # make nan black
    cmap.set_bad('black', 1.)

    # ToDo: make variable flexable
    im = summed_vals.tasmax.plot(ax=ax, cmap=cmap, add_colorbar=False,
                                 vmin=1, vmax=365)
    white_ocean(ax=ax, countries=True)

    cax = inset_axes(ax,
                     width="100%",
                     height="5%",
                     loc='lower center',
                     borderpad=-2.5
                     )

    fig.colorbar(im, cax=cax, orientation="horizontal", label='# of days')

    if type(year) == list:
        year_label = str(year[0]) + '_to_' + str(year[-1])
    else:
        assert type(year) == int
        year_label = str(year)

    ax.set_title(year_label)

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    if not 'source_id' in kwargs.keys():
        kwargs['source_id'] = 'GFDL-ESM4'

    if region != False:

        assert region in constants.coord_contraints.keys()

        ax.set_xlim(constants.coord_contraints[region]['BL']['x'], constants.coord_contraints[region]['BR']['x'])
        ax.set_ylim(constants.coord_contraints[region]['BL']['y'], constants.coord_contraints[region]['TL']['y'])

        plt.savefig(save_path + region + '_' + kwargs['source_id'] + '_days_over_' + str(threshold) + '_in_' + year_label.replace('_', ' ') + '.png', bbox_inches='tight', dpi=300)

    else:

        plt.savefig(
            save_path + 'global_' + kwargs['source_id'] + '_days_over_' + str(threshold) + '_in_' + year_label.replace('_', ' ') + '.png', bbox_inches='tight', dpi=300)

    print('end')
