# SOLS_microscope_data_processing
An example of how to process SOLS microscope data into more conventional formats
## Quick start:
- Download the whole repository (~400MB) and run 'make_data_file.py' (drops 'data.tif' into the main directory).
- Get a copy of 'sols_microscope.py' that contains the various data processing methods (https://github.com/amsikking/SOLS_microscope).
- Collect and install any missing dependencies (numpy, scipy, tifffile, napari, etc).
- Run 'sols_microscope_data_processing.py' to see the conversion of data from **'raw' -> 'preview' -> 'native' -> 'traditional'**.

Note: the critical **_metadata parameters_** needed to correctly process the data are preset in this example (scan_step_size_px, preview_line_px, timestamp_mode and voxel_aspect_ratio). However, they should normally be collected from the associated metadata file produced by the microscope (example included here -> 'metadata.txt').
## Details:
- 'data.tif' is a 5D acquisition of a fluorescent sphere etched in glass (for reference see the included datasheet 'pattern G' or https://argolight.com/). This concrete example has 2 volumes, 134 slices, 3 colors, 500 height pixels and 500 width pixels.
- If you're new to SOLS data a sphere is a good first example to visualize the various processing steps (i.e. it's 3D with an unambiguous shape).
- The **'raw'** data is how it comes from the camera and (barring cropping or compression) it's the most compact format. For the original SOLS system the raw data (by default) also contains the 'timestamps' that can be used to extract microsecond timing information (see https://github.com/amsikking/pco_decode_timestamp)
- The **'preview'** shows max intensity projections in the usual XYZ coordinates of a typical microscope. For speed and simplicity these are computed to the **_nearest pixel_** without interpolation and so may not be appropriate for rigorous analysis.
- The **'native'** view unshears the raw data into the naturally **_tilted_** coordinate system of the microscope (~30deg in the original SOLS system). In the default mode of SOLS the 'scan step sizes' are chosen so that _this_ shear operation can be done with integer pixels (i.e. no interpolation or nearest pixel approximation). Generating the native data is therefore fast and efficient, and the resulting voxels are **_cuboids_** (with an aspect ratio that is chosen during acquisition). The native view may therefore be the most principled data/coordinate system to use for rigorous analysis.
- The **'traditional'** view rotates the native view (with interpolation) back to the usual XYZ coordinates of a typical microscope, but (as currently implemented) this is **_very slow_** and may not be necessary. However for those who want to see their data in the traditional way it can be a pleasing operation.

Note: A basic **_roi cropping_** function (sols_microscope.DataRoi) is used here to reduce the data before processing. The SOLS microscope produces vast amounts of data very quickly (up to ~750MB/s continuously in the original system!). The 'native' and 'traditional' views (as currently implemented) greatly increase the data size **_-> so it is recommended that any cropping/data reduction be done as early as possible!_**


