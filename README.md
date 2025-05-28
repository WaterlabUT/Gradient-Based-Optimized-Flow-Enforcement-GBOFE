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
> Ensure the drainage network is digitized from upstream (source) to downstream (outlet).

<h1 align="center">Ejemplo de aplicación</h1>

**Subzona hidrográfica de los ríos Recio y Venadillo**

<p align="center">
  <img src="https://github.com/user-attachments/assets/82b61a72-99f0-4332-a971-23d0920bc0da" width="600">
</p>


1. **Descargue la carpeta `Example_Data`, que incluye:**
   - `FABDEM.tif`: modelo digital de elevación (FABDEM) de la zona de estudio.  
   - `Drainage.shp`: red de drenaje vectorial de los ríos Recio y Venadillo.

2. **Ejecute el código GBoFE** siguiendo los pasos 1 y 2 indicados en el tutorial principal.

3. **Especifique la ruta del modelo digital de elevación** (`FABDEM.tif`).

4. **Especifique la ruta de la red de drenaje vectorial** (`Drainage.shp`).

5. **Configure el método de corrección de flujo:**
   - Para **Normal Excavation**, **Normal Excavation Modified** o **r.carve**, introduzca el valor de *carving* que desee utilizar.  
   - Para **Gradient-Based Optimized Flow Enforcement (GBoFE)**, introduzca el parámetro de gradiente `G`. Se recomienda `G = 0.001` como valor estándar.


