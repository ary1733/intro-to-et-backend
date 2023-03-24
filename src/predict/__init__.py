from flask import Blueprint
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms

predict_blueprint = Blueprint('predict',__name__,url_prefix="/api/v1/predict")

# Note that the id's 0,1,2,3..
# here are not the same id in the database
labels_map =  {
    "0":	"fallen-tree" ,
    "1":	"road" ,
    "2":	"garbage" ,
    "3":	"pothole"
}

batch_size = 4
transform = transforms.Compose([
	transforms.Resize(640),
	transforms.RandomCrop(640),
	transforms.RandomHorizontalFlip(),
	transforms.ToTensor(),
	transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Define a convolution neural network
class Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=12, kernel_size=5, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(12)
        self.conv2 = nn.Conv2d(in_channels=12, out_channels=12, kernel_size=5, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(12)
        self.pool = nn.MaxPool2d(2,2)
        self.conv4 = nn.Conv2d(in_channels=12, out_channels=24, kernel_size=5, stride=1, padding=1)
        self.bn4 = nn.BatchNorm2d(24)
        self.conv5 = nn.Conv2d(in_channels=24, out_channels=24, kernel_size=5, stride=1, padding=1)
        self.bn5 = nn.BatchNorm2d(24)
        self.conv6 = nn.Conv2d(in_channels=24, out_channels=24, kernel_size=5, stride=1, padding=1)
        self.bn6 = nn.BatchNorm2d(24)
     
        self.fc1 = nn.Linear(24*314*314, 4)
        # 24*10*10 => C*H*W => C = channel
        # 4 is no of classes

    def forward(self, input):
        # print(input.shape)
        output = F.relu(self.bn1(self.conv1(input)))      
        output = F.relu(self.bn2(self.conv2(output)))     
        output = self.pool(output)                        
        output = F.relu(self.bn4(self.conv4(output)))     
        output = F.relu(self.bn5(self.conv5(output)))     
        # print(output.shape)
        """
        Note 24*314*314 got for 640x640 images
        So if you want to train on different size
        dataset uncomment print(output.size) and update
        both in forward and init
        """
        """
        we got 4D matrix from batch of images
        4x24x10x10 this is a 4D matrix
        => output.view(-1, 24*10*10)
        => 4x2400 
        we converted this to 2D matrix

        Now linear will change as g((W^T)*x+b)
        g => ReLU
        x => 4x2400
        W => 2400x8
        W^T => 8x2400
        b => 8x1

        each x is actually 2400x1 
        4 is the batch size. So,
        (W^T)*x will be 8x1

        and b is 8x1

        both will be added

        and the result be resulted in 
        4x8 as 4 is the batch size
        """
        output = output.view(-1, 24*314*314)
        #output = output.view(24*10*10,-1)
        output = self.fc1(output)

        return output

model = Network()
model.load_state_dict(torch.load("model.pth",map_location=torch.device(device)))
model.eval()

# This import might seem unconventional, however is required to register your
# routes, which are created.
from src.predict import controller