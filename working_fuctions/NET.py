import torch
import torch.nn as nn
class ResidualBlock(nn.Module):
    def __init__(self):
        super().__init__()
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
    
class ChessNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.Conv1 = nn.Conv2d(19,64,kernel_size=3,padding=1)
        self.moduls = nn.ModuleList([ResidualBlock() for _ in range(5)])

        self.policyConv1 = nn.Conv2d(64,2,kernel_size=1)
        self.policyBatch1 = nn.BatchNorm2d(2)
        self.policylayer1 = nn.Linear(128,4096)

        self.valueConv1 = nn.Conv2d(64,1,kernel_size=1)
        self.valueBatch1 = nn.BatchNorm2d(1)
        self.valuelayer1 = nn.Linear(64,64)
        self.valuelayer2 = nn.Linear(64,1)

    def forward(self,inputdata):
        output_data = torch.relu(self.Conv1(inputdata))
        for module in self.moduls:
            output_data = module(output_data)

        policydata = torch.relu(self.policyBatch1(self.policyConv1(output_data)))
        batch = policydata.size(0)
        policydata_Flattened = policydata.view(batch,-1)
        Policy_output = self.policylayer1(policydata_Flattened)

        valuedata = torch.relu(self.valueBatch1(self.valueConv1(output_data)))
        batch = valuedata.size(0)
        valuedata_Flattened1 = valuedata.view(batch,-1)
        valuedata_Flattened2 = torch.relu(self.valuelayer1(valuedata_Flattened1))
        Value_output = torch.tanh(self.valuelayer2(valuedata_Flattened2))

        return Policy_output, Value_output
        
CHESSmodel = ChessNet()

value_loss_output = nn.MSELoss()
policy_loss_output = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(CHESSmodel.parameters(),lr=0.001)
iteration = 0

for loop in range(10000):
    iteration += 1
    print(f"iteration:{iteration}")
    for batch_x, batch_y, batch_z in dataset:

        optimizer.zero_grad()

        Policy_output,Value_output = CHESSmodel(batch_x)


        Policy_loss = policy_loss_output(Policy_output,batch_y)

        Value_loss = value_loss_output(Value_output,batch_z)

        total_loss = Value_loss + Policy_loss
        total_loss.backward()
        optimizer.step()












    

