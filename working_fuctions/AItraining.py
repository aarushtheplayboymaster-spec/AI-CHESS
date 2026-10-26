import torch
import torch.nn as nn
from NET import ChessNet
from dataset import CHESS_DATASET_LODEAR
from torch.utils.data import DataLoader
from tqdm import tqdm
import os
def train():
        CHESSmodel = ChessNet()

        checkpoint_save_path = "check_point_chess_model_weights.pt"
        if os.path.exists(checkpoint_save_path):
                print("your weights has been found")
                CHESSmodel.load_state_dict(torch.load(checkpoint_save_path))
                print("starting the training form 1")
        else:
                print("NO checkpoint has been found starting you 0")


        value_loss_output = nn.MSELoss()#loss fuction for the value 
        policy_loss_output = nn.CrossEntropyLoss()#loss fuction for the policy

        optimizer = torch.optim.Adam(CHESSmodel.parameters(),lr=0.001)

        chessdata = CHESS_DATASET_LODEAR("AI-CHESS/assates/lichess_db_standard_rated_2013-01.pgn")
        dataset = DataLoader(chessdata,batch_size=64,shuffle=True,num_workers=2)
        for loop in range(1000):#run the network 10000 times
                for batch_x, batch_y, batch_z in tqdm(dataset, desc=f"Epoch {loop}"):#get the there data which is x(the moves from MCTS), y(the correct policy ), z(the correct value)
                        optimizer.zero_grad()

                        Policy_output,Value_output = CHESSmodel(batch_x) #give the input to chess network and gets the policy and value output


                        Policy_loss = policy_loss_output(Policy_output,batch_y.squeeze())#compares the policy output with y
                        batch_z = batch_z.unsqueeze(1)
                        Value_loss = value_loss_output(Value_output,batch_z)#compares the value output with z

                        total_loss = Value_loss + Policy_loss #gets the total loss

                        total_loss.backward() #the simplay process of backpropogation the optimizer
                        optimizer.step()
        
                print(f"iteration:{loop + 1}")
                if loop % 5 == 0:
                        torch.save(CHESSmodel.state_dict(), checkpoint_save_path)
                        print(f"checkpoint Model weights successfully saved to {checkpoint_save_path}!")

        save_path = "chess_model_weights.pt"
        torch.save(CHESSmodel.state_dict(), save_path)
        print(f"Model weights successfully saved to {save_path}!")
if __name__ == "__main__":
        train()

