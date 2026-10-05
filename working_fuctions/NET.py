import torch
import torch.nn as nn

class ResidualBlock(nn.Module): #A sub network which work as a deep hidden layer
    def __init__(self):
        super().__init__()

        self.Conv1 = nn.Conv2d(64,64,kernel_size=3,padding=1)# conv layer1 converts linear data into 2D
        self.Batch1 = nn.BatchNorm2d(64)

        self.Conv2 = nn.Conv2d(64,64,kernel_size=3,padding=1)# conv layer1 converts linear data into 2D
        self.Batch2 = nn.BatchNorm2d(64)

    def forward(self,x):
        residual = x #saves the input to skip connection and add it with output

        x = torch.relu(self.Batch1(self.Conv1(x)))# usages relu instand of sigmoid

        x = self.Batch2(self.Conv2(x))

        x += residual#adds original input to the output

        x = torch.relu(x)# usages relu instand of sigmoid

        return x
    
class ChessNet(nn.Module):
    def __init__(self):
        super().__init__()
        # it is the main layer of chess network which usages one layer of network and gives 64 outputs for 5 residual blocks
        self.Conv1 = nn.Conv2d(19,64,kernel_size=3,padding=1)
        self.moduls = nn.ModuleList([ResidualBlock() for _ in range(5)])
        #policy head usage the output given by the chess network and turn it into linear form of data which tell what move are the best
        self.policyConv1 = nn.Conv2d(64,2,kernel_size=1)
        self.policyBatch1 = nn.BatchNorm2d(2)
        self.policylayer1 = nn.Linear(128,4096)#turns the data into linear from 
        #value head usage the output given by the chess network and turn it into linear form of data(+1,-1) which tell who is winning
        self.valueConv1 = nn.Conv2d(64,1,kernel_size=1)
        self.valueBatch1 = nn.BatchNorm2d(1)
        self.valuelayer1 = nn.Linear(64,64)#turns the data into linear from
        self.valuelayer2 = nn.Linear(64,1)

    def forward(self,inputdata):
        #it simply run the first layer of chess network and the 5 residual block
        output_data = torch.relu(self.Conv1(inputdata))
        for module in self.moduls:
            output_data = module(output_data)
        #run the policy calculation
        policydata = torch.relu(self.policyBatch1(self.policyConv1(output_data)))
        Pbatch = policydata.size(0)
        policydata_Flattened = policydata.view(Pbatch,-1)
        Policy_output = self.policylayer1(policydata_Flattened)

        #run the value calculation
        valuedata = torch.relu(self.valueBatch1(self.valueConv1(output_data)))
        Vbatch = valuedata.size(0)
        valuedata_Flattened1 = valuedata.view(Vbatch,-1)
        valuedata_Flattened2 = torch.relu(self.valuelayer1(valuedata_Flattened1))
        Value_output = torch.tanh(self.valuelayer2(valuedata_Flattened2))

        return Policy_output, Value_output #give a prediction(output) of policy and value
        
CHESSmodel = ChessNet()

value_loss_output = nn.MSELoss()#loss fuction for the value 
policy_loss_output = nn.CrossEntropyLoss()#loss fuction for the policy

optimizer = torch.optim.Adam(CHESSmodel.parameters(),lr=0.001)
iteration = 0 #how many time it has run
dataset = []
for loop in range(10000):#run the network 10000 times
    iteration += 1
    print(f"iteration:{iteration}")

    for batch_x, batch_y, batch_z in dataset:#get the there data which is x(the moves from MCTS), y(the correct policy ), z(the correct value)

        optimizer.zero_grad()

        Policy_output,Value_output = CHESSmodel(batch_x) #give the input to chess network and gets the policy and value output


        Policy_loss = policy_loss_output(Policy_output,batch_y)#compares the policy output with y

        Value_loss = value_loss_output(Value_output,batch_z)#compares the value output with z

        total_loss = Value_loss + Policy_loss #gets the total loss

        total_loss.backward() #the simplay process of backpropogation the optimizer
        optimizer.step()