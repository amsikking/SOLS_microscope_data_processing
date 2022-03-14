import numpy as np
import tifffile as tif

def imread(filename): # re-define imread to keep 5D axes
    with tif.TiffFile(filename) as t:
        axes = t.series[0].axes
        hyperstack = t.series[0].asarray()
    return tif.transpose_axes(hyperstack, axes, 'TZCYX')

def imwrite(filename, data):
    return tif.imwrite(filename, data, imagej=True)

# Get data and combine into single file:
data = []
for i in range(20):
    filename = 'data%02i.tif'%i
    data_strip = imread('data%02i.tif'%i)
    print('Found: %s, shape = %s'%(filename, data_strip.shape))
    data.append(data_strip)

data = np.concatenate(data, axis=4)
print('\nCombined data in single file, shape = %s'%str(data.shape))
print('-> saving: ..\data.tif')
imwrite('..\data.tif', data)
print('-> done!')
