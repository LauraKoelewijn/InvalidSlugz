import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as cx

# load map description set to holland or nl
df = gpd.read_file('data/holland_regions.geojson')

# transform data into a structure contextily can read and set size, visibility and color
df_wm = df.to_crs(epsg=3857)
ax = df_wm.plot(figsize=(10, 10), alpha=0.3, edgecolor='k')

# plot basemap and regions in the same plot
cx.add_basemap(ax)

# hide axes
ax = plt.gca()
ax.get_yaxis().set_visible(False)
ax.get_xaxis().set_visible(False)

# save figure to map_holland or map_nl
plt.savefig('data/map_holland.png')

# show plot
plt.show()