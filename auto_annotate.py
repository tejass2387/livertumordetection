import os
import cv2
import torch
import numpy as np
import segmentation_models_pytorch as smp
from tqdm import tqdm # A progress bar library

# --- Configuration ---
# Directory with the JPG images you want to annotate
IMAGE_DIR = r"data\train\tumor"
# The number of images to process at once.
BATCH_SIZE = 32
# --- End Configuration ---

def apply_liver_window_batch(images):
    """Applies a liver CT window to a batch of images."""
    # ** THE FIX IS HERE: Convert to a larger data type before processing **
    images = images.astype(np.int16)

    window_center = 150
    window_width = 300
    min_window = window_center - window_width // 2
    max_window = window_center + window_width // 2
    
    images = np.clip(images, min_window, max_window)
    images = (images - min_window) / window_width * 255.0
    return np.uint8(images)

def auto_generate_annotations_batch(image_dir):
    """
    Uses a pre-trained U-Net model and BATCH PROCESSING to quickly generate
    bounding box annotations in YOLO .txt format.
    """
    print("Loading pre-trained segmentation model...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = smp.Unet(
        encoder_name="resnet34",
        encoder_weights="imagenet",
        in_channels=3,
        classes=1,
    ).to(device)
    model.eval()

    # Get a list of all images to process
    image_files = [f for f in os.listdir(image_dir) if f.endswith((".jpg", ".png", ".jpeg"))]
    print(f"Found {len(image_files)} images to process.")

    # Process images in batches
    for i in tqdm(range(0, len(image_files), BATCH_SIZE), desc="Annotating Batches"):
        batch_files = image_files[i:i + BATCH_SIZE]
        batch_input_tensors = []
        original_shapes = []

        for filename in batch_files:
            image_path = os.path.join(image_dir, filename)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            original_shapes.append(image.shape) # Store original (h, w)

            windowed_image = apply_liver_window_batch(image)
            image_bgr = cv2.cvtColor(windowed_image, cv2.COLOR_GRAY2BGR)
            
            input_image = cv2.resize(image_bgr, (256, 256)) / 255.0
            input_tensor = torch.from_numpy(input_image.transpose(2, 0, 1)).float()
            batch_input_tensors.append(input_tensor)

        # Stack all tensors into a single batch and send to GPU
        batch = torch.stack(batch_input_tensors).to(device)

        with torch.no_grad():
            masks = model(batch)
            masks = torch.sigmoid(masks).cpu().numpy()

        # Process results for each image in the batch
        for j, mask in enumerate(masks):
            mask = mask.squeeze()
            original_h, original_w = original_shapes[j]
            mask = cv2.resize(mask, (original_w, original_h))

            binary_mask = (mask > 0.5).astype(np.uint8)
            contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                if cv2.contourArea(largest_contour) > 100: # Area threshold
                    x, y, w, h = cv2.boundingRect(largest_contour)
                    
                    x_center = (x + w / 2) / original_w
                    y_center = (y + h / 2) / original_h
                    norm_w = w / original_w
                    norm_h = h / original_h
                    
                    yolo_annotation = f"0 {x_center} {y_center} {norm_w} {norm_h}"
                    annotation_filename = os.path.splitext(batch_files[j])[0] + ".txt"
                    annotation_path = os.path.join(image_dir, annotation_filename)
                    
                    with open(annotation_path, "w") as f:
                        f.write(yolo_annotation)

    print("\nAuto-annotation process complete!")
    print("Please review the generated boxes in labelImg.")

if __name__ == "__main__":
    try:
        from tqdm import tqdm
    except ImportError:
        print("TQDM library not found. Installing...")
        os.system("pip install tqdm")
        from tqdm import tqdm

    auto_generate_annotations_batch(IMAGE_DIR)