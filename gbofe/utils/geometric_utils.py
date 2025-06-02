"""
Geometric utilities for DEM processing.
"""
import numpy as np
import rasterio
from rasterio.features import rasterize
import rasterio.enums
from tqdm import tqdm
from typing import Tuple
from gbofe.config import DIAGONAL_MULTIPLIER, PROGRESS_MESSAGES
from gbofe.utils.ui_helpers import animated_loading

def get_neighbors(matrix: np.ndarray, position: Tuple[int, int]) -> np.ndarray:
    """
    Gets neighboring values based on D8 algorithm.

    Args:
        matrix: Data matrix
        position: Tuple (row, column) of position

    Returns:
        Array with neighbor values and their coordinates
    """
    r, c = position
    neighbors = np.array([
        [matrix[r - 1, c], r - 1, c],  # North
        [matrix[r - 1, c + 1], r - 1, c + 1],  # Northeast
        [matrix[r, c + 1], r, c + 1],  # East
        [matrix[r + 1, c + 1], r + 1, c + 1],  # Southeast
        [matrix[r + 1, c], r + 1, c],  # South
        [matrix[r + 1, c - 1], r + 1, c - 1],  # Southwest
        [matrix[r, c - 1], r, c - 1],  # West
        [matrix[r - 1, c - 1], r - 1, c - 1]  # Northwest
    ])
    return neighbors

def get_slopes(elevation_neighbors: np.ndarray, elevation_cell: float,
               resolution: float) -> np.ndarray:
    """
    Calculates slope values based on elevations and resolution.

    Args:
        elevation_neighbors: Neighbor elevations
        elevation_cell: Current cell elevation
        resolution: Raster resolution

    Returns:
        Array of slope values
    """
    # Distances: cardinal = resolution, diagonal = resolution * sqrt(2)
    distances = np.where(
        np.array([0, 1, 2, 3, 4, 5, 6, 7]) % 2 == 0,
        resolution,
        resolution * DIAGONAL_MULTIPLIER
    )

    slope_values = (elevation_cell - elevation_neighbors) / distances
    return slope_values.reshape(-1, 1)

def get_factor(neighbor_index: int, resolution: float) -> float:
    """
    Calculates a distance factor based on neighbor index.

    Args:
        neighbor_index: Neighbor index (0-7)
        resolution: Raster resolution

    Returns:
        Distance factor
    """
    return resolution * (DIAGONAL_MULTIPLIER if neighbor_index % 2 != 0 else 1.0)

def rasterize_drainage(raster, vector, recursive: bool = False) -> np.ndarray:
    """
    Generates a drainage raster from a drainage shapefile.

    Args:
        raster: Base GeoDataRaster object
        vector: Drainage GeoDataVector object
        recursive: Whether to create drainage hierarchy

    Returns:
        Numpy array with rasterized drainage
    """
    animated_loading(PROGRESS_MESSAGES['rasterizing'])

    # Resolution assuming square pixels
    resolution = raster.get_resolution()

    # Reproject shapefile to base raster CRS if different
    if vector.crs != raster.crs:
        vector.reproject(raster.crs)

    # Calculate longitud and order values from GeoDataFrame
    vector.geo["length"] = vector.geo.geometry.length
    vector.geo = vector.geo.sort_values("length", ascending=True)

    # Generate a list of points (with numeric value) for each polyline
    shapes_list = []

    for idx, row in vector.geo.iterrows():
        geom = row.geometry

        # Check if geometry is LineString or MultiLineString
        if geom.geom_type == "LineString":
            lines = [geom]
        elif geom.geom_type == "MultiLineString":
            lines = list(geom.geoms)
        else:
            continue

        # Process each line component
        for line in lines:
            # Calcular número de puntos
            n_points = max(int(line.length / resolution) + 1, 2)
            distances = np.linspace(1, line.length, n_points)

            if recursive:
                for i, dist in enumerate(distances):
                    point = line.interpolate(dist)
                    shapes_list.append((point, int(i)))
            else:
                points = line.interpolate(distances)
                for point in points:
                    shapes_list.append((point, 1))

    # Rasterize points using a base raster extent, resolution and transform
    drainage_raster = rasterize(
        shapes=shapes_list,
        out_shape=(raster.height, raster.width),
        transform=raster.transform,
        fill=0,
        dtype=rasterio.int32,
        merge_alg=rasterio.enums.MergeAlg.replace
    )

    if recursive:
        return _create_drainage_hierarchy(drainage_raster)
    else:
        return drainage_raster

def _create_drainage_hierarchy(drainage_raster: np.ndarray) -> np.ndarray:
    """Creates drainage hierarchy for recursive processing."""
    raster_val = drainage_raster.copy()
    raster_mod = drainage_raster.copy()
    unique_values = np.unique(drainage_raster)

    for value in tqdm(unique_values, desc=PROGRESS_MESSAGES['hierarchy']):
        if value == 0:
            continue

        indices = np.argwhere(drainage_raster == value)

        for index in indices:
            neighbors_val = get_neighbors(raster_val, index)
            neighbors_mod = get_neighbors(raster_mod, index)

            if max(neighbors_val[:, 0]) > 0:
                active_neighbors = neighbors_mod[neighbors_mod[:, 0] > 0]
                if len(active_neighbors) <= 2:
                    raster_mod[index[0], index[1]] = max(neighbors_mod[:, 0]) + 1
                else:
                    raster_mod[index[0], index[1]] = max(neighbors_mod[:, 0]) + 2
                raster_val[index[0], index[1]] = 0
            else:
                raster_mod[index[0], index[1]] = min(neighbors_mod[:, 0]) + 1
                raster_val[index[0], index[1]] = 0

    return raster_mod