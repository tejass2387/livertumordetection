import nibabel as nib
import numpy as np
import cv2
import os

# --- Configuration ---
# Path to the folder containing your SORTED tumor .nii files.
NII_INPUT_DIR = r"C:\TempNii\TumorScans" 

# Path where you want to save the 2D JPG images.
JPG_OUTPUT_DIR = r"data\train\tumor" 
# --- End Configuration ---


def convert_nii_to_jpg(nii_dir, output_dir):
    """
    Loads all .nii files from a directory, converts their slices to JPG,
    and saves them to an output directory.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output will be saved to: {output_dir}")

    for filename in os.listdir(nii_dir):
        if filename.endswith((".nii", ".nii.gz")):
            print(f"Processing file: {filename}")
            
            # Load the .nii file
            nii_path = os.path.join(nii_dir, filename)
            nii_img = nib.load(nii_path)
            
            # Get the image data as a NumPy array
            image_data = nii_img.get_fdata()
            
            # Get the base filename without the extension
            base_filename = filename.replace(".nii.gz", "").replace(".nii", "")
            
            # Iterate through the slices along the 3rd axis
            num_slices = image_data.shape[2]
            for i in range(num_slices):
                # Get the 2D slice
                slice_2d = image_data[:, :, i]
                
                # --- Image Processing ---
                # Normalize pixel values to be between 0 and 255
                slice_normalized = cv2.normalize(slice_2d, None, 0, 255, cv2.NORM_MINMAX)
                
                # Convert to an 8-bit unsigned integer
                slice_uint8 = np.uint8(slice_normalized)
                
                # Convert grayscale to 3-channel BGR to match model input
                slice_bgr = cv2.cvtColor(slice_uint8, cv2.COLOR_GRAY2BGR)
                
                # Define the output filename
                output_filename = f"{base_filename}_slice_{i:03d}.jpg"
                output_path = os.path.join(output_dir, output_filename)
                
                # Save the image
                cv2.imwrite(output_path, slice_bgr)
                
            print(f"-> Finished converting {filename}, created {num_slices} JPG images.")

if __name__ == '__main__':
    # This check is updated to ensure you've changed the default paths.
    if "path/to" in NII_INPUT_DIR:
         print("ERROR: Please update the NII_INPUT_DIR and JPG_OUTPUT_DIR paths in the script before running.")
    else:
        print("Starting conversion process...")
        convert_nii_to_jpg(NII_INPUT_DIR, JPG_OUTPUT_DIR)
        print("Conversion complete!")