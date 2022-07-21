<< [Back](../../../)

# Cameras

For the purpose of streaming, we implemented a dual-camera mode into the GTA5 to make watching Charles driving around more pleasant - usually the cinematic (3rd person) camera is more interesting, but the hood camera is what we need to feed the model. Previously, in 2017, the camera used for streaming was the same as the one fed to the model - the hood camera. With the reboot of the project, we decided to create a dual-camera mode (which can be further extended in the future if necessary).

In the player instance, we're rendering at 90 FPS, quickly changing the cameras to achieve:  
- the 3rd person camera (top-left corner)  
- the hood camera (top-right corner)  
- an additional camera that can be used later  

all rendering effectively at 30 FPS:  
![layout.jpg](../_media/layout.jpg)  

This way each camera renders at 30 FPS - the desired FPS for the project. The [`Data Collectors`](../project_info/system.md) are rendering only at 30 FPS since currently only the `Hood Camera` is being used to feed the model. We developed a custom system to synchronize currently-used and rendering cameras to form 3 separate streams, each at 30 FPS. This way we can display both cinematic and hood cameras on the stream at the same time, and use only the `Hood Camera` to feed the model.

All of the cameras are rendering at *1280x720* with the `Hood Camera` currently downscaling the image to *480x270*.
