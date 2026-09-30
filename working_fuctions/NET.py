import torch
import torch.nn as nn
class ResidualBlock(nn.Module):
    def __int__(self):
        super().__init__(self)
        self.Conv1 = nn.Conv2d(64,64,kernel_size=3,padding=1)
        self.Batch1 = nn.BatchNorm2d(64)
        self.Conv2 = nn.Conv2d(64,64,kernel_size=3,padding=1)
        self.Batch2 = nn.BatchNorm2d(64)
    def forward(self,x):
        residual = x
        x = torch.relu(self.Batch1(self.Conv1(x)))
        x = self.Batch2(self.Conv2(x))
        x += residual
        x = torch.relu(x)
        return x
    
class ChessNet(nn.ModuleList):
    def __int__(self):
        super().__init__(self)
        self.Conv1 = nn.Conv2d(19,67,kernel_size=3,padding=1)
        self.moduls = ([self.Conv1,ResidualBlock()])
    def forward(self,x):
        for module in self.moduls:
            x = module(x)
            return x
        
class Policy(ChessNet):
    def __int__(self):
        super().__int__()
        self.conv1 = nn.Conv2d(64,2,kernel_size=1)
        self.Batch = nn.BatchNorm2d(2)
        self.layer = nn.Linear(128,4096)
    def forward(self, x):
         x = torch.relu(self.Batch(self.conv1(x)))
         batch = x.size(0)
         x_Flattened = x.view(batch,128)
         Policyhead = self.layer(x_Flattened)
         return Policyhead
    
class Value(ChessNet):
    def __int__(self):
        super().__int__()
        self.conv1 = nn.Conv2d(64,1,kernel_size=1)
        self.Batch = nn.BatchNorm2d(1)
        self.layer1 = nn.Linear(64,64)
        self.layer2 = nn.Linear(64,1)
    def forward(self, x):
        x = torch.relu(self.Batch(self.conv1(x)))
        batch = x.size(0)
        x_Flattened = x.view(batch,128)
        x = torch.relu(self.layer1(x_Flattened))
        Valuehead = torch.tanh(self.layer2(x))
        return Valuehead

CHESSmodel = ChessNet()
Policymodel = Policy()
Valuemodel = Value()
value_loss_output = nn.MSELoss()
policy_loss_output = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(CHESSmodel.parameters(),lr=0.5)

x = 1
real_value = 1
real_policy = 1

input1 = CHESSmodel(x)
Policy_output = Policymodel(input1)
Value_output =  Valuemodel(input1)

Value_loss = value_loss_output(Value_output,real_value)
Policy_loss = policy_loss_output(Policy_output,real_policy)
total_loss = Value_loss + Policy_loss
total_loss.backward()
optimizer.step()





    

