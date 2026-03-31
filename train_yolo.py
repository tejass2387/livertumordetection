from ultralytics import YOLO

# Load a pre-trained YOLOv8 model to start from
# 'n' is for nano, the smallest and fastest version.
model = YOLO('yolov8n.pt')  

# Train the model using your custom data
if __name__ == '__main__':
    results = model.train(
        data='data.yaml',       # Path to your dataset configuration file
        epochs=50,              # Number of times to go through the data
        imgsz=640,              # Image size for training
        device=0,               # Use the first available GPU (device=0)
        patience=5              # Stop training early if no improvement is seen
    )