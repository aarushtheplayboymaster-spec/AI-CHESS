import torch
import torch.nn as nn
x = torch.tensor([[0.1,0.5,0.7,0.0,0.3]])
y = nn.Linear(in_features=5,out_features=5)
with torch.no_grad():
    y.bias.copy_(torch.tensor([0.2,0.5,0.6,0.9,0.2]))
output  = y(x)
