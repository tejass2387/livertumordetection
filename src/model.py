import torch
import torch.nn as nn
from . import config

class SimpleCNN(nn.Module):
    """A simple CNN for multi-class image classification."""
    def __init__(self, num_classes):
        super(SimpleCNN, self).__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )
        self.flatten = nn.Flatten()
        
        dummy_input = torch.zeros(1, 3, config.IMAGE_HEIGHT, config.IMAGE_WIDTH)
        dummy_output = self.conv_layers(dummy_input)
        flattened_size = dummy_output.view(1, -1).shape[1]

        self.fc_layers = nn.Sequential(
            nn.Linear(flattened_size, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            # Output layer now has `num_classes` outputs
            nn.Linear(512, num_classes) 
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = self.flatten(x)
        x = self.fc_layers(x)
        return x