# import numpy as np
# import tensorflow as tf
# from tensorflow.keras import activations
# from tensorflow.keras.layers import *
#
# def build_alexnet(width, height, output=9):
#     inputs = tf.keras.Input(shape=np.array([height, width, 1]).squeeze())
#
#     x = Conv2D(96, 11, 4, padding='same')(inputs)
#     x = BatchNormalization()(x)
#     x = MaxPooling2D(3, 2)(x)
#
#     x = Conv2D(256, 5, 1, padding='same')(x)
#     x = BatchNormalization()(x)
#     x = ReLU()(x)
#     x = MaxPooling2D(3, 2)(x)
#
#     x = Conv2D(384, 3, 1, padding='same')(x)
#     x = BatchNormalization()(x)
#     x = ReLU()(x)
#
#     x = Conv2D(384, 3, 1, padding='same')(x)
#     x = BatchNormalization()(x)
#     x = ReLU()(x)
#
#     x = Conv2D(256, 3, 1, padding='same')(x)
#     x = BatchNormalization()(x)
#     x = ReLU()(x)
#     x = MaxPooling2D(3, 2)(x)
#
#     x = Flatten()(x)
#
#     x = Dense(4096)(x)
#     x = ReLU()(x)
#     x = Dropout(0.5)(x)
#     x = Dense(4096)(x)
#     x = ReLU()(x)
#     x = activations.tanh(x)
#     x = Dropout(0.5)(x)
#
#     x = Dense(output)(x)
#     outputs = Softmax()(x)
#
#     return tf.keras.Model(inputs, outputs)



import tensorflow as tf

def AlexNet(image_width = 480, image_height = 270, channels = 1, NUM_CLASSES = 9):
    model = tf.keras.Sequential([
        # layer 1
        tf.keras.layers.Conv2D(filters=96,
                               kernel_size=(11, 11),
                               strides=4,
                               padding="valid",
                               activation=tf.keras.activations.relu,
                               input_shape=(image_height, image_width, channels)),
        tf.keras.layers.MaxPool2D(pool_size=(3, 3),
                                  strides=2,
                                  padding="valid"),
        tf.keras.layers.BatchNormalization(),
        # layer 2
        tf.keras.layers.Conv2D(filters=256,
                               kernel_size=(5, 5),
                               strides=1,
                               padding="same",
                               activation=tf.keras.activations.relu),
        tf.keras.layers.MaxPool2D(pool_size=(3, 3),
                                  strides=2,
                                  padding="same"),
        tf.keras.layers.BatchNormalization(),
        # layer 3
        tf.keras.layers.Conv2D(filters=384,
                               kernel_size=(3, 3),
                               strides=1,
                               padding="same",
                               activation=tf.keras.activations.relu),
        # layer 4
        tf.keras.layers.Conv2D(filters=384,
                               kernel_size=(3, 3),
                               strides=1,
                               padding="same",
                               activation=tf.keras.activations.relu),
        # layer 5
        tf.keras.layers.Conv2D(filters=256,
                               kernel_size=(3, 3),
                               strides=1,
                               padding="same",
                               activation=tf.keras.activations.relu),
        tf.keras.layers.MaxPool2D(pool_size=(3, 3),
                                  strides=2,
                                  padding="same"),
        tf.keras.layers.BatchNormalization(),
        # layer 6
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(units=4096,
                              activation=tf.keras.activations.relu),
        tf.keras.layers.Dropout(rate=0.2),
        # layer 7
        tf.keras.layers.Dense(units=4096,
                              activation=tf.keras.activations.relu),
        tf.keras.layers.Dropout(rate=0.2),
        # layer 8
        tf.keras.layers.Dense(units=NUM_CLASSES,
                              activation=tf.keras.activations.softmax)
    ])

    return model
