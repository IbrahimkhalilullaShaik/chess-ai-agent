import torch
import torch.nn as nn
import torch.nn.functional as F

class ChessNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(12, 64, 3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, 3, padding=1)

        self.policy_head = nn.Linear(128 * 8 * 8, 4672)
        self.value_head = nn.Linear(128 * 8 * 8, 1)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = x.view(x.size(0), -1)

        policy = self.policy_head(x)
        value = torch.tanh(self.value_head(x))

        return policy, value