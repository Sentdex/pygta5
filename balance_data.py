# balance_data.py
# slightly modified version for v.0.03+

import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import cv2

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]




for i in range(1800): # Number of training data

	try:

		train_data = np.load('F:/GTA-V/training_data/training_data-{}.npy'.format(i), allow_pickle=True) # name of the training data
		df = pd.DataFrame(train_data)
		print(df.head())
		print(Counter(df[1].apply(str)))
	
	
		w = []
		s = []
		a = []
		d = []
		wa = []
		wd = []
		sa = []
		sd = []
		nk = []




		shuffle(train_data)

		for data in train_data:

			img = data[0]
			choice = data[1]

			
			if choice == [1,0,0,0,0,0,0,0,0]: # Sol
				w.append([img,choice])
			
			elif choice == [0,1,0,0,0,0,0,0,0]:
				s.append([img,choice])
			
			elif choice == [0,0,1,0,0,0,0,0,0]:
				a.append([img,choice])

			elif choice == [0,0,0,1,0,0,0,0,0]:
				d.append([img,choice])

			elif choice == [0,0,0,0,1,0,0,0,0]:
				wa.append([img,choice])# Arka sol
			
			elif choice == [0,0,0,0,0,1,0,0,0]:
				wd.append([img,choice])# Arka sol

			elif choice == [0,0,0,0,0,0,1,0,0]:
				sa.append([img,choice])

			elif choice == [0,0,0,0,0,0,0,1,0]:
				sd.append([img,choice])

			elif choice == [0,0,0,0,0,0,0,0,1]:
				nk.append([img,choice])

			else:
				print("Something is wrong!!!")
		

		w = w[:len(wa)][:len(wd)][:len(nk)][:len(s)][:len(sa)][:len(sd)][:len(d)][:len(a)]
		
		wa = wa[:len(w)]
		wd = wd[:len(w)]
		nk = nk[:len(w)]
		s = s[:len(w)]
		sa = sa[:len(w)]
		d = d[:len(w)]
		sd = sd[:len(w)]
		a = a[:len(w)]
		
	
		final_data = w+s+a+d+wa+wd+sa+sd+nk
		
			
		np.save('F:/GTA-V/training_data/training_data-balanced-{}.npy'.format(i), final_data) # name of your 
		
		
		print("Saved: {}".format(i))
		print("Size: {}".format(len(final_data)))
		


	except Exception as e:
		print(str(e))