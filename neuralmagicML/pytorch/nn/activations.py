"""
Implementations related to activations for neural networks in PyTorch
"""

from typing import Union
from torch import Tensor
from torch.nn import Module, PReLU, LeakyReLU
from torch.nn import ReLU as TReLU
from torch.nn import ReLU6 as TReLU6
import torch.nn.functional as TF


__all__ = [
    "ReLU",
    "ReLU6",
    "Swish",
    "swish",
    "create_activation",
    "replace_activation",
    "is_activation",
]


class ReLU(TReLU):
    """
    ReLU wrapper to enforce that number of channels for the layer is passed in.
    Useful for activation sparsity work.

    :param num_channels: number of channels for the layer
    :param inplace: True to run the operation in place in memory, False otherwise
    """

    def __init__(self, num_channels: int = -1, inplace: bool = False):
        super().__init__(inplace=inplace)
        self.num_channels = num_channels


class ReLU6(TReLU6):
    """
    ReLU6 wrapper to enforce that number of channels for the layer is passed in.
    Useful for activation sparsity work.

    :param num_channels: number of channels for the layer
    :param inplace: True to run the operation in place in memory, False otherwise
    """

    def __init__(self, num_channels: int = -1, inplace: bool = False):
        super().__init__(inplace=inplace)
        self.num_channels = num_channels


def swish(x_tens: Tensor):
    """
    Swish layer functional implementation: x * sigmoid(x).
    More information can be found in the paper
    `here <https://arxiv.org/abs/1710.05941>`__.

    :param x_tens: the input tensor to perform the swish op on
    :return: the output of x_tens * sigmoid(x_tens)
    """
    return x_tens * TF.sigmoid(x_tens)


class Swish(Module):
    """
    Swish layer OOP implementation: x * sigmoid(x).
    More information can be found in the paper
    `here <https://arxiv.org/abs/1710.05941>`__.

    :param num_channels: number of channels for the layer
    """

    def __init__(self, num_channels: int = -1):
        super().__init__()
        self.num_channels = num_channels

    def forward(self, inp: Tensor):
        return swish(inp)


def replace_activation(
    module: Module,
    name: str,
    act_type: str,
    inplace: bool = False,
    num_channels: Union[int, None] = None,
    **kwargs
) -> Module:
    """
    General function to replace the activation for a specific layer in a Module
    with a new one.

    :param module: the module to replace the activation function in
    :param name: the name of the layer to replace the activation for
    :param act_type: the type of activation to replace with; options:
        [relu, relu6, prelu, lrelu, swish]
    :param inplace: True to create the activation as an inplace, False otherwise
    :param num_channels: The number of channels to create the activation for
    :param kwargs: Additional kwargs to pass to the activation constructor
    :return: the created activation layer
    """
    layer = module
    layers = name.split(".")

    for lay in layers[:-1]:
        layer = layer.__getattr__(lay)

    cur = layer.__getattr__(layers[-1])

    if num_channels is None and hasattr(cur, "num_channels"):
        num_channels = cur.num_channels
    elif num_channels is None and hasattr(cur, "num_parameters"):
        num_channels = cur.num_parameters

    act = create_activation(
        act_type, inplace=inplace, num_channels=num_channels, **kwargs
    )
    layer.__setattr__(layers[-1], act)

    return act


def create_activation(
    act_type: str, inplace: bool, num_channels: int, **kwargs
) -> Module:
    """
    Create an activation function using the given parameters.

    :param act_type: the type of activation to replace with; options:
        [relu, relu6, prelu, lrelu, swish]
    :param inplace: True to create the activation as an inplace, False otherwise
    :param num_channels: The number of channels to create the activation for
    :param kwargs: Additional kwargs to pass to the activation constructor
    :return: the created activation layer
    """
    act_type = act_type.lower()

    if act_type == "relu":
        return ReLU(num_channels=num_channels, inplace=inplace)

    if act_type == "relu6":
        return ReLU6(num_channels=num_channels, inplace=inplace)

    if act_type == "prelu":
        return PReLU(num_parameters=num_channels, **kwargs)

    if act_type == "lrelu":
        return LeakyReLU(inplace=inplace, **kwargs)

    if act_type == "swish":
        return Swish(num_channels=num_channels)

    raise ValueError("unknown act_type given of {}".format(act_type))


def is_activation(module: Module) -> bool:
    """
    :param module: the module to check whether it is a common activation function or not
    :return: True if the module is an instance of a common activation function,
        False otherwise
    """
    return (
        isinstance(module, TReLU)
        or isinstance(module, TReLU6)
        or isinstance(module, ReLU)
        or isinstance(module, ReLU6)
        or isinstance(module, PReLU)
        or isinstance(module, LeakyReLU)
        or isinstance(module, Swish)
    )
