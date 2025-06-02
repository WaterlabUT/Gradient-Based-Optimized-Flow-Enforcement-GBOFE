"""
Implementation of the r.carve method.
"""
import numpy as np
from gbofe.algorithms.base_strategy import FlowEnforcementStrategy

class RCarveMethod(FlowEnforcementStrategy):
    """Implementation of the r.carve method for flow correction."""

    def apply(self, dem_data: np.ndarray, drainage_data: np.ndarray,
              resolution: float) -> np.ndarray:
        """
        Applies r.carve method by directly subtracting the gradient.

        Args:
            dem_data: DEM data
            drainage_data: Rasterized drainage data
            resolution: Raster resolution

        Returns:
            Corrected DEM using r.carve
        """
        corrected_dem = dem_data.copy()
        drainage_indices = self.get_drainage_indices(drainage_data)

        for x, y in drainage_indices:
            corrected_dem[x, y] = corrected_dem[x, y] - self.gradient

        return corrected_dem