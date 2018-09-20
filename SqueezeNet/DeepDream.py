from SqueezeNet import *
import time
import numpy as np
import cv2

WIDTH = 160
HEIGHT = 120
LR = 1e-3
EPOCHS = 1000
CLASSES = 3
MODEL_NAME = 'pygta5-car-fast-{}-{}-{}-epochs-300K-data.model'.format(LR, 'squeezenet',EPOCHS)

sess = tf.InteractiveSession()

x = tf.placeholder(tf.float32,(None,WIDTH,HEIGHT,1))
y = tf.placeholder(tf.float32,(None,CLASSES)) # Not used
keep_prob = tf.placeholder(tf.float32) # Set to 1

model,_,_ = getSqueezeNetModel(x,y,keep_prob,LR)
sess.run(tf.global_variables_initializer())
saver = tf.train.Saver()
saver.restore(sess,'./'+MODEL_NAME)

def dream(layer = len(activations)-1,ITERATIONS = 50):
  #img_noise = np.random.uniform(size=(WIDTH,HEIGHT))
  img_noise = np.ones((WIDTH,HEIGHT)) * .5
  total_image = None

  for channel in range(activations[layer].get_shape().as_list()[-1]):
    try:
      t_obj = activations[layer][:,:,:,channel]
    except:
      t_obj = activations[layer][:,channel]
    t_score = tf.reduce_mean(t_obj)
    t_grad = tf.gradients(t_score,x)[0]
    img = img_noise.copy()
    img = np.reshape(img,(1,WIDTH,HEIGHT,1))

    for i in range(ITERATIONS):
      g,score = sess.run([t_grad,t_score],{x:img,keep_prob:1})
      g /= g.std()+1e-8
      step = 1
      img += g*step
    print(channel,score)

    img = (img-img.mean())/max(img.std(), 1e-4)*.1 + 0.5     
    if total_image is None:
      total_image = img.reshape((WIDTH,HEIGHT))
    else:
      total_image = np.hstack((total_image,img.reshape((WIDTH,HEIGHT))))
  cv2.imwrite('Total_%s.png'%layer,total_image * 255)

def dreamAll(ITERATIONS = 50):
  for i in range(len(activations)):
    print('Layer %d'%i)
    dream(i,ITERATIONS)
