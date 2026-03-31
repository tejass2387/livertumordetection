import torch
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from . import config
from .dataset import get_data_loaders
from .model import SimpleCNN

def evaluate_model():
    print("INFO: Loading test data for evaluation...")
    # Get the test_loader and the class names
    _, test_loader, class_names = get_data_loaders()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Make sure to load the multi-class model
    model = SimpleCNN(num_classes=config.NUM_CLASSES).to(device)
    model.load_state_dict(torch.load(config.MODEL_PATH, map_location=device))
    model.eval() # Set model to evaluation mode

    all_preds = []
    all_labels = []

    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            
            # Get the index of the highest score for multi-class
            _, preds = torch.max(outputs, 1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    print("\n--- Classification Report ---")
    print(classification_report(all_labels, all_preds, target_names=class_names))
    
    # Optional: Display a confusion matrix to visualize results
    print("--- Confusion Matrix ---")
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='g', xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.show()


if __name__ == '__main__':
    evaluate_model()