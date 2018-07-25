import os
import cv2
import matplotlib.pyplot as plt 


def read_dcm_to_array(file_dir, min_hu=-1150, max_hu=350, normalize=True):
    reader = sitk.ImageSeriesReader()
    filenames = reader.GetGDCMSeriesFileNames(file_dir)
    reader.SetFileNames(filenames)
    sitk_image = reader.Execute()
    numpy_image = sitk.GetArrayFromImage(sitk_image)
    if normalize:
        numpy_image = normalize_image(numpy_image)
    return numpy_image


def normalize_image(image, min_hu=-1150, max_hu=350, to255=False):
    # image = np.array(image, np.float)
    image[image > max_hu] = max_hu
    image[image < min_hu] = min_hu
    image = (image - min_hu) / float(max_hu - min_hu)
    image = image.astype(np.float32)
    if to255:
    	image = (image*255).astype(np.uint8)
    return image

def draw_contour(img, label, color=(0, 255, 0), line=1, text_infos=None, text_color=(0,0,128)):
	_, contours, _ = cv2.findContours(label, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	if len(contours) >= 0:
		cv2.drawContours(img, contours, -1, color, line)
	if text_infos is not None:
		for text_info in text_infos:
			x = text_info.center[1]
			y = text_info.center[0]
			cv2.putText(img, "%s"%(text_info.text), (int(x)-10, int(y)),
						cv2.FONT_HERSHEY_SIMPLEX, 0.2, text_color, 1)
	return img


def plot_3dmasks_to_folder(mask, folder='tmp', axis=-1):
	if not os.path.exists(folder):
		os.makedirs(folder)
	if mask.max() <= 1:
		mask = mask*255
	for i in range(mask.shape[axis]):
		if axis == 0:
			ma = mask[i, :, :]
		elif axis ==1:
			ma = mask[:, i, :]
		else:
			ma = mask[:, :, i]
		cv2.imwrite(os.path.join(folder, '%d.png'%i), ma)
	print 'mask is written to %s'%folder


def plot_3dimages_with_mask_contour(image, masks=None, folder='tmp', axis=-1, normalize=False):
	if not os.path.exists(folder):
		os.makedirs(folder)
	if normalize:
		pass
		#TODO
	if image.max() <= 1:
		image = image*255
	for i in range(image.shape[axis]):
		if axis == 0:
			im = image[i, :, :]
		elif axis ==1:
			im = image[:, i, :]
		else:
			im = image[:, :, i]
		
		if masks:
			out_image = np.stack([im, im, im], axis=-1)
			colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
			if not isinstance(masks, list):
				masks = [masks]
			for ind, mask in enumerate(masks):
				color_map = colors[ind]
				if axis == 0:
					ma = mask[i, :, :]
				elif axis ==1:
					ma = mask[:, i, :]
				else:
					ma = mask[:, :, i]
				out_image = draw_contour(out_image.astype(np.uint8), ma.astype(np.uint8), color_map)
		else:
			out_image = im

		cv2.imwrite(os.path.join(folder, '%d.png'%i), out_image)
	print 'image with contour is written to %s'%folder


					