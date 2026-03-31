# --- File Paths ---
TRAIN_DIR = "data/train"
TEST_DIR = "data/test"
MODEL_PATH = "models/multi_class_detector.pth" # New model name

# --- Image Parameters ---
IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224

# --- Training Hyperparameters ---
NUM_CLASSES = 4 # IMPORTANT: We now have 4 categories
BATCH_SIZE = 32
EPOCHS = 30 # Let's train for a few more epochs
LEARNING_RATE = 0.001