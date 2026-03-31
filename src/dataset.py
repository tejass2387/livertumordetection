import os
import cv2
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from . import config

class LiverDataset(Dataset):
    """Custom Dataset for loading multi-class tumor images."""
    def __init__(self, image_dir, transform=None):
        self.image_dir = image_dir
        self.transform = transform
        self.image_paths = []
        self.labels = []
        
        # Dynamically find class names from the subdirectories
        self.class_names = sorted(os.listdir(image_dir))
        
        for label, category in enumerate(self.class_names):
            category_dir = os.path.join(self.image_dir, category)
            if not os.path.isdir(category_dir):
                continue
            for image_name in os.listdir(category_dir):
                self.image_paths.append(os.path.join(category_dir, image_name))
                self.labels.append(label)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Use LongTensor for CrossEntropyLoss
        label = torch.tensor(self.labels[idx], dtype=torch.long)

        if self.transform:
            image = self.transform(image)
        
        return image, label

def get_data_loaders():
    """Returns training and testing data loaders."""
    data_transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((config.IMAGE_HEIGHT, config.IMAGE_WIDTH)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_dataset = LiverDataset(config.TRAIN_DIR, transform=data_transform)
    test_dataset = LiverDataset(config.TEST_DIR, transform=data_transform)

    train_loader = DataLoader(train_dataset, batch_size=config.BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=config.BATCH_SIZE, shuffle=False)
    
    return train_loader, test_loader, train_dataset.class_names