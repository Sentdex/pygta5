<< [Back](../../../)

# InceptionResNetv2

Table of Contents:
- [`Overview`](#overview)
- [`Models`](#models)
- [`Usage`](#usage)
- [`Papers`](#papers)
- [`Graph`](#graph)

<br/>
<br/>

# Overview
`InceptionResNetv2` is the second model architecture used as a CNN backbone. After a few trained models using [`Xception`](../project_info/xception.md) model for this task, we wanted to test a bigger and deeper model to see if there's going to be any performance impact. The `InceptionResNetv2` is only slightly slower than the [`Xception`](../project_info/xception.md) but offers much deeper model (so also an ability to learn more complex and more multi-dimentional dependeces) and about twice as many parameters. This yielded our best model so far, the [`model_0004_inceptionresnetv2_v3`](../project_info/model_0004_inceptionresnetv2).

<br/>
<br/>

# Models
This model architecture has been used in the following model lines:
- [`model_0004_inceptionresnetv2`](../model_0004_inceptionresnetv2/)
- [`model_0005_inceptionresnetv2`](../model_0005_inceptionresnetv2/)
- [`model_0006_inceptionresnetv2`](../model_0006_inceptionresnetv2/)
- [`model_0007_inceptionresnetv2`](../model_0007_inceptionresnetv2/)
- [`model_0008_irv2_data_td`](../model_0008_irv2_data_td/)
- [`model_0009_irv2_cr_tl`](../model_0009_irv2_cr_tl/)
- [`model_0010_irv2_tcb`](../model_0010_irv2_tcb/)

and we are currently replacing it with the `Regnets` (TBA).

<br/>
<br/>

# Usage

We're using Keras implementation of the `InceptionResNetv2` model without the head and with randomly initialized parameters (with an ability to use `Imagenet` to initialize parameters):  
Import:  
```py
from tensorflow.keras.applications import InceptionResNetv2
```  
Usage:  
```py
cnn_backbone = InceptionResNetv2(weights="imagenet" if settings['CNN_USE_PRETRAINED_WEIGHTS'] else None, include_top=False, input_shape=model_input['shape'])
```

<br/>
<br/>

# Papers

The paper describing the model: [https://arxiv.org/pdf/1602.07261.pdf](https://arxiv.org/pdf/1602.07261.pdf)

<br/>
<br/>

# Graph

Model graph:
![InceptionResNetv2](../_media/inceptionresnetv2.png)