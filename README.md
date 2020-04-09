# Neural Magic ML API
Neural Magic is focused on making performance engineering for deep learning easy, affordable, and accessible. 
The Neural Magic Inference Engine enhances speed for neural networks in numerous ways, 
including activation sparsity and model pruning. 
This codebase is set up to allow easy creation of performance-optimized models specifically for Neural Magic. 
Additionally, implementations for multiple frameworks, including PyTorch and TensorFlow, are provided. 
The easy-to-use codebase is designed for machine learning engineers.

## Repository Structure
```
neuralmagicml
    neuralmagicML - The Python API Code
    notebooks - Tutorial Notebooks for using the Python API
    scripts - Functional scripts for working with the Python API
    tf2onnx - API for converting TensorFlow models to ONNX
    README.md - readme file
    requirements.txt - requirements for the Python API
    setup.py - setuptools install script
```

## Installation and Requirements
Python 3.5.0 or higher is required on the system. 
General instructions for doing this are found [here](https://realpython.com/installing-python/).

Additionally, it is recommended to work within a virtual environment. 
Sample commands for creating and activating in a Unix-based system are provided below:
```
pip3 install virtualenv
python3 -m venv ./venv
source ./venv/bin/activate
```

### Supported ML Frameworks
- PyTorch supported versions: `1.X.X`
- TensorFlow supported versions: `1.X.X` (TensorFlow >= `2.X` is not currently supported)

### Installation
1. Navigate to the parent directory of the `neuralmagicml` code base.
2. Use pip install to run the setup.py file in the repo: `pip install neuralmagicml/`
3. Import neuralmagicML library in your code: `import neuralmagicML`

Note: If you run into issues with TensorFlow / PyTorch imports (specifically GPU vs. CPU support), 
you can edit the `requirements.txt` file at the root of the repo for the desired TensorFlow or PyTorch version.


## Tutorials
.
Tutorials, which are implemented as Jupyter notebooks for easy consumption and editing, 
are provided under the `notebooks` directory. 
To run one of the tutorials, start a Jupyter session in the `notebooks` directory.
```bash
cd notebooks
jupyter notebook
```

Once the Jupyter session has started, you can open the desired notebooks.

### model_repo.ipynb
A tutorial for exploring and downloading from the [Model Repository](#model-repository). 
It allows downloads for any model currently available within any ML framework.

### pruning_adam_pytorch.ipynb
A tutorial for pruning models in PyTorch using an Adam optimizer. 
A step-by-step process, along with simple UIs, is given to make the process easier and more intuitive. 
It is used to increase the performance of models when executing in the Neural Magic Inference Engine.

### transfer_learning_pytorch.ipynb
A tutorial for transfer learning from a model in the [Model Repository](#model-repository) 
within PyTorch using an Adam optimizer.
The main use case is transfer learning from a previously pruned model. 
In this way, you can limit the training time needed as well as the potential complexity of 
the pruning process while keeping the performance.

## Model Repository
A number of pre-trained models are available in this API.
Included are both baseline and recalibrated models for higher performance on the Neural Magic Inference Engine. 
The types available for each model architecture are noted in the table below.

Possible types are:
 - base - the baseline model (standard training process)
 - recal - a recalibrated model for better performance that achieves ~100% of baseline validation metrics
 - recal-perf - a recalibrated model for better performance that meets ~99% of baseline validation metrics


### Available Models
|  Architecture      | Dataset  | Available Types         | Frameworks                 | Validation Baseline Metric |
| ------------------ | -------- | ----------------------- | -------------------------- | -------------------------- |
| MnistNet           | mnist    | base                    | onnx, PyTorch, TensorFlow  | ~99% top1 accuracy         |
| MobileNet V1       | imagenet | base, recal, recal-perf | onnx, PyTorch              | 70.9% top1 accuracy        |
| MobileNet V2       | imagenet | base                    | onnx, PyTorch              | 71.88% top1 accuracy       |
| ResNet 50          | imagenet | base, recal, recal-perf | onnx, PyTorch              | 76.1% top1 accuracy        |
| ResNet 50 2xwidth  | imagenet | base                    | onnx, PyTorch              | 78.51% top1 accuracy       |
| ResNet 101         | imagenet | base                    | onnx, PyTorch              | 77.37% top1 accuracy       |
| ResNet 101 2xwidth | imagenet | base                    | onnx, PyTorch              | 78.84% top1 accuracy       |
| ResNet 152         | imagenet | base                    | onnx, PyTorch              | 78.31% top1 accuracy       |
| VGG 11             | imagenet | base                    | onnx, PyTorch              | 69.02% top1 accuracy       |
| VGG 11bn           | imagenet | base                    | onnx, PyTorch              | 70.38% top1 accuracy       |
| VGG 13             | imagenet | base                    | onnx, PyTorch              | 69.93% top1 accuracy       |
| VGG 13bn           | imagenet | base                    | onnx, PyTorch              | 71.55% top1 accuracy       |
| VGG 16             | imagenet | base, recal, recal-perf | onnx, PyTorch              | 71.59% top1 accuracy       |
| VGG 16bn           | imagenet | base                    | onnx, PyTorch              | 71.55% top1 accuracy       |
| VGG 19             | imagenet | base                    | onnx, PyTorch              | 72.38% top1 accuracy       |
| VGG 19bn           | imagenet | base                    | onnx, PyTorch              | 74.24% top1 accuracy       |

### Downloading and Usage
Tutorial notebooks are provided for easily integrating and using the models in the Neural Magic Model Repo. 
Check the [Tutorials section](#tutorials) for more details. 
The APIs provided to interface with the Model Repo are located in `neuralmagicML.utils`. 

To retrieve all available models in the repo, you can use the `available_models` function. 
It returns a list of `RepoModel` objects.
Example code:
```python
from neuralmagicML.utils import available_models, RepoModel

models = available_models()  # type: List[RepoModel]
print(models)
```

#### ONNX
The `RepoModel` class contains a helper function to download the ONNX files: RepoModel().download_onnx_file()`.
Example code:
```python
import os
from neuralmagicML.utils import available_models, RepoModel

model = available_models()[0]  # type: RepoModel
print(model)
save_dir = os.path.join(".", "model-repo")
downloaded_path = model.download_onnx_file(save_dir=save_dir)
print("Downloaded to {}".format(downloaded_path))
```

#### PyTorch
You can use the `RepoModel` class with the `ModelRegistry` class under 
`neuralmagicML.pytorch.models` to download and create a PyTorch model.
Example code:
```python
from neuralmagicML.utils import available_models, RepoModel, PYTORCH_FRAMEWORK
from neuralmagicML.pytorch.models import ModelRegistry

repo_model = [
    mod for mod in available_models() if mod.framework == PYTORCH_FRAMEWORK
][0]
print(repo_model)

pytorch_model = ModelRegistry.create(
    repo_model.registry_key, pretrained=repo_model.desc
)
print(pytorch_model)
```

#### TensorFlow
You can use the `RepoModel` class with the `ModelRegistry` class under 
`neuralmagicML.tensorflow.models` to download and create a TensorFlow model. Example code:
```python
from neuralmagicML.utils import available_models, RepoModel, TENSORFLOW_FRAMEWORK
from neuralmagicML.tensorflow.models import ModelRegistry
from neuralmagicML.tensorflow.utils import tf_compat

repo_model = [
    mod for mod in available_models() if mod.framework == TENSORFLOW_FRAMEWORK
][0]
print(repo_model)

with tf_compat.Graph().as_default() as graph:
    inputs = tf_compat.placeholder(
        tf_compat.float32,
        [None, *ModelRegistry.input_shape(repo_model.registry_key)],
        name="inputs",
    )
    outputs = ModelRegistry.create(repo_model.registry_key, inputs)

    with tf_compat.Session() as sess:
        ModelRegistry.load_pretrained(
            repo_model.registry_key,
            pretrained=repo_model.desc,
            pretrained_dataset=repo_model.dataset,
        )
        print(graph.as_graph_def())
``` 

## Recalibration
APIs for recalibrating models are provided for each supported ML framework.
Recalibration includes such things as 
[model pruning (kernel sparsity)](https://towardsdatascience.com/pruning-deep-neural-network-56cae1ec5505) 
as well as [quantization](https://towardsdatascience.com/speeding-up-deep-learning-with-quantization-3fe3538cbb9)
in a future release.
Both of these, when paired with the Neural Magic Inference Engine, can significantly improve model inference speed.

The APIs are designed to be integrated into your existing code with as few lines as possible.
The implementations for each framework differ to best match their internal structures and designs.

### Config File
All recalibration APIs are designed to work with configuration files.
These configuration files are written in [YAML](https://yaml.org/) and are loaded into 
modifying Python objects when recalibrating the models.
The config files additionally have the same interface across the ML frameworks.
This enables relatively minimal changes to the config files to load an original 
config for a PyTorch model into TensorFlow, for example.

An interactive UI will be rolled out in a future release to support easier modification and creation of the config files.
For now, UI's with basic functions are provided in the supporting [tutorial notebooks](#tutorials).
We recommend becoming familiar with these first.

The config.yaml files are made up of individual modifiers. 
These modifiers handle changing different parts of the training process.
In general, each modifier will have a start and an end epoch for when the modifier should be active.
The modifiers will start at `start_epoch` and run until `end_epoch`.
Note that it does not run through `end_epoch`.
Additionally, all epoch values support decimal values such that they can be started somewhere in the middle of an epoch.
For example, `start_epoch: 2.5` will start in the middle of the second training epoch.

The most commonly used ones are enumerated as subsections below.
Also, here is a simple example of a config.yaml file that prunes all layers in a model:
```yaml
version: 1.0.0

modifiers:
    - !EpochRangeModifier
        start_epoch: 0.0
        end_epoch: 25.0

    - !GradualKSModifier
        layers: __ALL__
        init_sparsity: 0.05
        final_sparsity: 0.8
        start_epoch: 5.0
        end_epoch: 20.0
        update_frequency: 1.0
```

#### Training Epoch Modifiers
The `EpochRangeModifier` controls the range of epochs for training a model.
Each supported ML framework has an implementation to enable easily retrieving this number of epochs.
Note, that this is not a hard rule and if other modifiers have a larger `end_epoch` or smaller `start_epoch`
then those values will be used instead.

The only parameters that can be controlled for `EpochRangeModifier` are the `start_epoch` and `end_epoch`.
Both parameters are required.

Required Parameters:
 - `start_epoch`: The start range for the epoch (0 indexed)
 - `end_epoch`: The end range for the epoch
 
 Example:
 ```yaml
     - !EpochRangeModifier
        start_epoch: 0.0
        end_epoch: 25.0
 ```

#### Pruning Modifiers
The pruning modifiers handle creating or enforcing kernel sparsity for a specified layer(s) in a given model.

##### ConstantKSModifier
The `ConstantKSModifier` enforces the sparsity structure and level for an already pruned layer(s) in a model.
The modifier is used for transfer learning from an already pruned model.
The weights are allowed to make updates to enable transferring to a new task, however the sparsity is unchanged.

Note, currently unsupported in TensorFlow.

Required Parameters:
 - `layers`: The layers in the model to prune. 
   It can be set to a string containing `__ALL__` to prune all layers or a list to specify the targeted layers.
   Ex: `['blocks.1.conv']` for PyTorch and `['mnist_net/blocks/conv0/conv']` for TensorFlow.
 - `init_sparsity`: The decimal value for the initial sparsity to start pruning with.
 - `start_epoch`: [Optional] The epoch to start the pruning at (0 indexed).
   It supports floating-point values to enable starting pruning between epochs.
   Defaults to -1 meaning that it starts immediately.
 - `end_epoch`: [Optional] The epoch to stop pruning before.
   It supports floating-point values to enable stopping pruning between epochs.
   It defaults to -1, meaning that it never ends.
   
Example:
```yaml
    - !ConstantKSModifier
        layers: __ALL__
        start_epoch: 0.0
        end_epoch: 10.0
        param: weight
        log_types: __ALL__
```

##### GradualKSModifier
The `GradualKSModifier` prunes the layer(s) in a model to a target sparsity 
(percentage of 0's for a layer's param/variable).
This is done gradually from an initial to final sparsity (`init_sparsity`, `final_sparsity`)
over a range of epochs (`start_epoch`, `end_epoch`) and updated at a specific interval defined by the `update_frequency`.
For example, using the following settings `start_epoch: 0`, `end_epoch: 5`, `update_frequency: 1`, 
`init_sparsity: 0.05`, `final_sparsity: 0.8` will do the following:
- at epoch 0 set the sparsity for the specified layer(s) to 5%
- once every epoch, gradually increase the sparsity towards 80%
- by the start of epoch 5, stop pruning and set the final sparsity for the specified layer(s) to 80%

Required Parameters:
 - `layers`: The layers in the model to prune. 
   Can be set to a string containing `__ALL__` to prune all layers or a list to specify the targeted layers.
   Ex: `['blocks.1.conv']` for PyTorch and `['mnist_net/blocks/conv0/conv']` for TensorFlow.
 - `init_sparsity`: The decimal value for the initial sparsity to start pruning with.
   At `start_epoch` will set the sparsity for the param/variable to this value. Generally kept at 0.05 (5%)
 - `final_sparsity`: The decimal value for the final sparsity to end pruning with.
   By the start of `end_epoch` will set the sparsity for the param/variable to this value.
   Generally kept in a range from 0.6 to 0.95 depending on the model and layer. 
   Anything less than 0.4 is not useful for performance.
 - `start_epoch`: The epoch to start the pruning at (0 indexed).
   Supports floating-point values to enable starting pruning between epochs.
 - `end_epoch`: The epoch to stop pruning before.
   Supports floating-point values to enable stopping pruning between epochs.
 - `update_frequency`: The number of epochs/fractions of an epoch between each pruning step.
   It supports floating-point values to enable updating inside of epochs.
   Generally set to update once per epoch (`1.0`). 
   However, if the loss for the model recovers quickly, it should be set to a lesser value.
   Ex: Set it to `0.5` for once every half epoch (twice per epoch). 
   
Example:
```yaml
    - !GradualKSModifier
        layers: ['blocks.1.conv']
        init_sparsity: 0.05
        final_sparsity: 0.8
        start_epoch: 5.0
        end_epoch: 20.0
        update_frequency: 1.0
```

#### Learning Rate Modifiers
The learning rate modifiers sets the learning rate for an optimizer during training.
If you are using an Adam optimizer, then generally, these are not useful.
If you are using a standard stochastic gradient descent optimizer, then these give a convenient way to control the LR.

Note, currently unsupported in TensorFlow.

##### SetLearningRateModifier
The `SetLearningRateModifier` sets the learning rate for the optimizer to a specific value at a specific point
in the training process.

Required Parameters:
 - `start_epoch`: The epoch in the training process to set the `learning_rate` value for the optimizer.
   Supports floating-point values to enable setting the LR between epochs.
 - `learning_rate`: The floating-point value to set as the learning rate for the optimizer at `start_epoch`.
 
Example:
```yaml
    - !SetLearningRateModifier
        start_epoch: 5.0
        learning_rate: 0.1
```

#### LearningRateModifier
The `LearningRateModifier` sets schedules for controlling the learning rate for an optimizer during training.
If you are using an Adam optimizer, then generally these are not useful.
If you are using a standard stochastic gradient descent optimizer, then these give a convenient way to control the LR.
Provided schedules to choose from are the following:
 - `ExponentialLR`: multiplies the learning rate by a `gamma` value every epoch.
   To use this one, `lr_kwargs` should be set to a dictionary containing `gamma`.
   Ex: `{'gamma': 0.9}`
 - `StepLR`: multiplies the learning rate by a `gamma` value after a certain epoch period defined by `step`.
   To use this one, `lr_kwargs` must be set to a dictionary containing `gamma` and `step`.
   Ex: `{'gamma': 0.9, step: 2.0}`
 - `MultiStepLR`: multiplies the learning rate by a `gamma` value at specific epoch points defined by `milestones`.
   To use this one, `lr_kwargs` must be set to a dictionary containing `gamma` and `milestones`.
   Ex: `{'gamma': 0.9, 'milestones': [2.0, 5.5, 10.0]}`
   
Required Parameters:
 - `start_epoch`: The epoch to start modifying the LR at (0 indexed).
   Supports floating-point values to enable starting pruning between epochs.
 - `end_epoch`: The epoch to stop modifying the LR before.
   Supports floating-point values to enable stopping pruning between epochs.
 - `lr_class`: The LR class to use, one of [`ExponentialLR`, `StepLR`, `MultiStepLR`]
 - `lr_kwargs`: The named arguments for the `lr_class`
 - `init_lr`: [Optional] The initial LR to set at `start_epoch` and to use for creating the schedules, 
    if not given then will use the optimizer's current LR at startup
 
 Example:
 ```yaml
     - !LearningRateModifier
        start_epoch: 0.0
        end_epoch: 25.0
        lr_class: MultiStepLR
        lr_kwargs:
            gamma: 0.9
            milestones: [2.0, 5.5, 10.0]
        init_lr: 0.1
 ```

### Recalibrating in PyTorch
The recalibration tooling for PyTorch is located under `neuralmagicML.pytorch.recal`.
Inside are APIs designed to make model recalibration as easy as possible.
Additionally, the tooling is designed to work with the previously described config files.

The `ScheduledModifierManager` is used to create modifiers from a config file.
Specifically, `ScheduledModifierManager.from_yaml(/PATH/TO/config.yaml)` should be used.
The function call will return a new instance of `ScheduledModifierManager` containing the modifiers described in the config file.
Once a manager class has been created, a `ScheduledOptimizer` class must be created.
This class is used to wrap the `ScheduledModifierManager`, PyTorch model, 
and PyTorch optimizer to enable modifying the training process.
The `ScheduledOptimizer` should then be used in place of the original PyTorch optimizer in the rest of your code.
Mainly, it overrides the `optimizer.step()` function to modify the training process.
Additionally, `optimizer.epoch_start()` and `optimizer.epoch_end()` should be called 
at the start and end of each epoch respectively. 

Example:
```python
from torch.optim import Adam
from torch.utils.data import DataLoader
import torch.nn.functional as TF
from neuralmagicML.pytorch.models import mnist_net
from neuralmagicML.pytorch.datasets import MNISTDataset
from neuralmagicML.pytorch.recal import ScheduledModifierManager, ScheduledOptimizer

model = mnist_net()
optimizer = Adam(model.parameters(), lr=1e-4)
train_data = MNISTDataset(train=True)
batch_size = 1024

config_path = "/Users/markkurtz/code/neuralmagic/Shared/neuralmagicml/config.yaml"
manager = ScheduledModifierManager.from_yaml(config_path)
optimizer = ScheduledOptimizer(optimizer, model, manager, steps_per_epoch=len(train_data))

for epoch in range(manager.max_epochs):
    optimizer.epoch_start()
    for batch_x, batch_y in DataLoader(train_data, batch_size):
        optimizer.zero_grad()
        batch_pred = model(batch_x)[0]
        loss = TF.cross_entropy(batch_pred, batch_y)
        loss.backward()
    optimizer.epoch_end()
```

Note: if you would like to log to TensorBoard, a logger class can be created and passed into the `ScheduledOptimizer`.
Example:
```python
from neuralmagicML.pytorch.utils import TensorBoardLogger

optimizer = ScheduledOptimizer(
    optimizer, 
    model, 
    manager, 
    steps_per_epoch=len(train_data), 
    loggers=[TensorBoardLogger()]
)
```

### Recalibrating in TensorFlow
The recalibration tooling for TensorFlow is located under `neuralmagicML.tensorflow.recal`.
Inside are APIs designed to make model recalibration as easy as possible.
Additionally, the tooling is designed to work with the previously described config files.

The `ScheduledModifierManager` is used to create modifiers from a config file.
Specifically, `ScheduledModifierManager.from_yaml(/PATH/TO/config.yaml)` should be used.
This will return a new instance of `ScheduledModifierManager` containing the modifiers described in the config file.
Once a manager class has been created, it can be used to modify the training graph.
Under the scope of a TensorFlow graph containing the created model operations and variables,
`manager.create_ops()` must be called.
This will go through and modify the graph as defined in the config.yaml file.
It will return modifying ops as a list and modifying extras as a dictionary.
The list of ops must be run once per training step and after the optimizer has run.
Also, `create_ops()` must be called outside of a session to have any effect.
Under the scope of a created TensorFlow session, `manager.initialize_session()` should be called
if the global variables initializer was not run.
This will handle initializing any variables that were created as part of the `create_ops()` invocation.
Finally, after training is complete, `manager.complete_graph()` must be called.
This will clean up the modified graph properly for saving and export.

Example:
```python
from tensorflow.examples.tutorials.mnist import input_data
from neuralmagicML.tensorflow.utils import tf_compat, batch_cross_entropy_loss
from neuralmagicML.tensorflow.models import mnist_net
from neuralmagicML.tensorflow.recal import ScheduledModifierManager

dataset = input_data.read_data_sets("./mnist_data", one_hot=True)
batch_size = 1024
num_batches = int(len(dataset.train.images) / batch_size)

with tf_compat.Graph().as_default() as graph:
    inputs = tf_compat.placeholder(
        tf_compat.float32, [None, 28, 28, 1], name="inputs"
    )
    labels = tf_compat.placeholder(tf_compat.float32, [None, 10])
    logits = mnist_net(inputs)
    loss = batch_cross_entropy_loss(logits, labels)

    global_step = tf_compat.train.get_or_create_global_step()
    manager = ScheduledModifierManager.from_yaml("/PATH/TO/config.yaml")
    mod_ops, mod_extras = manager.create_ops(steps_per_epoch=len(dataset.train.images))
    
    train_op = tf_compat.train.AdamOptimizer(learning_rate=1e-4).minimize(
        loss, global_step=global_step
    )
    
    with tf_compat.Session() as sess:
        sess.run(tf_compat.global_variables_initializer())
        
        for epoch in range(manager.max_epochs):
            for batch in range(num_batches):
                batch_xs, batch_ys = dataset.train.next_batch(batch_size)
                batch_xs = batch_xs.reshape([-1, 28, 28, 1])
                sess.run(train_op, feed_dict={inputs: batch_xs, labels: batch_ys})
                sess.run(mod_ops)
```

Note: if you would like to log to TensorBoard, summaries for the modifying ops and variables are created by default.
They are added to the default TensorFlow summaries collection, and they are additionally made 
accessible under the mod_extras returned from the `manager.create_ops()` function.
Example:
```python
from neuralmagicML.tensorflow.recal import EXTRAS_KEY_SUMMARIES

summary_ops = mod_extras[EXTRAS_KEY_SUMMARIES]
```

## Licenses and Agreements
* All implementations in this repo are subject to Neural Magic's [Privacy Policy.](https://neuralmagic.com/privacy-policy/)
* All implementations in this repo are subject to Neural Magic's [Terms of Use.](https://neuralmagic.com/evaluation-license-agreement)
* All packages as defined in the requirements.txt and their associated licenses.
* PyTorch [License.](https://github.com/pytorch/pytorch/blob/master/LICENSE)
* PyTorch torchvision and models [License.](https://github.com/pytorch/vision/blob/master/LICENSE)
* TensorFlow [License.](https://github.com/tensorflow/tensorflow/blob/master/LICENSE)
* Examples given in some of the notebooks make use of fast.ai's 
  [Imagenette / Imagewoof dataset](https://github.com/fastai/imagenette) provided under the 
  [Apache License 2.0](https://github.com/fastai/imagenette/blob/master/LICENSE)
