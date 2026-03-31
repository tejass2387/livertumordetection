import torch
import torch.optim as optim
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from src.classifier_model import TumorClassifier

# --- Configuration ---
# IMPORTANT: Update this path to your new labeled dataset
DATA_DIR = "data_classifier/train"
MODEL_SAVE_PATH = "models/tumor_classifier.pth"
NUM_CLASSES = 3  # Update this to the number of tumor types you have
BATCH_SIZE = 32
EPOCHS = 30
# --- End Configuration ---

def train_classifier():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"INFO: Using '{device}' for training.")

    data_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_dataset = datasets.ImageFolder(DATA_DIR, transform=data_transform)
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    
    model = TumorClassifier(num_classes=NUM_CLASSES).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    print("INFO: Starting classifier training...")
    for epoch in range(EPOCHS):
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * inputs.size(0)
        
        epoch_loss = running_loss / len(train_loader.dataset)
        print(f"Epoch [{epoch+1}/{EPOCHS}], Loss: {epoch_loss:.4f}")

    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print(f"INFO: Classifier model saved to {MODEL_SAVE_PATH}")

if __name__ == '__main__':
    train_classifier()