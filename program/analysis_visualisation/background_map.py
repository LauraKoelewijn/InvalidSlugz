import matplotlib.pyplot as plt # type: ignore
import geopandas as gpd # type: ignore
import contextily as cx # type: ignore

def make_map() -> None:
    # load map description set to nl
    df = gpd.read_file('data/geo_data/nl_regions.geojson')

    # transform data into a structure contextily can read and set size, visibility and color
    df_wm = df.to_crs(epsg=3857)
    ax = df_wm.plot(figsize=(10, 10), alpha=0.3, edgecolor='k')

    # plot basemap and regions in the same plot
    cx.add_basemap(ax)

    # hide axes
    ax = plt.gca()
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)

    # save figure to map_nl
    plt.savefig('data/background/map_nl.png')

    # show plot
    plt.show()