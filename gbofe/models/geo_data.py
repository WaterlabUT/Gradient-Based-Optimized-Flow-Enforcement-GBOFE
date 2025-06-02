"""
Classes for handling geospatial data.
"""
import geopandas as gpd
import rasterio
import numpy as np
from typing import Optional, Any, Union
import os
from gbofe.exceptions import InvalidFileFormatError, FileNoFoundError, DEMProcessingError
from gbofe.config import PROGRESS_MESSAGES

class GeoDataRaster:
    """Class for storing information about a raster file and its attributes."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.data: Optional[np.ndarray] = None
        self.transform: Optional[Any] = None
        self.width: Optional[int] = None
        self.height: Optional[int] = None
        self.crs: Optional[Any] = None
        self.nodata: Optional[Union[int, float]] = None
        self.bounds: Optional[Any] = None

        # Additional attributes for processing
        self.drainage: Optional[np.ndarray] = None
        self.burn: Optional[np.ndarray] = None

        self._validate_file()
        print(f"📋 {PROGRESS_MESSAGES['loading']} raster...")
        self._load_raster()

    def _validate_file(self) -> None:
        """Validates that the file exists and has the correct format."""
        if not os.path.isfile(self.file_path):
            raise FileNoFoundError(f"File {self.file_path} does not exist")
        if not self.file_path.lower().endswith(('.tif', '.tiff')):
            raise InvalidFileFormatError(f"Unsupported file format: {self.file_path}")

    def _load_raster(self) -> None:
        """Loads raster data."""
        try:
            with rasterio.open(self.file_path) as src:
                self.data = src.read(1)
                self.transform = src.transform
                self.width = src.width
                self.height = src.height
                self.crs = src.crs
                self.nodata = src.nodata
                self.bounds = src.bounds
        except Exception as e:
            raise DEMProcessingError(f"Error loading raster: {e}")

    def get_resolution(self) -> float:
        """Gets raster resolution (assuming square pixels)."""
        return abs(self.transform.a)

    def save(self, output_path: str, data: Optional[np.ndarray] = None) -> None:
        """Saves the raster to the specified path."""
        data_to_save = data if data is not None else self.data
        print(f"📋 {PROGRESS_MESSAGES['saving']}...")

        try:
            with rasterio.open(
                    output_path, "w",
                    driver="GTiff",
                    height=self.height,
                    width=self.width,
                    count=1,
                    dtype=data_to_save.dtype,
                    crs=self.crs,
                    transform=self.transform,
                    nodata=self.nodata,
            ) as dst:
                dst.write(data_to_save, 1)
        except Exception as e:
            raise DEMProcessingError(f"Error saving raster: {e}")


class GeoDataVector:
    """Class for storing information about a vector file and its attributes."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.geo: Optional[gpd.GeoDataFrame] = None

        self._validate_file()
        print(f"📋 {PROGRESS_MESSAGES['loading']} vector...")
        self._load_vector()

    def _validate_file(self) -> None:
        """Validates that the file exists and has the correct format."""
        if not os.path.isfile(self.file_path):
            raise FileNoFoundError(f"File {self.file_path} does not exist")
        if not self.file_path.lower().endswith('.shp'):
            raise InvalidFileFormatError(f"Unsupported file format: {self.file_path}")

    def _load_vector(self) -> None:
        """Loads vector data."""
        try:
            self.geo = gpd.read_file(self.file_path)
        except Exception as e:
            raise DEMProcessingError(f"Error loading vector: {e}")

    @property
    def crs(self) -> Any:
        """Gets the vector coordinate system."""
        return self.geo.crs if self.geo is not None else None

    def reproject(self, target_crs: Any) -> None:
        """Reprojects the vector to the specified coordinate system."""
        if self.geo is not None:
            self.geo = self.geo.to_crs(target_crs)