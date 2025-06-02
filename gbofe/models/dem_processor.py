"""
Main processor for DEM correction.
"""
import numpy as np
from typing import Tuple, Optional
from gbofe.models.geo_data import GeoDataRaster, GeoDataVector
from gbofe.algorithms.base_strategy import FlowEnforcementStrategy
from gbofe.utils.geometric_utils import rasterize_drainage
from gbofe.exceptions import DEMProcessingError
from gbofe.config import PROGRESS_MESSAGES

class DEMProcessor:
    """Main processor for DEM flow correction."""

    def __init__(self, dem_raster: GeoDataRaster, drainage_vector: GeoDataVector):
        self.dem_raster = dem_raster
        self.drainage_vector = drainage_vector
        self._processed_data: Optional[np.ndarray] = None

    @classmethod
    def from_files(cls, dem_path: str, drainage_path: str) -> 'DEMProcessor':
        """Creates a processor from files."""
        print(PROGRESS_MESSAGES['loading'])
        dem_raster = GeoDataRaster(dem_path)
        drainage_vector = GeoDataVector(drainage_path)
        return cls(dem_raster, drainage_vector)

    def prepare_data(self, recursive: bool = False) -> Tuple[np.ndarray, np.ndarray]:
        """Prepares data for processing."""
        # Convert the drainage to a raster
        drainage_raster = rasterize_drainage(
            self.dem_raster,
            self.drainage_vector,
            recursive=recursive
        )

        # Create copies to modify
        dem_data = np.copy(self.dem_raster.data.astype(np.float64))
        drainage_data = np.copy(drainage_raster.astype(np.int32))

        # Replace NoData values with NaN
        if self.dem_raster.nodata is not None:
            dem_data = np.where(
                dem_data == self.dem_raster.nodata,
                np.nan,
                dem_data
            )

        return dem_data, drainage_data

    def process(self, strategy: FlowEnforcementStrategy, recursive: bool = False) -> 'ProcessingResult':
        """Processes the DEM using the specified strategy."""
        try:
            dem_data, drainage_data = self.prepare_data(recursive)

            corrected_dem = strategy.apply(
                dem_data=dem_data,
                drainage_data=drainage_data,
                resolution=self.dem_raster.get_resolution()
            )

            return ProcessingResult(corrected_dem, self.dem_raster)

        except Exception as e:
            raise DEMProcessingError(f"Error during processing: {e}")

class ProcessingResult:
    """Result of DEM processing."""

    def __init__(self, corrected_data: np.ndarray, original_raster: GeoDataRaster):
        self.corrected_data = corrected_data
        self.original_raster = original_raster

    def save(self, output_path: str) -> None:
        """Saves the result to the specified path."""
        self.original_raster.save(output_path, self.corrected_data)