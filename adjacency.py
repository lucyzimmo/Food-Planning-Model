"""
This script generates the adjacency relationships between census tracts in Imperial County, California."""
import geopandas as gpd
import json


# Load the geospatial data of California Census Tracts
shapefile_path = 'data/tl_rd22_06_tract/tl_rd22_06_tract.shp'  
gdf = gpd.read_file(shapefile_path)
gdf_imperial = gdf[gdf['COUNTYFP'] == '025']  # Filter for Imperial County
gdf = gdf_imperial[['GEOID', 'geometry']]
adjacency = {}
for idx, tract in gdf.iterrows():
    # Find neighboring tracts that share a boundary with the current tract
    neighbors = gdf[gdf.geometry.touches(tract.geometry)]['GEOID'].tolist()
    adjacency[tract['GEOID']] = neighbors

# Print adjacency results
for tract, neighbors in adjacency.items():
    print(f"Census Tract {tract} has neighbors: {neighbors}")


# Save adjacency relationships for later use
adjacency_file_path = 'adjacency.json'
with open(adjacency_file_path, 'w') as f:
    json.dump(adjacency, f)

print(f"Adjacency relationships saved to: {adjacency_file_path}")

