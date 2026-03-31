import pydicom
import numpy as np
import cv2
import os

# --- Configuration ---
# 1. Path to the PARENT folder containing all the 'DICOM_anon' subfolders.
DCM_PARENT_DIR = r"C:\MyLiverDataset 2" 

# 2. Path where you want to save the 2D JPG images.
JPG_OUTPUT_DIR = r"data\train\no_tumor" 
# --- End Configuration ---


def convert_dcm_to_jpg(dcm_parent_dir, output_dir):
    """
    Walks through all subdirectories of a parent folder, finds all .dcm files,
    converts them to JPG, and saves them to an output directory.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output will be saved to: {output_dir}")

    total_files_converted = 0
    # os.walk is perfect for this. It goes into every folder and subfolder.
    for root, _, files in os.walk(dcm_parent_dir):
        for filename in files:
            if filename.endswith(".dcm"):
                dcm_path = os.path.join(root, filename)
                
                # Read the DICOM file
                try:
                    dcm_data = pydicom.dcmread(dcm_path)
                except Exception as e:
                    print(f"Could not read {dcm_path}. Skipping. Error: {e}")
                    continue

                # Get the pixel data
                if 'PixelData' in dcm_data:
                    image_data = dcm_data.pixel_array
                else:
                    print(f"No pixel data in {filename}. Skipping.")
                    continue
                    
                # --- Image Processing ---
                image_normalized = cv2.normalize(image_data, None, 0, 255, cv2.NORM_MINMAX)
                image_uint8 = np.uint8(image_normalized)
                image_bgr = cv2.cvtColor(image_uint8, cv2.COLOR_GRAY2BGR)
                
                # Define a unique output filename
                # We combine the subfolder name and filename to avoid overwrites
                parent_folder_name = os.path.basename(root)
                base_filename = os.path.splitext(filename)[0]
                output_filename = f"{parent_folder_name}_{base_filename}.jpg"
                output_path = os.path.join(output_dir, output_filename)
                
                # Save the image
                cv2.imwrite(output_path, image_bgr)
                total_files_converted += 1
            
    print(f"\nFinished converting files. Total JPGs created: {total_files_converted}")


if __name__ == '__main__':
    if "path/to" in DCM_PARENT_DIR:
         print("ERROR: Please update the DCM_PARENT_DIR path in the script before running.")
    else:
        print("Starting DICOM to JPG conversion process...")
        convert_dcm_to_jpg(DCM_PARENT_DIR, JPG_OUTPUT_DIR)
        print("Conversion complete!")