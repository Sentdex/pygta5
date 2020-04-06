import numpy as np
import tensorflow as tf
from tensorflow.keras import activations
from tensorflow.keras.layers import *


def build_alexnet(width, height, output = 9):
    inputs = tf.keras.Input(shape=np.array([width, height, 1]).squeeze())

    x = Conv2D(96, 11, 4, padding='same')(inputs)
    x = BatchNormalization()(x)
    x = MaxPooling2D(3, 2)(x)

    x = Conv2D(256, 5, 1, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = MaxPooling2D(3, 2)(x)

    x = Conv2D(384, 3, 1, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    x = Conv2D(384, 3, 1, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    x = Conv2D(256, 3, 1, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = MaxPooling2D(3, 2)(x)

    x = Flatten()(x)

    x = Dense(4096)(x)
    x = ReLU()(x)
    x = Dropout(0.5)(x)
    x = Dense(4096)(x)
    x = ReLU()(x)
    x = activations.tanh(x)
    x = Dropout(0.5)(x)

    x = Dense(output)(x)
    outputs = Softmax()(x)

    return tf.keras.Model(inputs, outputs)