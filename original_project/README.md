NOTE: This old project is provided in legacy mode. Currently there are no plans to provide any updates to it

# Using Python programming to Play Grand Theft Auto 5

Explorations of Using Python to play Grand Theft Auto 5, mainly for the purposes of creating self-driving cars and other vehicles.

We read frames directly from the desktop, rather than working with the game's code itself. This means it works with more games than just GTA V, and it will basically learn (well, attempt to learn...) whatever you put in front of it based on the frames as input and key presses as output.

Pull requests are welcomed.

Currently, to use the latest version of this AI, you will need to run first "create_training_data.py," then balance this data with "balance_Data.py."

When creating training data, this works when you have the game in windowed mode, 800x600 resolution, at the top left of your screen. You need this for both training and testing. Eventually we can go off the window's name, but, for now, the current code wants the window in the corner.

Do this for as many files/training samples as you wish. I suggest 100K+ after balancing, but the more the merrier.

Next, Train the model with train_model.py.

Finally, use the model in game with test_model.py. 

...you'll probably want to poke into the tutorials here: https://pythonprogramming.net/game-frames-open-cv-python-plays-gta-v/. If you need tutorials on deep learning, or tensorflow, or tflearn, see here: https://pythonprogramming.net/tensorflow-introduction-machine-learning-tutorial/

Do you know of some relevant papers/research/models for this project? Share with us here: https://github.com/Sentdex/pygta5/issues/11
