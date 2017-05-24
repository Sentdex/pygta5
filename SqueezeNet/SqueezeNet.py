'''
SqueezeNet v1.1 (https://github.com/DeepScale/SqueezeNet/tree/master/SqueezeNet_v1.1)
Paper: https://arxiv.org/abs/1602.07360

TODO: Use Xavier initializer
'''

import tensorflow as tf
import numpy as np

#x = tf.placeholder(tf.float32,(None,28*28))
#y = tf.placeholder(tf.float32,(None,10))
#keep_prob = tf.placeholder(tf.float32)

def getSqueezeNetModel(x,y,keep_prob,learning_rate=1e-3):
    activations = []

    activations.append(x)

    classCount = y.get_shape().as_list()[1]

    NORM = 1e+2

    def fire(inputs,squeezeTo,expandTo):
        h = squeeze(inputs,squeezeTo)
        h = expand(h,expandTo)
        h = tf.clip_by_norm(h,NORM) # Remove if network fails to train
        activations.append(h)

    def squeeze(inputs,squeezeTo):
        with tf.name_scope('squeeze'):
            inputSize = inputs.get_shape().as_list()[3]
            w = tf.Variable(tf.truncated_normal([1,1,inputSize,squeezeTo]))
            h = tf.nn.relu(tf.nn.conv2d(inputs,w,[1,1,1,1],'SAME'))        
        return h

    def expand(inputs,expandTo):
        with tf.name_scope('expand'):
            squeezeTo = inputs.get_shape().as_list()[3]
            w = tf.Variable(tf.truncated_normal([1,1,squeezeTo,expandTo]))
            h1x1 = tf.nn.relu(tf.nn.conv2d(inputs,w,[1,1,1,1],'SAME'))
            w = tf.Variable(tf.truncated_normal([3,3,squeezeTo,expandTo]))
            h3x3 = tf.nn.relu(tf.nn.conv2d(inputs,w,[1,1,1,1],'SAME'))
            h = tf.concat(3,[h1x1,h3x3])
        return h

    # The original paper proposes the use of 6-bit variables which is not
    # possible in tensorflow. For 32-bit tensorflow variables and 526,912 trainable
    # parameters, the size becomes about 2 MB.

    filters  = np.array([64,64,128,128,192,192,256,256])
    squeezes = np.array([16,16, 32, 32, 48, 48, 64, 64])

    with tf.name_scope('conv1'):
        w = tf.Variable(tf.truncated_normal([3,3,1,64]))
        h = tf.nn.relu(tf.nn.conv2d(activations[-1],w,[1,2,2,1],'SAME'))
        activations.append(h)

    with tf.name_scope('maxpool1'):
        h = tf.nn.max_pool(activations[-1],[1,3,3,1],[1,2,2,1],'SAME')
        activations.append(h)

    for i in range(0,2):
        with tf.name_scope('fire'+str(i+2)):
            fire(activations[-1],squeezes[i],filters[i])

    with tf.name_scope('maxpool2'):
        h = tf.nn.max_pool(activations[-1],[1,3,3,1],[1,2,2,1],'SAME')
        activations.append(h)

    for i in range(2,4):
        with tf.name_scope('fire'+str(i+2)):
            fire(activations[-1],squeezes[i],filters[i])

    with tf.name_scope('maxpool3'):
        h = tf.nn.max_pool(activations[-1],[1,3,3,1],[1,2,2,1],'SAME')
        activations.append(h)

    for i in range(4,7):
        with tf.name_scope('fire'+str(i+2)):
            fire(activations[-1],squeezes[i],filters[i])

    with tf.name_scope('dropout'):
        h = tf.nn.dropout(activations[-1],keep_prob)
        activations.append(h)

    with tf.name_scope('conv10'):
        input_shape = activations[-1].get_shape().as_list()[3]
        w = tf.Variable(tf.truncated_normal([1,1,input_shape,classCount]))
        h = tf.nn.relu(tf.nn.conv2d(activations[-1],w,[1,1,1,1],'SAME'))
        activations.append(h)

    with tf.name_scope('avgpool'):
        input_shape = activations[-1].get_shape().as_list()
        h = tf.nn.avg_pool(activations[-1],[1,input_shape[1],input_shape[2],1],[1,1,1,1],'VALID')
        h = tf.squeeze(h,[1,2])
        activations.append(h)

    y_conv = tf.nn.softmax(activations[-1])
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(activations[-1], y)
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    tf.summary.scalar('accuracy',accuracy)

    def getSize():
        total_parameters = 0
        for variable in tf.trainable_variables():
            shape = variable.get_shape()
            variable_parametes = 1
            for dim in shape:
                variable_parametes *= dim.value
            print(shape,variable_parametes)
            total_parameters += variable_parametes
        print('Total trainable variables: ',total_parameters)

        for a in activations:
            print(a.get_shape())

    #getSize()
    
    return (y_conv,train_step,accuracy)



