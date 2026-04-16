import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models

class BaselineCNN(nn.Module):
    """Simple CNN for baseline performance."""
    def __init__(self, num_classes: int):
        super(BaselineCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(16 * 112 * 112, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = x.view(-1, 16 * 112 * 112)
        x = self.fc1(x)
        return x

class AdvancedModel(nn.Module):
    """Transfer learning with ResNet18."""
    def __init__(self, num_classes: int):
        super(AdvancedModel, self).__init__()
        self.model = models.resnet18(pretrained=True)
        # Freeze early layers
        for param in self.model.parameters():
            param.requires_grad = False
        
        # Replace final head
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, num_classes)

    def forward(self, x):
        return self.model(x)

def save_model(model, path):
    torch.save(model.state_dict(), path)

def load_model(model, path, device='cpu'):
    model.load_state_dict(torch.load(path, map_location=device))
    return model
