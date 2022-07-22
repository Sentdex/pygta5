<< [Back](../../../)

# Storage and Buffers

## Table of Contents
- [`Overview`](#overview)
- [`Buffers`](#buffers)
- [`Storage`](#storage)

<br/>
<br/>

# Overview

Some of our tests did show that collecting (caching) more data and randomly sampling from it is more beneficial than using sample sets sent by the [`Data Collectors`](../project_info/system.md) right away. This is because while sampling a batch from a bigger cache of samples, we’re taking samples collected over a longer period of time, from other parts of the map, containing different data characteristics., etc. This means the batches are a better representation of all of the data and do not make the model only fit wherever the NPCs are now and to their current actions.

<br/>
<br/>

## Buffers

When [`Data Collectors`](../project_info/system.md) send data to the [`Trainer`](../project_info/system.md) through the [`Server`](../project_info/system.md) it's not being immediately used to train the model. Instead, the buffers are being filled first, currently to *25,000* samples each. The training starts when all of the buffers are filled in. During training, a batch is formed by randomly sampling from each of the buffers (the same number of samples is being drawn per buffer but the samples are random) then these samples are removed from the buffers (and are never used again). This way each batch of samples consists of random data from different in-game points of time and areas. We found out that without buffers, the model did learn significantly worse since the data has been consisting of very similar images and actions only, changing with time. The buffers combined with a good [`Balancing`](../project_info/data_balancing.md) let us build a live-training system that feeds the model with the data as fast as possible but also in a balanced and shuffled fashion important for good model training and generalization.

<br/>
<br/>

## Storage

Because filling in of the buffers takes time, and we sometimes need to restart the server or there are other circumstances like power loss or code issues, we added the storage to the system which keeps a copy of the buffers on the disk in a form of individual samples that are being constantly rotated. This way we can quickly re-fill the `Buffers` without waiting for the [`Data Collectors`](../project_info/system.md) to fill them in (the training can start shortly after the [`Trainer`](../project_info/system.md) is being run)
