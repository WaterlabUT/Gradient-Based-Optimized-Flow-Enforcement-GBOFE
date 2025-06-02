"""
Implementation of normal and modified excavation methods.
"""
import numpy as np
from tqdm import tqdm
from gbofe.algorithms.base_strategy import FlowEnforcementStrategy
from gbofe.utils.geometric_utils import get_neighbors
from gbofe.config import FLOW_ACCUMULATION_THRESHOLD, PROGRESS_MESSAGES

class NormalExcavationMethod(FlowEnforcementStrategy):
    """Implementation of the normalized excavation method."""

    def apply(self, dem_data: np.ndarray, drainage_data: np.ndarray,
              resolution: float) -> np.ndarray:
        """
        Applies the normalized excavation method based on minimum neighbors.

        Args:
            dem_data: DEM data
            drainage_data: Rasterized drainage data
            resolution: Raster resolution

        Returns:
            Corrected DEM using normal excavation
        """
        corrected_dem = dem_data.copy()
        drainage_indices = self.get_drainage_indices(drainage_data)

        new_elevations = []
        for index in drainage_indices:
            neighbors = get_neighbors(corrected_dem, index)
            min_neighbor = min(neighbors[:, 0])
            new_elevation = min_neighbor - self.gradient
            new_elevations.append(new_elevation)

        # Apply new elevations
        for i, (x, y) in enumerate(drainage_indices):
            corrected_dem[x, y] = new_elevations[i]

        return corrected_dem

class NormalExcavationModifiedMethod(FlowEnforcementStrategy):
    """Implementation of the modified normalized excavation method."""

    def apply(self, dem_data: np.ndarray, drainage_data: np.ndarray,
              resolution: float) -> np.ndarray:
        """
        Applies the modified normalized excavation method processing by flow values.

        Args:
            dem_data: DEM data
            drainage_data: Rasterized drainage data  
            resolution: Raster resolution

        Returns:
            Corrected DEM using modified normal excavation
        """
        corrected_dem = dem_data.copy()

        # Obtener valores únicos de flujo acumulado
        flow_values = drainage_data.ravel()
        valid_flow_values = flow_values[flow_values >= FLOW_ACCUMULATION_THRESHOLD]
        unique_values = np.unique(valid_flow_values)

        # Process flow values
        for flow_value in tqdm(unique_values, desc=PROGRESS_MESSAGES['processing']):
            indices = np.argwhere(drainage_data == flow_value)

            for index in indices:
                neighbors = get_neighbors(corrected_dem, index)
                min_neighbor = min(neighbors[:, 0])
                corrected_dem[index[0], index[1]] = min_neighbor - self.gradient

        return corrected_dem