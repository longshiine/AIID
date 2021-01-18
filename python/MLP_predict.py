import pandas as pd
import numpy as np
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import torch
from torch.utils.data import Dataset, DataLoader
import torch.optim as torch_optim
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
from datetime import datetime

train = pd.read_csv('data/animal/train.csv')
test = pd.read_csv('data/animal/test.csv')

train_X = train.drop(columns= ['OutcomeType', 'OutcomeSubtype', 'AnimalID'])
Y = train['OutcomeType']
test_X = test

stacked_df = train_X.append(test_X.drop(columns=['ID']))
stacked_df = stacked_df.drop(columns=['DateTime'])

for col in stacked_df.columns:
    if stacked_df[col].isnull().sum() > 10000:
        print("dropping", col, stacked_df[col].isnull().sum())
        stacked_df = stacked_df.drop(columns = [col])