import SimpleITK as sitk

def read_mhd(inputpath):
    inputimage = sitk.ReadImage(inputpath)
    spacing = inputimage.GetSpacing()
    origin = inputimage.GetOrigin()
    outputimage = sitk.GetArrayFromImage(inputimage)
    size = inputimage.GetSize()
    return outputimage, spacing, origin, size