# <h1 align="center">Gradient-Based Optimized Flow Enforcement (GBOFE)</h1>

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![NumPy](https://img.shields.io/badge/NumPy-2.3.0+-orange.svg)](https://numpy.org/)
[![Rasterio](https://img.shields.io/badge/Rasterio-1.4.3+-green.svg)](https://rasterio.readthedocs.io/)
[![GeoPandas](https://img.shields.io/badge/GeoPandas-1.0.1+-lightblue.svg)](https://geopandas.org/)
[![Version](https://img.shields.io/badge/Version-0.1-lightgrey.svg)]() <!-- Assuming the version is 0.1 based on __init__.py -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<h3 align="center">A New Algorithm for Flow Enforcement to Correct Surface Drainage Patterns and Improve Watershed Delineations Derived from Digital Elevation Models (DEMs)</h3>

<p align="center"> 
  <img src="https://github.com/user-attachments/assets/b7073e1f-812d-49da-a8d7-6f569e1c8540" width="700" alt="GBOFE conceptual diagram">
</p> 

## Table of Contents
1. [Introduction](#introduction)
2. [Main Features](#main-features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Using GBOFE](#using-gbofe)
6. [Project Structure](#project-structure)
7. [Contributions](#contributions)
8. [License](#license)

## Introduction
**Gradient-Based Optimized Flow Enforcement (GBOFE)** is an innovative stream-burning algorithm that substantially improves the representation of drainage networks in Digital Elevation Models (DEMs). Unlike traditional approaches—which typically carve deep channels and cause significant morphometric losses—GBOFE adjusts only the cells that are strictly necessary, applying the minimum topographic gradient required to guarantee continuous downslope flow. In this way, GBOFE:

<ol type="a">
  <li>Preserves the original topography: It minimizes alterations to a slope, curvature, and other DEM-derived attributes.</li>
  <li>Optimizes hydrological connectivity: It ensures that every cell drains toward the cell indicated by the vector drainage network, preventing spurious flows.</li>
  <li>Reduces bias in morphometric metrics: It enhances reliability in watershed delineation, stream-length calculations, contributing-area estimation, and discharge modeling.</li>
</ol>

## Main Features
*   **Multiple Correction Methods:** Four different Flow Enforcement methods are implemented.
    *   Normal Excavation
    *   Normal Excavation Modified
    *   r.carve
    *   Gradient-Based Optimized Flow Enforcement (GBOFE)
*   **Geospatial Data Support:** Processes DEMs in raster format and drainage networks in vector format.
*   **Interactive User Interface:** Facilitates method selection and input file specification.
*   **Efficient Processing:** Uses optimized libraries such as NumPy, Rasterio, and GeoPandas for geospatial data handling.

## Prerequisites
*   Python 3.12 or higher.
*   The Python libraries listed in the `requirements.txt` file.

## Installation
Follow these steps to set up the project in your local environment:

1.  **Clone the repository (or download the code):**
    ```bash
    # If using Git
    git clone https://github.com/WaterlabUT/Gradient-Based-Optimized-Flow-Enforcement-GBOFE.git
    cd gbofe
    ```
    If you have downloaded the code as a ZIP file, extract it to your desired location.

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # Activate the virtual environment
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    Ensure that the `requirements.txt` file is in the root directory of your project.
    ```bash
    pip install -r requirements.txt
    ```

## Using GBOFE
Follow this tutorial to use GBOFE:

1.  **Run the main script:**
    Navigate to the directory where you have cloned or unzipped the GBOFE project. Open the `main.py` file (or your project's main entry point script) in your preferred Python IDE and run it.

2.  **Choose the flow enforcement method:**
    Once the script is running, you will be presented with an interface (likely in the console) to select the technique you wish to apply:
    *   Normal Excavation
    *   Normal Excavation Modified
    *   r.carve
    *   Gradient-Based Optimized Flow Enforcement (GBOFE)

3.  **Specify the input DEM:**
    Enter the full path to the Digital Elevation Model (including the file name and extension). For example: `C:\data\fabdem_clip.tif`. Ensure the file format is compatible (e.g., GeoTIFF).

4.  **Specify the drainage network:**
    Provide the full path to the vector file containing the drainage network (including name and extension). For example: `C:\data\drainage.shp`. Common vector formats like Shapefile or GeoPackage are usually compatible.

5.  **Set the carving depth:**
    For **Normal Excavation**, **Normal Excavation Modified**, or **r.carve**, specify the carving depth in metres to be applied along the drainage network.
    If you select **GBOFE**, define the slope-reduction gradient `G > 0`. A recommended default is `G = 0.001`.
    
6.  **Configure the output:**
    Provide the path and file name for the corrected DEM, e.g. `C:\data\dem_burn.tif`.
    
7.  **Processing and Results:**
    The script will process the data using the selected method. Once completed, the results (the corrected DEM) will generally be saved in a specified output directory or in the same folder as the input data. Pay attention to console messages for the location of output files.

> **Note**  
> It is essential that the user digitizes the drainage network from upstream (source) to downstream (outlet). Additionally, it is crucial that both the Digital Elevation Model (DEM) and the drainage network share the same spatial reference system (projection and datum) to ensure proper alignment and spatial analysis.

## Project Structure
The GBOFE project is organized into the following main modules within the `gbofe/` folder:

*   `algorithms/`: Contains implementations of the different flow enforcement algorithms (e.g., `RCarveMethod`, `NormalExcavationMethod`, `GBOFEMethod`).
*   `models/`: Defines data structures for handling geospatial information (e.g., `GeoDataRaster`, `GeoDataVector`) and the main DEM processor (`DEMProcessor`).
*   `utils/`: Includes utility functions for file operations, geometric calculations, and user interface helpers.
*   `exceptions.py`: Defines custom exceptions for handling specific DEM processing errors.
*   `config.py`: Stores constants and configurations used throughout the project.
*   `main.py`: Entry point of the application, handles the main logic and user interaction.

## Contributions
Contributions are welcome. If you wish to contribute to the project, please consider the following:
1.  Fork the repository.
2.  Create a new branch for your feature or fix (`git checkout -b feature/new-feature` or `git checkout -b fix/bug-fix`).
3.  Make your changes and commit them (`git commit -m 'Add new feature'`).
4.  Push your changes to your fork (`git push origin feature/new-feature`).
5.  Open a Pull Request to the main branch of the original repository.

Please ensure your code follows the project's style guides and includes the necessary tests.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

---