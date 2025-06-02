"""
Base strategy for flow enforcement methods.
"""
import numpy as np
from abc import ABC, abstractmethod

class FlowEnforcementStrategy(ABC):
    """Base strategy for flow enforcement methods in DEM."""

    def __init__(self, gradient: float):
        self.gradient = gradient
        self._validate_gradient()

    def _validate_gradient(self) -> None:
        """Validates that the gradient is positive."""
        if self.gradient <= 0:
            raise ValueError("Gradient must be greater than 0")

    @abstractmethod
    def apply(self, dem_data: np.ndarray, drainage_data: np.ndarray,
              resolution: float) -> np.ndarray:
        """
        Applies the flow enforcement method.

        Args:
            dem_data: DEM data
            drainage_data: Rasterized drainage data
            resolution: Raster resolution

        Returns:
            Corrected DEM
        """
        pass

    @staticmethod
    def get_drainage_indices(drainage_data: np.ndarray,
                             min_threshold: int = 1) -> np.ndarray:
        """Gets the indices where drainage exists."""
        return np.argwhere(drainage_data >= min_threshold)