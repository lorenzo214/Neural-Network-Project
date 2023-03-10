# -*- coding: utf-8 -*-
import torch
from torch import nn

class SRNNHidden(nn.Module):
  def __init__(self, inputSize, hiddenSize, numLayer, outputSize):
    super().__init__()
    self.gatBranch = nn.Linear(inputSize,hiddenSize)
    listaLayer = [nn.Linear(inputSize,hiddenSize),nn.ReLU()]
    for i in range(numLayer-1):
      listaLayer.append(nn.Linear(hiddenSize,hiddenSize))
      listaLayer.append(nn.ReLU())
    self.fr = nn.Sequential(*listaLayer)
    self.wp = torch.cat((torch.eye(hiddenSize)[1:],torch.eye(hiddenSize)[0].reshape(1,hiddenSize)))
    self.lastLayer = nn.Linear(hiddenSize,outputSize)
    self.inputSize = inputSize

  def forward(self, x, h = None):
    batchSize = x.shape[0]
    if self.inputSize == 1:
      x = torch.tensor(torch.reshape(x,(batchSize,1)),dtype=torch.float)
    if h == None:
      h = self.fr(x)*torch.sigmoid(self.gatBranch(x))
    else:
      h = torch.matmul(h,self.wp)+self.fr(x)*torch.sigmoid(self.gatBranch(x))
      
    return self.lastLayer(h),h


class SRNN(nn.Module):
  def __init__(self, inputSize, hiddenSize, numLayer, outputSize):
    super().__init__()
    self.srnnHidden = SRNNHidden(inputSize, hiddenSize, numLayer, outputSize)
    

  def forward(self, x):
    lenRNN = x.shape[1]
    h = None
    for i in range(lenRNN):
      lastLayer , h = self.srnnHidden(x[:,i],h) 
    return lastLayer, h
