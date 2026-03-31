import os
import shutil
import re

# --- Configuration ---
# 1. Path to the folder containing your raw dataset.
#    This has been updated to your specified location.
RAW_DATA_DIR = r"C:\MyLiverDataset"

# 2. Path to a temporary directory where the sorted .nii files will be copied.
SORTED_NII_DIR = r"C:\TempNii"
# --- End Configuration ---


def sort_nii_files(raw_dir, sorted_dir):
    """
    Sorts .nii volume files from multiple 'volume_pt' subdirectories into 
    'TumorScans' and 'NoTumorScans' folders based on the presence of a 
    corresponding segmentation file.
    """
    # Define paths
    segmentation_dir = os.path.join(raw_dir, 'segmentations')
    output_tumor_dir = os.path.join(sorted_dir, 'TumorScans')
    output_no_tumor_dir = os.path.join(sorted_dir, 'NoTumorScans')

    # Create output directories if they don't exist
    os.makedirs(output_tumor_dir, exist_ok=True)
    os.makedirs(output_no_tumor_dir, exist_ok=True)

    # --- Step 1: Get all segmentation numbers ---
    segmentation_numbers = set()
    if os.path.exists(segmentation_dir):
        for f in os.listdir(segmentation_dir):
            # Use regex to find the number in filenames like 'segmentation-10.nii'
            match = re.search(r'(\d+)', f)
            if match:
                segmentation_numbers.add(int(match.group(1)))
    print(f"Found {len(segmentation_numbers)} unique segmentation files.")

    # --- Step 2: Find all volume directories ---
    volume_dirs = [os.path.join(raw_dir, d) for d in os.listdir(raw_dir) if d.startswith('volume_pt')]
    print(f"Found {len(volume_dirs)} volume directories to search in.")

    # --- Step 3: Iterate through all volumes and sort them ---
    total_volumes = 0
    for vol_dir in volume_dirs:
        for f in os.listdir(vol_dir):
            if f.endswith(('.nii', '.nii.gz')):
                total_volumes += 1
                match = re.search(r'(\d+)', f)
                if not match:
                    continue
                
                volume_number = int(match.group(1))
                source_path = os.path.join(vol_dir, f)

                # Check if this volume has a corresponding segmentation
                if volume_number in segmentation_numbers:
                    # It has a tumor, copy to TumorScans
                    shutil.copy(source_path, os.path.join(output_tumor_dir, f))
                else:
                    # It does not have a tumor, copy to NoTumorScans
                    shutil.copy(source_path, os.path.join(output_no_tumor_dir, f))

    print(f"\nSorting complete!")
    print(f"Processed {total_volumes} total volumes.")
    print(f"Sorted {len(os.listdir(output_tumor_dir))} files into '{output_tumor_dir}'")
    print(f"Sorted {len(os.listdir(output_no_tumor_dir))} files into '{output_no_tumor_dir}'")


if __name__ == '__main__':
    # Ensure paths are correctly configured before running
    if "path/to" in RAW_DATA_DIR:
        print("ERROR: Please update the RAW_DATA_DIR path in the script before running.")
    else:
        sort_nii_files(RAW_DATA_DIR, SORTED_NII_DIR)