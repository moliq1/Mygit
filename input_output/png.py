import glob
import SimpleITK as sitk
import numpy as np


def read_png(lung_mask_path):
    pngfile_list = glob.glob(lung_mask_path + '/' + '*.png')
    pngfile_list.sort()
    sitk_reader = sitk.ImageSeriesReader()
    sitk_reader.SetFileNames(pngfile_list)
    sitk_mask = sitk_reader.Execute()
    mask = sitk.GetArrayFromImage(sitk_mask)
    mask[mask > 0] = 1
    mask = mask.astype(np.int8)
    return mask
