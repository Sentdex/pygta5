# balance_data.py

import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
from settings import (
 LEFT,
 FORWARD,
 RIGHT
)

train_data = np.load('training_data.npy')

df = pd.DataFrame(train_data)
print(df.head())
print(Counter(df[1].apply(str)))

lefts = []
rights = []
forwards = []

shuffle(train_data)

for data in train_data:
    img = data[0]
    choice = data[1]

    if choice == LEFT:
        lefts.append([img, choice])
    elif choice == FORWARD:
        forwards.append([img, choice])
    elif choice == RIGHT:
        rights.append([img, choice])
    else:
        print('no matches')

forwards = forwards[:len(lefts)][:len(rights)]
lefts = lefts[:len(forwards)]
rights = rights[:len(forwards)]

final_data = forwards + lefts + rights
shuffle(final_data)

np.save('training_data.npy', final_data)
