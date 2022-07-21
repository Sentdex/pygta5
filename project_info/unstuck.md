<< [Back](../../../)

# Unstuck

Both NPCs and Charles (but mostly Charles) can get stuck. NPCs can get stuck mostly on the environmental elements like in the ditches, between objects, buildings, etc. Charles, additionally to this, can get stuck on many other occasions like in front of some obstacle not "knowing" it's an obstacle and trying to drive forward, in front of intersections since lack of speed sense does not let it know it's current speed and NPCs usually slow down at intersections to take turns, so does Charles - this can lead to a complete stop or even reverse. One of the most famous Charle's stuck moments is `!water` (yes, it has a command in Twitch chat) - a moment when he drives straight into the water (most likely because the color of the water on the minimap is similar to the color of the road as opposed to other types of the terrain or buildings).

To avoid such situations where NPCs are stuck and stop collecting valuable data, or Charles is stuck rendering streaming not interesting, we developed the `Unstuck` which checks periodically if the car has moved by a certain amount in a certain time. It's not ideal since it does not count the distance traveled and if the car is close to the same point after a given number of seconds this sometimes leads to a situation when unstuck is being invoked even if it is not necessary. Otherwise works perfectly well.

The way the unstuck works is:
- stop predicting
- fade the screen out
- find a random place on the map and put the car there
- load all textures and other data required for the car to drive
- fade in the screen
- start predicting again
