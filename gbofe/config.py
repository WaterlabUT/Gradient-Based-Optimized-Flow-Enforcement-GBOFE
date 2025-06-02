"""
Configs and constants for DEM processing.
"""
import numpy as np
from enum import Enum

class FlowEnforcementMethod(Enum):
    """Available methods for flow correction."""
    R_CARVE = 1
    NORMAL_EXCAVATION = 2
    NORMAL_EXCAVATION_MODIFIED = 3
    GBOFE = 4

# Geometric constants
DIAGONAL_MULTIPLIER = np.sqrt(2)
FLOW_ACCUMULATION_THRESHOLD = 1

# File configurations
SUPPORTED_RASTER_EXTENSIONS = [".tif", ".tiff"]
SUPPORTED_VECTOR_EXTENSIONS = [".shp"]

# Interface configurations
METHOD_DESCRIPTIONS = {
    FlowEnforcementMethod.R_CARVE: "r.carve",
    FlowEnforcementMethod.NORMAL_EXCAVATION: "Normal Excavation",
    FlowEnforcementMethod.NORMAL_EXCAVATION_MODIFIED: "Normal Excavation Modified",
    FlowEnforcementMethod.GBOFE: "Gradient-Based Optimized Flow Enforcement (gbofe)"
}

# Progress messages
PROGRESS_MESSAGES = {
    'loading': 'Loading data',
    'rasterizing': 'Export to raster drainage shapefile',
    'processing': 'Processing DEM correction',
    'hierarchy': 'Creating drainage hierarchy',
    'saving': 'Saving result'
}
