import time
import tifffile as tif
import napari
from sols_microscope import DataPreview, DataRoi, DataNative, DataTraditional

def imread(filename): # re-define imread to keep 5D axes
    with tif.TiffFile(filename) as t:
        axes = t.series[0].axes
        hyperstack = t.series[0].asarray()
    return tif.transpose_axes(hyperstack, axes, 'TZCYX')

def imwrite(filename, data):
    return tif.imwrite(filename, data, imagej=True)

def view_in_napari(data_preview,
                   data_preview_roi=None,
                   data_native=None,
                   voxel_aspect_ratio=None, # Needed for data_native
                   data_traditional=None):
    print('\nViewing in napari')
    with napari.gui_qt():
        preview = napari.Viewer()
        preview.add_image(data_preview, name='data_preview')
        if data_preview_roi is not None:
            preview_roi = napari.Viewer()
            preview_roi.add_image(data_preview_roi, name='data_preview_roi')
        if data_native is not None:
            native = napari.Viewer()
            for channel in range(data_native.shape[2]):
                native.add_image(data_native[:, :, channel, :, :],
                                 name='data_native',
                                 scale=(1, voxel_aspect_ratio, 1, 1))
        if data_traditional is not None: 
            traditional = napari.Viewer()
            for channel in range(data_traditional.shape[2]):
                traditional.add_image(data_traditional[:, :, channel, :, :],
                                      name='data_traditional')

# Get processsing tools:
datapreview     = DataPreview()
dataroi         = DataRoi()
datanative      = DataNative()
datatraditional = DataTraditional()

# Get data and metadata:
t0 = time.perf_counter()
print('\nGetting: data', end=' ')
data = imread('data.tif')
t1 = time.perf_counter()
print('(%0.2fs)'%(t1 - t0))
print('-> data.shape =', data.shape)
print('-> format = 5D "tzcyx" (volumes, slices, channels, height_px, width_px)')
scan_step_size_px = 3
preview_line_px = 10
preview_crop_px = 3
timestamp_mode = "binary+ASCII"
voxel_aspect_ratio =  1.7320508075688772

# Get preview:
print('\nGetting: preview', end=' ')
preview = datapreview.get(
    data, scan_step_size_px, preview_line_px, preview_crop_px, timestamp_mode)
t2 = time.perf_counter()
print('(%0.2fs)'%(t2 - t1))
print('-> saving: data_preview.tif')
imwrite('data_preview.tif', preview)

# Get roi: -> edit 'signal_to_bg_ratio' and 'gaussian_filter_std' as needed
print('\nGetting: roi', end=' ')
roi = dataroi.get(data, preview_crop_px, timestamp_mode,
                  signal_to_bg_ratio=1.2, gaussian_filter_std=3)
t3 = time.perf_counter()
print('(%0.2fs)'%(t3 - t2))
print('-> saving: data_roi.tif')
imwrite('data_roi.tif', roi)

# Get roi preview:
print('\nGetting: roi preview', end=' ')
roi_preview = datapreview.get(
    roi, scan_step_size_px, preview_line_px, preview_crop_px, timestamp_mode)
t4 = time.perf_counter()
print('(%0.2fs)'%(t4 - t3))
print('-> saving: data_roi_preview.tif')
imwrite('data_roi_preview.tif', roi_preview)

# Get native data:
print('\nGetting: roi native view', end=' ')
native = datanative.get(roi, scan_step_size_px)
t5 = time.perf_counter()
print('(%0.2fs)'%(t5 - t4))
print('-> saving: data_roi_native.tif')
imwrite('data_roi_native.tif', native)

# Get traditional data for roi: -> this is very slow (adds about ~30s)
print('\nGetting: roi traditional view', end=' ')
native_subset = native[0:1, : , 0:1, :, :] # -> picking 1 volume, but keep 5D!
traditional = datatraditional.get(native_subset, scan_step_size_px)
t6 = time.perf_counter()
print('(%0.2fs)'%(t6 - t5))
print('-> saving: data_roi_traditional.tif')
imwrite('data_roi_traditional.tif', traditional)

# View in napari (or checked saved data with ImageJ or similar):
view_in_napari(preview, roi_preview, native, voxel_aspect_ratio, traditional)
