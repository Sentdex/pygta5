<< [Back](../../../)

# Purpose

The purpose is our approach to give Charles purpose in driving. In 2017, the models deeply fitted to the minimap with driving, but this time we wanted new models to be able to drive without waypoints. Even if wandering around worked better than we thought and expected (a single-frame model can take an action and stick to it), we wanted Charles to be able to choose actions more consistently by setting a point on the map and giving the direction and distance to this point as one of the inputs to the model.

The purpose is being visualized as a point on the map, which is additionally also visible to the model on the [`Hood Camera`](../project_info/cameras.md) (however, we can disable that marker point if necessary):  
![purpose.jpg](../_media/purpose.jpg)

The purpose has not been used much as of now but is going to be used again with [`model_0012_regnet`](../model_0012_regnet) and newer.
