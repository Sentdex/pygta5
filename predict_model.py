import numpy as np
import tensorflow as tf

import tf2_processing

model = tf.keras.models.load_model("./models/model_alexnet_V0_500e_500i")

image = np.load("./collected_data/training_data-1.npy", allow_pickle=True)[460][0]
image = tf2_processing.process_img(image)

prediction = model.predict(image)
print(prediction)
