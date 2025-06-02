"""
Implementation of gbofe (Gradient-Based Optimized Flow Enforcement) method.
"""
import numpy as np
from tqdm import tqdm
from gbofe.algorithms.base_strategy import FlowEnforcementStrategy
from gbofe.utils.geometric_utils import get_neighbors, get_slopes, get_factor
from gbofe.config import FLOW_ACCUMULATION_THRESHOLD, PROGRESS_MESSAGES

class GBOFEMethod(FlowEnforcementStrategy):
    """Implementation of gbofe method."""

    def apply(self, dem_data: np.ndarray, drainage_data: np.ndarray,
              resolution: float) -> np.ndarray:
        """
        Applies the gbofe method with gradient-based optimization.

        Args:
            dem_data: DEM data
            drainage_data: Rasterized drainage data
            resolution: Raster resolution

        Returns:
            Corrected DEM using gbofe
        """
        corrected_dem = dem_data.copy()
        drainage_copy = drainage_data.copy()

        # Get unique accumulated flow values
        flow_values = drainage_data.ravel()
        valid_flow_values = flow_values[flow_values >= FLOW_ACCUMULATION_THRESHOLD]
        unique_values = np.unique(valid_flow_values)

        # Process each flow value
        for flow_value in tqdm(unique_values, desc=PROGRESS_MESSAGES['processing']):
            indices = np.argwhere(drainage_copy == flow_value)

            for index in indices:
                self._process_cell(
                    corrected_dem, drainage_copy, index,
                    flow_value, resolution
                )

        return corrected_dem

    def _process_cell(self, dem_data: np.ndarray, drainage_data: np.ndarray,
                      index: np.ndarray, current_flow: int, resolution: float) -> None:
        """Processes an individual cell using the gbofe algorithm."""

        # Get neighbor values
        elevation_neighbors = get_neighbors(dem_data, index)
        flow_neighbors = get_neighbors(drainage_data, index)

        current_elevation = float(dem_data[index[0], index[1]])

        if np.max(flow_neighbors[:, 0]) == 0:
            drainage_data[index[0], index[1]] = 0
            return

        # Calculate slopes
        slopes = get_slopes(elevation_neighbors[:, 0], current_elevation, resolution)

        # Create combined matrix: [elevation, row, column, slope, accumulated_flow]
        combined_matrix = np.concatenate([
            elevation_neighbors,
            slopes,
            flow_neighbors[:, 0].reshape(-1, 1)
        ], axis=1)

        # Remove row where flow equals current node
        combined_matrix = combined_matrix[combined_matrix[:, 4] != current_flow]

        # Filter superior values
        flow_column = combined_matrix[:, 4]
        superior_values = flow_column[flow_column > current_flow]

        if superior_values.size > 0:
            min_superior = superior_values.min()
            combined_matrix = combined_matrix[
                (flow_column <= current_flow) | (flow_column == min_superior)
                ]

        # Find neighbors with higher accumulated flow
        max_flow = np.max(combined_matrix[:, 4])
        max_flow_indices = np.argwhere(combined_matrix[:, 4] == max_flow)

        # Verify positive slope
        max_slope = np.max(combined_matrix[:, 3])

        if max_slope <= 0:
            # No positive slope: equalize elevation
            for idx in max_flow_indices:
                neighbor_idx = idx[0]
                dem_data[
                    int(combined_matrix[neighbor_idx, 1]),
                    int(combined_matrix[neighbor_idx, 2])
                ] = current_elevation
            drainage_data[index[0], index[1]] = 0
        else:
            # With positive slope: apply correction
            self._apply_gbofe_correction(
                dem_data, drainage_data, combined_matrix,
                max_flow_indices, max_slope, current_elevation,
                index, resolution
            )

    def _apply_gbofe_correction(self, dem_data: np.ndarray, drainage_data: np.ndarray,
                                combined_matrix: np.ndarray, max_flow_indices: np.ndarray,
                                max_slope: float, current_elevation: float,
                                current_index: np.ndarray, resolution: float) -> None:
        """Applies the specific gbofe correction."""

        max_slope_indices = np.argwhere(combined_matrix[:, 3] == max_slope)

        if len(max_flow_indices) == 1:
            # Case 1: Only one neighbor with maximum flow
            neighbor_idx = max_flow_indices[0, 0]
            if (combined_matrix[neighbor_idx, 3] != max_slope) or (len(max_slope_indices) > 1):
                corrected_slope = max_slope + self.gradient
                factor = get_factor(neighbor_idx, resolution)
                dem_data[
                    int(combined_matrix[neighbor_idx, 1]),
                    int(combined_matrix[neighbor_idx, 2])
                ] = current_elevation - corrected_slope * factor
                drainage_data[current_index[0], current_index[1]] = 0
        else:
            # Case 2: Multiple neighbors with maximum flow
            max_flow_slopes = combined_matrix[max_flow_indices[:, 0], 3]
            has_max_slope = np.any(np.isin(max_flow_slopes, combined_matrix[max_slope_indices, 3]))

            if (not has_max_slope) or (len(max_flow_indices) < len(max_slope_indices)):
                corrected_slope = max_slope + self.gradient
                for idx in max_flow_indices:
                    neighbor_idx = idx[0]
                    factor = get_factor(neighbor_idx, resolution)
                    dem_data[
                        int(combined_matrix[neighbor_idx, 1]),
                        int(combined_matrix[neighbor_idx, 2])
                    ] = current_elevation - corrected_slope * factor
                drainage_data[current_index[0], current_index[1]] = 0