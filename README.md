# <h1 align="center"> Gradient Based Optimized Flow Enforcement GBOFE

## New Algorithm for Flow Enforcement to Correct Surface Drainage Patterns and Improve Boundary Delimitations Derived from DEM
<p align="center"> 
  <img src="https://github.com/user-attachments/assets/b7073e1f-812d-49da-a8d7-6f569e1c8540"width="1500">
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

1. Download the code: Locate the GBOFE folder and download the source code to your computer.

2. Run the script: Open the main file in your preferred Python IDE and run it.

3.Choose the flow-enforcement method: Select the technique you wish to apply:

Normal Excavation

Normal Excavation Modified

r.carve

Gradient-Based Optimized Flow Enforcement (GBOFE)

4. Specify the input DEM: Enter the full path to the Digital Elevation Model (including file name and extension), e.g. FABDEM.tif.

5. Specify the drainage network: Enter the full path to the drainage vector file (including file name and extension), e.g. Drainage.shp.

Set the carving depth (if applicable):

6.For Normal Excavation, Normal Excavation Modified, or r.carve, specify the carving depth (in metres) applied along the drainage network.

Set the gradient (GBOFE only):

7.If you select GBOFE, define the slope-reduction gradient 𝐺>0. A recommended default is 𝐺=0.001

8. Configure the output: Provide the path and file name for the corrected DEM, e.g. FABDEM_burn.tif.

Note: Ensure your drainage network is digitised from upstream (source) to downstream (outlet).



