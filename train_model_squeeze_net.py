# train_model.py

from SqueezeNet.SqueezeNet import *
import time
import random

WIDTH = 160
HEIGHT = 120
LR = 1e-3
EPOCHS = 1000
CLASSES = 3
BATCH_SIZE = 64
MODEL_NAME = 'pygta5-car-fast-{}-{}-{}-epochs-300K-data.model'.format(LR, 'squeezenet',EPOCHS)

train_data = np.load('training_data.npy')

c = len(train_data)
train = train_data[:-c//10]
test = train_data[-c//10:]

X = np.array([i[0] for i in train]).reshape(-1,WIDTH,HEIGHT,1)
Y = [i[1] for i in train]

print('Dataset size:',len(X))

test_x = np.array([i[0] for i in test]).reshape(-1,WIDTH,HEIGHT,1)
test_y = [i[1] for i in test]

x = tf.placeholder(tf.float32,(None,WIDTH,HEIGHT,1))
y = tf.placeholder(tf.float32,(None,CLASSES))
keep_prob = tf.placeholder(tf.float32)

_,train_step,accuracy = getSqueezeNetModel(x,y,keep_prob,LR)

with tf.Session() as sess:
    merged = tf.summary.merge_all()
    summaryWriter = tf.summary.FileWriter('./SqueezeNet/Tensorboard',sess.graph)
    sess.run(tf.global_variables_initializer())    
    run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
    run_metadata = tf.RunMetadata()
    saver = tf.train.Saver()

    print('Started')
    start_time = time.time()
    for i in range(EPOCHS):
        print(i)
        if i%100 == 0:
            summary, train_accuracy = sess.run([merged, accuracy],
                                        feed_dict={x: test_x, y: test_y,keep_prob: 1},
                                        options=run_options,
                                        run_metadata=run_metadata)
            summaryWriter.add_run_metadata(run_metadata, 'step%03d' % i)
            summaryWriter.add_summary(summary, i)
            print("step %d, training accuracy %g %f"%(i, train_accuracy,time.time()-start_time))
            start_time = time.time()
            saver.save(sess,'./SqueezeNet/'+MODEL_NAME)

        batch = np.array(random.sample(list(zip(X,Y)),BATCH_SIZE))
        batchX = list(batch[:,0])
        batchY = list(batch[:,1])
        train_step.run(feed_dict={x: batchX, y: batchY,keep_prob:.5})
        
        
    
