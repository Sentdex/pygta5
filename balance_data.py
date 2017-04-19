# balance_data.py

import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle

train_data = np.load('training_data.npy')

df = pd.DataFrame(train_data)
print(df.head())
print(Counter(df[1].apply(str)))

CHOICE_LEFT = [1, 0, 0]
CHOICE_FORWARD = [0, 1, 0]
CHOICE_RIGHT = [0, 0, 1]

lefts = []
rights = []
forwards = []

shuffle(train_data)

for data in train_data:
    img = data[0]
    choice = data[1]

    if choice == CHOICE_LEFT:
        lefts.append([img, choice])
    elif choice == CHOICE_FORWARD:
        forwards.append([img, choice])
    elif choice == CHOICE_RIGHT:
        rights.append([img, choice])
    else:
        print('no matches')

forwards = forwards[:len(lefts)][:len(rights)]
lefts = lefts[:len(forwards)]
rights = rights[:len(forwards)]

final_data = forwards + lefts + rights
shuffle(final_data)

np.save('training_data.npy', final_data)
