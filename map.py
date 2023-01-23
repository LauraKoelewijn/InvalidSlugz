import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as cx

df = gpd.read_file('data/nl_regions.geojson')

df_wm = df.to_crs(epsg=3857)
ax = df_wm.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
cx.add_basemap(ax)

# # loading file of boarders of Holland
# df_places = gpd.read_file('data/holland_regions.geojson')

# # looping through regions in the data file and plotting them in a matplotlib graph
# for polygon in df_places['geometry']:
#     x,y = polygon.exterior.xy
#     plt.plot(x,y)

plt.show()