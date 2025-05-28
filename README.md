# <h1 align="center"> Gradient Based Optimized Flow Enforcement GBOFE

## New Algorithm for Flow Enforcement to Correct Surface Drainage Patterns and Improve Boundary Delimitations Derived from DEM
<p align="center"> 
  <img src="https://github.com/user-attachments/assets/b7073e1f-812d-49da-a8d7-6f569e1c8540"width="800">
</p> 

<h1 align="center">Software required</h1>

- **GDAL** 2.2.3  
- **OpenCV** 3.2.0  
- **Python** 3.7.9  
- **PyTorch** 1.4.0  
- **torchvision** 0.5.0  
- **pytorch-lightning** 1.0.6  
- **gdal**  
- **numpy**  
- **opencv-python**  
- **opencv-contrib-python**  
- **scipy**  
- **tqdm**  
- **networkx**  
- **richdem**

<h1 align="center">Tutorial</h1>

# GBOFE Usage Tutorial

## 1. Download the code
Locate the **GBOFE** folder and download the source code to your computer.

## 2. Run the script
Open the main file in your preferred Python IDE and run it.

## 3. Choose the flow-enforcement method
In the interface, select the technique you wish to apply:

- **Normal Excavation**
- **Normal Excavation Modified**
- **r.carve**
- **Gradient-Based Optimized Flow Enforcement (GBOFE)**

## 4. Specify the input DEM
Enter the full path to the Digital Elevation Model (including file name and extension), e.g. `FABDEM.tif`.

## 5. Specify the drainage network
Enter the full path to the drainage vector file (including file name and extension), e.g. `Drainage.shp`.

## 6. Set the carving depth *(if applicable)*
For **Normal Excavation**, **Normal Excavation Modified**, or **r.carve**, specify the carving depth in metres to be applied along the drainage network.

## 7. Set the gradient *(GBOFE only)*
If you select **GBOFE**, define the slope-reduction gradient `G > 0`. A recommended default is `G = 0.001`.

## 8. Configure the output
Provide the path and file name for the corrected DEM, e.g. `FABDEM_burn.tif`.

> **Note**  
> It is essential that the user digitizes the drainage network from upstream (source) to downstream (outlet). Additionally, it is crucial that both the Digital Elevation Model (DEM) and the drainage network share the same spatial reference system (projection and datum) to ensure proper alignment and spatial analysis.

<h1 align="center">Application Example</h1>

**Hydrographic Subzone of the Recio and Venadillo Rivers**

<p align="center">
  <img src="https://github.com/user-attachments/assets/82b61a72-99f0-4332-a971-23d0920bc0da" width="600">
</p>

1. **Download the `Example_Data` folder, which includes:**
   - `FABDEM.tif`: Digital Elevation Model (FABDEM) of the study area.  
   - `Drainage.shp`: Vector drainage network of the Recio and Venadillo rivers.

2. **Run the GBOFE code** following steps 1 and 2 of the main tutorial.

3. **Specify the path to the Digital Elevation Model** (`FABDEM.tif`).

4. **Specify the path to the vector drainage network** (`Drainage.shp`).

5. **Configure the flow correction method:**
   - For **Normal Excavation**, **Normal Excavation Modified**, or **r.carve**, enter the desired *carving* value.  
   - For **Gradient-Based Optimized Flow Enforcement (GBOFE)**, enter the gradient parameter `G`. A standard value of `G = 0.001` is recommended.

