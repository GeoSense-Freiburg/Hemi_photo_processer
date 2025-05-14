import rawpy
import cv2
import numpy as np
import os

input_folder = '/mnt/gsdata/projects/icos_har/hemi_photo/2025-05-08/raw/'
output_folder = '/mnt/gsdata/projects/icos_har/hemi_photo/2025-05-08/contrast_corrected'
os.makedirs(output_folder, exist_ok=True)

def enhance_image_cv2(img_rgb):
    # Convert to LAB color space for brightness/contrast control
    lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)

    # Apply CLAHE (adaptive histogram equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    lab = cv2.merge((cl, a, b))

    # Convert back to RGB
    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

    # Apply sharpening filter
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)

    return sharpened

for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.lower().endswith(('.nef', '.cr2', '.arw', '.dng')):
            raw_path = os.path.join(root, file)
            
            with rawpy.imread(raw_path) as raw:
                rgb = raw.postprocess(use_camera_wb=True, no_auto_bright=False)

            enhanced_img = enhance_image_cv2(rgb)
            output_path = os.path.join(output_folder, os.path.splitext(file)[0] + '.jpg')
            cv2.imwrite(output_path, cv2.cvtColor(enhanced_img, cv2.COLOR_RGB2BGR), [int(cv2.IMWRITE_JPEG_QUALITY), 95])
