import csv
import glob
import numpy as np 
import SimpleITK as sitk



############################################
# csv reading
############################################

def write_csv(filename, lines):
    with open(filename, "wb") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerows(lines)


def read_csv(filename):
    lines = []
    with open(filename, "rb") as f:
        csvreader = csv.reader(f)
        for line in csvreader:
            lines.append(line)
    return lines


def read_csv_without_first_line(file_name):
    lines = read_csv(file_name)
    return lines[1:]


def try_float(value):
    try:
        value = float(value)
    except:
        value = value

    return value


def get_column(lines, columnid, elementType=''):
    column = []
    for line in lines:
        try:
            value = line[columnid]
        except:
            continue

        if elementType == 'float':
            value = try_float(value)

        column.append(value)
    return column




############################################
# dicom reading
############################################


def normalize_image(image, min_hu=-1150, max_hu=350, to255=False):
    # image = np.array(image, np.float)
    image[image > max_hu] = max_hu
    image[image < min_hu] = min_hu
    image = (image - min_hu) / float(max_hu - min_hu)
    image = image.astype(np.float32)
    if to255:
        image = (image*255).astype(np.uint8)
    return image

def read_dcm_to_array(file_dir, min_hu=-1150, max_hu=350, normalize=False):
    reader = sitk.ImageSeriesReader()
    filenames = reader.GetGDCMSeriesFileNames(file_dir)
    reader.SetFileNames(filenames)
    sitk_image = reader.Execute()
    spacing = sitk_image.GetSpacing()
    origin = sitk_image.GetOrigin()
    size = sitk_image.GetSize()
    numpy_image = sitk.GetArrayFromImage(sitk_image)
    if normalize:
        numpy_image = normalize_image(numpy_image, min_hu, max_hu)
    return numpy_image, spacing, origin, size


def read_mhd_to_array(inputpath, min_hu=-1150, max_hu=350, normalize=False):
    inputimage = sitk.ReadImage(inputpath)
    spacing = inputimage.GetSpacing()
    origin = inputimage.GetOrigin()
    outputimage = sitk.GetArrayFromImage(inputimage)
    size = inputimage.GetSize()
    if normalize:
        numpy_image = normalize_image(outputimage, min_hu, max_hu)
    return outputimage, spacing, origin, size


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