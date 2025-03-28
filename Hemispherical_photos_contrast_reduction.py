import rawpy
from PIL import Image, ImageEnhance
import os

# Define your input and output directories
input_folder = '/mnt/gsdata/projects/bigplantsens/3_Field_data_collection/01_ECOSENSE/1_Hemispherical_photos/2025-03-24'
output_folder = '/mnt/gsdata/projects/bigplantsens/3_Field_data_collection/01_ECOSENSE/Hemi_photos_edited'
os.makedirs(output_folder, exist_ok=True)

# Set the contrast factor (1.0 means no change; less than 1.0 lowers contrast)
contrast_factor = 0.8  

# Process each raw file in the input folder
for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.lower().endswith(('.nef', '.cr2', '.arw', '.dng')):
            raw_path = os.path.join(root, file)
        
        with rawpy.imread(raw_path) as raw:
            rgb = raw.postprocess()  # Convert the raw file to an RGB image array
        img = Image.fromarray(rgb)
        
        # Lower the contrast using Pillow
        enhancer = ImageEnhance.Contrast(img)
        img_contrast = enhancer.enhance(contrast_factor)
        
        # Save the processed image as a JPEG file
        jpg_name = os.path.splitext(file)[0] + '.jpg'
        jpg_path = os.path.join(output_folder, jpg_name)
        img_contrast.save(jpg_path, quality=90)
