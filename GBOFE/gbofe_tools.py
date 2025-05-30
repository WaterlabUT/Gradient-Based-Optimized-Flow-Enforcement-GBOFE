# import libraries
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.features import rasterize
import rasterio.enums
from tqdm import tqdm
import time
import sys

# ========================================================================
# Get neighboring values based on the D8 algorithm
# ========================================================================
def get_neighbors(matrix, rc):
    r, c = rc
    neighbors = np.array([
        [matrix[r - 1, c], r - 1, c],
        [matrix[r - 1, c + 1], r - 1, c + 1],
        [matrix[r, c + 1], r, c + 1],
        [matrix[r + 1, c + 1], r + 1, c + 1],
        [matrix[r + 1, c], r + 1, c],
        [matrix[r + 1, c - 1], r + 1, c - 1],
        [matrix[r, c - 1], r, c - 1],
        [matrix[r - 1, c - 1], r - 1, c - 1]
    ])
    return neighbors

# ========================================================================
# Calculate slope values based on elevation values and resolution
# ========================================================================
def get_slopes(elevation_neighbors, elevation_cell, resolution):
    distances = np.where(np.array([0, 1, 2, 3, 4, 5, 6, 7]) % 2 == 0,
                          resolution,
                          resolution * np.sqrt(2))
    slope_values = (elevation_cell - elevation_neighbors) / distances
    return slope_values.reshape(-1, 1)

# ========================================================================
# Calculate factor values based on index and resolution
# ========================================================================
def get_factor(index_neighbor, resolution):
    return resolution * (np.sqrt(2) if index_neighbor % 2 != 0 else 1.0)

# ========================================================================
# Animate loading messages for the user during processing
# ========================================================================
def animated_loading(message):
    for _ in range(3):
        for m in ['', '.', '..', '...']:
            sys.stdout.write(f'\r{message}' + m)
            sys.stdout.flush()
            time.sleep(0.5)
    print()

# ========================================================================
# Generate a drainage raster from a drainage shapefile
# ========================================================================
def rasterize_drainage(path_dem, path_drainage, path_out, recursive=False):
    animated_loading('Export to raster drainage shapefile')

    # Read the DEM to get an extent, resolution, CRS and array
    with rasterio.open(path_dem) as base:
        base_transform = base.transform
        base_width = base.width
        base_height = base.height
        base_crs = base.crs
        # Assuming square pixels, resolution is extracted from 'a'
        res = abs(base_transform.a)

    # Read drainage shapefile
    gdf = gpd.read_file(path_drainage)

    # Reproject shapefile to base raster CRS if different
    if gdf.crs != base_crs:
        gdf = gdf.to_crs(base_crs)

    # Calculate the length of each record and sort GeoDataFrame from smallest to largest
    gdf["length"] = gdf.geometry.length
    gdf = gdf.sort_values("length", ascending=True)
    
    # Generate a list of points (with numeric value) for each polyline
    shapes_list = []

    # Iterate each record in the shapefile
    for idx, row in gdf.iterrows():
        geom = row.geometry
        # Check if geometry is LineString or MultiLineString
        if geom.geom_type == "LineString":
            lineas = [geom]
        elif geom.geom_type == "MultiLineString":
            lineas = list(geom.geoms)
        else:
            continue  # Other geometries are omitted

        # Process each line component
        for linea in lineas:
            # Calculate the number of points based over line length and base raster resolution
            n_puntos = max(int(linea.length / res) + 1, 2)
            # Create an array of equidistant points
            distancias = np.linspace(1, linea.length, n_puntos)
            # If recursive, add a point for each order value
            if recursive:
                for i, dist in enumerate(distancias):
                    punto = linea.interpolate(dist)
                    # Add a point and its order value to the list
                    shapes_list.append((punto, int(i)))
            # Otherwise, add a point for each equidistant point in the line
            else:
                puntos = linea.interpolate(distancias)
                for punto in puntos:
                    shapes_list.append((punto, 1))

    # 6. Rasterize points using a base raster extent, resolution and transform
    raster_drenaje = rasterize(
        shapes=shapes_list,
        out_shape=(base_height, base_width),
        transform=base_transform,
        fill=0,  # Value for pixels without data
        dtype=rasterio.int32,
        merge_alg=rasterio.enums.MergeAlg.replace  # In case of overlap, replace
    )

    # If recursive, modify the raster values to create a drainage hierarchical
    if recursive:
        raster_drenaje_val = raster_drenaje.copy()
        raster_drenaje_mod = raster_drenaje.copy()
        # Get unique values in the raster
        values_drenaje = np.unique(raster_drenaje)
        
        # Iterate through each value in the raster
        for k in tqdm(range(len(values_drenaje)), desc="Creating drainage hierarchy"):
            value = values_drenaje[k]

            if value == 0:
                continue
            # Find indices of pixels with the current value in the raster
            ind = np.argwhere(raster_drenaje == value)
            # Iterate through each pixel index in the list of indices
            for n in range(len(ind)):
                m = ind[n]
                # Get neighboring values based on the D8 algorithm
                nb_drenaje_val = get_neighbors(raster_drenaje_val, m)
                nb_drenaje_mod = get_neighbors(raster_drenaje_mod, m)
                # Modify the value based on the number of neighboring values
                if max(nb_drenaje_val[:, 0]) > 0:
                    if len(nb_drenaje_mod[nb_drenaje_mod[:, 0] > 0]) <= 2:
                        raster_drenaje_mod[m[0], m[1]] = max(nb_drenaje_mod[:, 0])+1
                        raster_drenaje_val[m[0], m[1]] = 0
                    else:
                        raster_drenaje_mod[m[0], m[1]] = max(nb_drenaje_mod[:, 0]) + 2
                        raster_drenaje_val[m[0], m[1]] = 0
                else:
                    raster_drenaje_mod[m[0], m[1]] = min(nb_drenaje_mod[:, 0]) + 1
                    raster_drenaje_val[m[0], m[1]] = 0

        # Export the resulting raster to a TIFF (.tif) file
        with rasterio.open(
            path_out, "w",
            driver="GTiff",
            height=base_height,
            width=base_width,
            count=1,
            dtype=rasterio.int32,
            crs=base_crs,
            transform=base_transform
        ) as dst:
            dst.write(raster_drenaje_mod, 1)
        print("Raster created and exported successfully")

    # Otherwise, export the raster as it is
    else:
        # Export the resulting raster to a TIFF (.tif) file
        with rasterio.open(
                path_out, "w",
                driver="GTiff",
                height=base_height,
                width=base_width,
                count=1,
                dtype=rasterio.int32,
                crs=base_crs,
                transform=base_transform
        ) as dst:
            dst.write(raster_drenaje, 1)
        print("Raster created and exported successfully")

a = r"D:\Universidad del Tolima\Artículos Científicos\Burn_Stream\DEM_Original\fabdem_clip.tif"
b = r"D:\Universidad del Tolima\Artículos Científicos\Burn_Stream\Shapes\drainage.shp"
o = r"D:\Universidad del Tolima\Artículos Científicos\Burn_Stream\test_new_recursive.tif"

rasterize_drainage(a, b, o, recursive=True)

# path_dem = r"D:\Universidad del Tolima\Artículos Científicos\Burn_Stream\DEM_Original\fabdem_clip.tif"
# path_drainage = r"D:\Universidad del Tolima\Artículos Científicos\Burn_Stream\Shapes\drainage.shp"
# path_out = r"D:\Universidad del Tolima\Artículos Científicos\Burn_Stream\test_new.tif"