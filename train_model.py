import numpy as np

import tf2_processing
from build_models import build_alexnet

WIDTH = 480
HEIGHT = 270
LR = 1e-3
EPOCHS = 30

model = build_alexnet(width=WIDTH, height=HEIGHT, output=9)
data = np.load("./collected_data/training_data-1.npy", allow_pickle=True)
X_train, X_test, Y_train, Y_test = tf2_processing.process(data=data, WIDTH= WIDTH, HEIGHT=HEIGHT)


model.compile(optimizer="rmsprop", loss="categorical_crossentropy")
model.fit(X_train, Y_train, epochs=10)
model.save("./models/model_alexnet_V0_500e_500i")
loss, acc =model.evaluate(X_test, Y_test)
print("acc: ", acc)
