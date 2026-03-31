import torch
import torch.nn as nn

class TumorClassifier(nn.Module):
    """A CNN for multi-class classification of tumor types."""
    def __init__(self, num_classes):
        super(TumorClassifier, self).__init__()
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
        
        # A dummy forward pass to calculate flattened size
        dummy_input = torch.zeros(1, 3, 224, 224)
        dummy_output = self.conv_layers(dummy_input)
        flattened_size = dummy_output.view(1, -1).shape[1]

        self.fc_layers = nn.Sequential(
            nn.Linear(flattened_size, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = self.flatten(x)
        x = self.fc_layers(x)
        return x