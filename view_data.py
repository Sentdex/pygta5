import numpy as np
import cv2

train_data = np.load('training_data.npy')

directions = {
    (1,0,0): 'LEFT',
    (0,1,0): 'UP',
    (0,0,1): 'RIGHT'
}

for data in train_data:
    img = data[0]
    choice = directions[tuple(data[1])]
    cv2.imshow('test', img)
    print(choice)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
