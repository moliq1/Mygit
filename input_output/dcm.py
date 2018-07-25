import SimpleITK as sitk


def read_dcm_files(file_dir):
    reader = sitk.ImageSeriesReader()
    filenames = reader.GetGDCMSeriesFileNames(file_dir)
    reader.SetFileNames(filenames)
    sitk_image = reader.Execute()
    spacing = sitk_image.GetSpacing()
    origin = sitk_image.GetOrigin()
    size = sitk_image.GetSize()
    return sitk_image, spacing, origin, size


def read_dcm_to_ndimage(file_dir):
    sitk_image, spacing, origin, size = read_dcm_files(file_dir)
    numpy_image = sitk.GetArrayFromImage(sitk_image)
    return numpy_image, spacing, origin, size


# input_path = '/home/fc/fc/dcms_temp/1.3.6.1.4.1.14519.5.2.1.6279.6001.108197895896446896160048741492/000001.dcm'
# file_reader = sitk.ImageFileReader()
# file_reader.SetFileName(input_path)
# sitk_image=file_reader.Execute()
# print sitk_image.GetMetaDataKeys()