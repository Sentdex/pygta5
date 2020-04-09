import random

import numpy as np

import tf2_processing
from build_models import AlexNet

WIDTH = 480
HEIGHT = 270
LR = 1e-3
EPOCHS = 30
n_training_set = 14

# model = tf.keras.models.load_model("./models/alexnet10")
model = AlexNet()
model.compile(optimizer="rmsprop", loss="categorical_crossentropy")


for e in range(EPOCHS):
    data_order = [i for i in range(1, n_training_set + 1)]
    random.shuffle(data_order)
    for count, i in enumerate(data_order):

        try:
            file_name = './tf_dataset/data/training_data-{}.npy'.format(i)
            # full file info
            train_data = tf2_processing.process(file_name)
            target_data = np.load("./tf_dataset/target/target_data-{}.npy".format(i))
            print('training_data-{}.npy'.format(i), len(train_data))

            X_train = train_data[:-10]
            y_train = target_data[:-10]
            X_test = train_data[-10:]
            y_test = np.array(target_data[-10:])

            model.fit(X_train, y_train, n_epoch=1, validation_data=(X_test, y_test))

            if count % 10 == 0:
                print(count, ' SAVING MODEL!')
                model.save("./models/alexnet{}".format(count))

        except Exception as e:
            print(str(e))
