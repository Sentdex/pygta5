<< [Back](../../../)

# Python Plays Grand Theft Auto 5 - System

The system has been built from the ground up. The central part of it is the `server/trainer`. The server part communicates with other scripts and instructs them on what task to perform.

## Table of Contents
- [`Data collectors`](#data-collectors)
- [`Server`](#server)
- [`Trainer`](#trainer)
- [`Player`](#player)
- [`Other parts of the system`](#other-parts-of-the-system)

<br/>
<br/>

## Data collectors
The whole process starts at the `Data Collector` nodes running GTA5 and our custom [`NPCs`](../project_info/NPCs.md), our custom GTA5 mod, and the `Data Collector` script. The script connects to the server to acquire the current configuration, then connects to our custom game mod to set the environment, start driving and start collecting the data. We are typically running 3-5 data collector instances at a time, but will most likely use more in the future. The custom game mod lets us set different aspects of the environment like the car used, the weather or time of day, and much more.

Each data collector is running our [`NPC`](../project_info/NPCs.md) which is driving around and generating the data that's being collected by the data collector script.

The data consists of:
- current image frame (synchronized strictly with the other data and being taken exactly every 1/30th of the second for the best data quality)
- current car's acceleration/braking and steering
- current speed
- current [`Purpose`](../project_info/purpose.md) - a way to instruct a model where to drive

The collected data is then [`balanced`](../project_info/data_balancing.md) to ensure it consists of a variety of outputs and sent as balanced sample sets to the [`Server`](#server).

<br/>
<br/>

## Server
The server is a central part of the system (and integrates the [`Trainer`](#trainer)). It listens for the connections from the other parts of the system like [`Data Collectors`](#data-collectors) and [`Players`](#player). It loads the configuration and is responsible for keeping all scripts running and communicating. The [`Data Collectors`](#data-collectors) connect to it and send the collected data which it then sends further to the [`Trainer`](#trainer). The [`Player`](#player) instances connect and the server announces them to the [`Trainer`](#trainer) which then can send the updated parameters to them.

The system has been built to be flexible, so we can quickly change many settings and restart training. For example, we can freely mix the output types between regression, classification, and discrete delta for each of the outputs separately, and the loss, metric, balancing, and other parts of the system are going to be automatically updated to reflect these settings.

The `Server/Trainer Console` (visible on the stream) shows the state of the buffers, how many batches we have trained for so far, the training status as well as additional information from the server like the other scripts connecting to the server or player updates with parameters.

<br/>
<br/>

## Trainer:
[`Data Collectors`](#data-collectors) are collecting and balancing the data according to these settings and the `Trainer` receives balanced sample sets through the [`Server`](#server). Newly received samples are being put into the [`Buffers`](../project_info/storage_buffer.md) and [`Storage`](../project_info/storage_buffer.md) and when the buffers are filled-in, the training starts - as long as there is a minimum number of samples in each of the buffers (at least 90%), batches are being drawn and the model is being trained. The trained model is periodically saved to the disk and sent to all connected [`Player`](#player) instances.

<br/>
<br/>

## Player:
The `Player` instances (usually one, seen on the stream) connect to the server, acquire configuration and start playing waiting for the [`Trainer`](#trainer) to send updated parameters of the currently trained model - the `Player` updates them during the nearest [`Unstuck`](../project_info/unstuck.md) and this way we can observe the model's growth. The player runs its copy of a model, which is set in the inference mode to make predictions as fast as possible (ideally 30 times a second). Our custom GTA5 game mod lets us grab a screen frame, resize it, and grab additional information from the game to feed the model that predicts acceleration/braking and steering values. These predictions are being calculated into virtual controller inputs (we're using `vgamepad`) and the car steering is being updated.

The `Player Console` shows current raw predictions (outside of the rounded brackets) and translated controller values (inside of the rounded brackets) - we have to translate predictions to controller inputs because of so-called dead zones in the controller used by GTA5. The `FPS` shows the [`Hood Camera`](../project_info/cameras.md)’s frames per second and the `PPS` shows how many predictions per second we're currently performing.

<br/>
<br/>

## Other parts of the system:
The whole system is significantly more complicated than this quick summary and is constantly under heavy development.
