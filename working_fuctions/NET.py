import torch
import torch.nn as nn
class ResidualBlock(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden = nn.Conv2d(19,64)
        self.filter = nn.Conv2d(64)
    def forward(self,x):
        x = self.hidden(x)
        x = self.filter(x)
        return x

modul_Res = ResidualBlock()
class CHESS_engine(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden = nn.Conv2d(19,64)


