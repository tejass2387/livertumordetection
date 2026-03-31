import torch
import torch.optim as optim
import torch.nn as nn
from . import config
from .dataset import get_data_loaders
from .model import SimpleCNN

def train_model():
    """Main function to train the model."""
    print("INFO: Loading data...")
    train_loader, _, _ = get_data_loaders()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"INFO: Using '{device}' for training.")
    
    # Pass the number of classes to the model
    model = SimpleCNN(num_classes=config.NUM_CLASSES).to(device)
    
    # Use CrossEntropyLoss for multi-class classification
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=config.LEARNING_RATE)

    print("INFO: Starting model training...")
    for epoch in range(config.EPOCHS):
        model.train()
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
        print(f"Epoch [{epoch+1}/{config.EPOCHS}], Loss: {epoch_loss:.4f}")

    print("INFO: Training complete.")
    
    torch.save(model.state_dict(), config.MODEL_PATH)
    print(f"INFO: Model saved successfully at {config.MODEL_PATH}")

if __name__ == '__main__':
    train_model()