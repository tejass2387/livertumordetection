import os
import cv2
import torch
from ultralytics import YOLO
from torchvision import transforms
from .classifier_model import TumorClassifier

# --- Model Paths ---
YOLO_MODEL_PATH = 'runs/detect/train3/weights/best.pt'
CLASSIFIER_MODEL_PATH = 'models/tumor_classifier.pth'
NUM_CLASSES = 3
CLASSIFIER_CLASS_NAMES = ['Adenoma', 'Focal Nodular Hyperplasia', 'Hemangioma']

# --- Load Models with Safety Checks ---
# Check for and load the YOLO model
if not os.path.exists(YOLO_MODEL_PATH):
    raise FileNotFoundError(f"YOLO model not found at: {YOLO_MODEL_PATH}. Please make sure you have trained the YOLO model and the path is correct.")
yolo_model = YOLO(YOLO_MODEL_PATH)

# Check for and load the classifier model
if not os.path.exists(CLASSIFIER_MODEL_PATH):
    raise FileNotFoundError(f"Classifier model not found at: {CLASSIFIER_MODEL_PATH}. Please run train_classifier.py.")
classifier_model = TumorClassifier(num_classes=NUM_CLASSES)
classifier_model.load_state_dict(torch.load(CLASSIFIER_MODEL_PATH, map_location='cpu'))
classifier_model.eval()

# --- Prediction Function ---
def get_full_prediction(image_path, output_dir='static/uploads'):
    detection_status = "No Tumor Detected"
    tumor_type = "N/A"
    
    image = cv2.imread(image_path)
    base_filename = os.path.basename(image_path)
    result_filename = base_filename

    # Step 1: Run YOLO Detection
    results = yolo_model(image, conf=0.5)

    for r in results:
        if len(r.boxes) > 0:
            detection_status = "Tumor Detected"
            
            result_image_array = r.plot()
            result_filename = f"detected_{base_filename}"
            cv2.imwrite(os.path.join(output_dir, result_filename), result_image_array)

            # Step 2: Run Classifier on the detected tumor
            box = r.boxes[0].xyxy[0].cpu().numpy().astype(int)
            x1, y1, x2, y2 = box
            
            cropped_tumor = image[y1:y2, x1:x2]
            
            transform = transforms.Compose([
                transforms.ToPILImage(),
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            input_tensor = transform(cropped_tumor).unsqueeze(0)
            
            with torch.no_grad():
                outputs = classifier_model(input_tensor)
                _, predicted_idx = torch.max(outputs, 1)
                tumor_type = CLASSIFIER_CLASS_NAMES[predicted_idx.item()]
    
    return result_filename, detection_status, tumor_type