<< [Back](../../../)

# Xception

Table of Contents:
- [`Overview`](#overview)
- [`Models`](#models)
- [`Usage`](#usage)
- [`Papers`](#papers)
- [`Graph`](#graph)

<br/>
<br/>

# Overview
`Xception` is the first model architecture used as the CNN backbone that we've used with this project. This has been also our first choice as `Xception` turned out to work best [back in 2017](../original_project/) with the original project attempt. As opposed to the old project, this time we attached (in most of the cases) the regression outputs to the full model (also we're not using waypoints). It worked quite well as a CNN backbone letting the model learn more than we initially thought it'll be capable of.

<br/>
<br/>

# Models
This model architecture has been used in the following model lines:
- [`model_0001_xception`](../model_0001_xception/)
- [`model_0002_xception`](../model_0002_xception/)
- [`model_0003_xception`](../model_0003_xception/)
- [`model_0011_x_tcb`](../model_0011_x_tcb/)

and we later replaced it with the [`InceptionResNetv2`](../project_info/inceptionresnetv2.md).

<br/>
<br/>

# Usage

We're using Keras implementation of the `Xception` model without the head and with randomly initialized parameters (with an ability to use `Imagenet` to initialize parameters):  
Import:  
```py
from tensorflow.keras.applications.xception import Xception
```  
Usage:  
```py
cnn_backbone = Xception(weights="imagenet" if settings['XCEPTION_USE_PRETRAINED_WEIGHTS'] else None, include_top=False, input_shape=model_input['shape'])
```

<br/>
<br/>

# Papers

The paper describing the model: [https://arxiv.org/pdf/1610.02357.pdf](https://arxiv.org/pdf/1610.02357.pdf)

<br/>
<br/>

# Graph

Model graph:
![Xception](../_media/xception.png)