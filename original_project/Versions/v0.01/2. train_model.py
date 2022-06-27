import numpy as np
from alexnet import alexnet2
from random import shuffle
import pandas as pd

# what to start at
START_NUMBER = 60

# what to end at
hm_data = 111

# use a previous model to begin?
START_FRESH = False

WIDTH = 160
HEIGHT = 120
LR = 1e-3
EPOCHS = 1
MODEL_NAME = ''
EXISTING_MODEL_NAME = ''

model = alexnet2(WIDTH, HEIGHT, LR, output=9)

if not START_FRESH:
    model.load(EXISTING_MODEL_NAME)

for i in range(EPOCHS):
    data_order = [i for i in range(START_NUMBER,hm_data+1)]
    shuffle(data_order)
    for i in data_order:
        train_data = np.load('training_data-{}.npy'.format(i))
        
        df = pd.DataFrame(train_data)
        df = df.iloc[np.random.permutation(len(df))]
        train_data = df.values.tolist()

        train = train_data[:-100]
        test = train_data[-100:]

        X = np.array([i[0] for i in train]).reshape(-1,WIDTH,HEIGHT,1)
        Y = [i[1] for i in train]

        test_x = np.array([i[0] for i in test]).reshape(-1,WIDTH,HEIGHT,1)
        test_y = [i[1] for i in test]

        model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}), 
            snapshot_step=2500, show_metric=True, run_id=MODEL_NAME)

        model.save(MODEL_NAME)

# tensorboard --logdir=foo:C:/Users/H/Desktop/ai-gaming-phase5/log
