import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as cx

df = gpd.read_file('data/holland_regions.geojson')

df_wm = df.to_crs(epsg=3857)
ax = df_wm.plot(figsize=(10, 10), alpha=0.3, edgecolor='k')
cx.add_basemap(ax)

ax = plt.gca()
ax.get_yaxis().set_visible(False)
ax.get_xaxis().set_visible(False)

plt.savefig('data/map_1.png')

plt.show()