# balance_data.py

import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle

train_data = np.load('training_data.npy')

df = pd.DataFrame(train_data)
print(df.head())
print(Counter(df[1].count()))

lefts = []
rights = []
forwards = []

shuffle(train_data)

for data in train_data:
    img = data[0]
    choice = data[1]

    if choice == [1,0,0]:
        lefts.append([img,choice])
    elif choice == [0,1,0]:
        forwards.append([img,choice])
    elif choice == [0,0,1]:
        rights.append([img,choice])
    else:
        print('no matches')


train_len = len(min(lefts,rights)) #take the len of which ever list is shorter & reduce to that
forwards = forwards[:train_len]
lefts = lefts[:train_len]
rights = rights[:train_len]

final_data = forwards + lefts + rights
shuffle(final_data)

np.save('training_data.npy', final_data)




