# Copyright (c) 2021 - present / Neuralmagic, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Modifiers classes related to magnitude pruning
"""

from typing import Dict, List, Union

import torch
from torch import Tensor
from torch.nn import Parameter

from sparseml.pytorch.optim.modifier import PyTorchModifierYAML
from sparseml.pytorch.sparsification.pruning.mask_creator import (
    FourBlockMaskCreator,
    PruningMaskCreator,
    UnstructuredPruningMaskCreator,
)
from sparseml.pytorch.sparsification.pruning.modifier_pruning_base import (
    BaseGradualPruningModifier,
)
from sparseml.pytorch.sparsification.pruning.scorer import PruningParamsScorer
from sparseml.sparsification import GMPruningModifier as BaseGMPruningModifier
from sparseml.utils import ALL_TOKEN


__all__ = [
    "MagnitudePruningParamsScorer",
    "MagnitudePruningModifier",
    "GMPruningModifier",
    "GlobalMagnitudePruningModifier",
]


class MagnitudePruningParamsScorer(PruningParamsScorer):
    """
    Scores parameters based on their magnitude

    :param params: list of model Parameters to track and score
    """

    def score_parameters(self) -> List[Tensor]:
        """
        :return: List of Tensors the same shapes as the given Parameters where
            each Parameter's elements are scored by their magnitude (absolute value)
        """
        return [torch.abs(param.data) for param in self._params]


@PyTorchModifierYAML()
class GMPruningModifier(BaseGradualPruningModifier, BaseGMPruningModifier):
    """
    Gradually applies kernel sparsity to a given parameter or parameters from
    init_sparsity until final_sparsity is reached over a given amount of time
    and applied with an interpolated function for each step taken.

    Applies based on magnitude pruning unless otherwise specified by mask_type.

    | Sample yaml:
    |   !GMPruningModifier
    |       init_sparsity: 0.05
    |       final_sparsity: 0.8
    |       start_epoch: 0.0
    |       end_epoch: 10.0
    |       update_frequency: 1.0
    |       params: ["re:.*weight"]
    |       leave_enabled: True
    |       inter_func: cubic
    |       log_types: __ALL__
    |       mask_type: unstructured

    :param init_sparsity: initial sparsity for each param to start with at
        start_epoch. __FROM_PARAM__ will set initial sparsity for each param to
        the existing sparsity level in that param
    :param final_sparsity: the final sparsity for the param to end with at end_epoch.
        Can also be a Dict of final sparsity values to a list of parameters to apply
        them to. If given a Dict, then params must be set to [] and the params to
        be pruned will be read from the final_sparsity Dict
    :param start_epoch: The epoch to start the modifier at
    :param end_epoch: The epoch to end the modifier at
    :param update_frequency: The number of epochs or fraction of epochs to update at
        between start and end
    :param params: A list of full parameter names or regex patterns of names to apply
        pruning to.  Regex patterns must be specified with the prefix 're:'. __ALL__
        will match to all parameters. __ALL_PRUNABLE__ will match to all ConvNd
        and Linear layers' weights. If a sparsity to param mapping is defined by
        final_sparsity, then params should be set to []
    :param leave_enabled: True to continue masking the weights after end_epoch,
        False to stop masking. Should be set to False if exporting the result
        immediately after or doing some other prune
    :param inter_func: the type of interpolation function to use:
        [linear, cubic, inverse_cubic]
    :param log_types: The loggers to allow the learning rate to be logged to,
        default is __ALL__
    :param mask_type: String to define type of sparsity to apply. May be 'unstructured'
        for unstructured pruning or 'block' for four block pruning
    """

    def __init__(
        self,
        init_sparsity: Union[float, str],
        final_sparsity: Union[float, Dict[float, List[str]]],
        start_epoch: float,
        end_epoch: float,
        update_frequency: float,
        params: Union[str, List[str]],
        leave_enabled: bool = True,
        inter_func: str = "cubic",
        log_types: Union[str, List[str]] = ALL_TOKEN,
        mask_type: str = "unstructured",
    ):
        super(GMPruningModifier, self).__init__(
            params=params,
            init_sparsity=init_sparsity,
            final_sparsity=final_sparsity,
            start_epoch=start_epoch,
            end_epoch=end_epoch,
            update_frequency=update_frequency,
            inter_func=inter_func,
            log_types=log_types,
            mask_type=mask_type,
            leave_enabled=leave_enabled,
            end_comparator=-1,
            global_sparsity=self._use_global_sparsity,
            allow_reintroduction=False,
            parent_class_kwarg_names=[
                "init_sparsity",
                "final_sparsity",
                "params",
                "leave_enabled",
                "mask_type",
            ],
        )

    def _get_mask_creator(
        self, param_names: List[str], params: List[Parameter]
    ) -> PruningMaskCreator:
        """
        :param names: full names of parameters to be pruned
        :param params: list of parameters to be masked
        :return: mask creator object to be used by this pruning algorithm
        """
        if self.mask_type == "unstructured":
            return UnstructuredPruningMaskCreator()
        elif self.mask_type == "block":
            return FourBlockMaskCreator()
        else:
            raise ValueError(
                f"Unknown mask_type {self.mask_type}. Supported mask types include "
                "'unstructured' and 'block'"
            )

    def _get_scorer(self, params: List[Parameter]) -> PruningParamsScorer:
        """
        :param params: list of Parameters for scorer to track
        :return: param scorer object to be used by this pruning algorithm
        """
        return MagnitudePruningParamsScorer(params)

    @property
    def _use_global_sparsity(self) -> bool:
        # base GMPruningModifier will not support global sparsity
        return False


@PyTorchModifierYAML()
class MagnitudePruningModifier(GMPruningModifier):
    """
    Gradually applies kernel sparsity to a given parameter or parameters from
    init_sparsity until final_sparsity is reached over a given amount of time
    and applied with an interpolated function for each step taken.

    Applies based on magnitude pruning unless otherwise specified by mask_type.

    | Sample yaml:
    |   !MagnutidePruningModifier
    |       init_sparsity: 0.05
    |       final_sparsity: 0.8
    |       start_epoch: 0.0
    |       end_epoch: 10.0
    |       update_frequency: 1.0
    |       params: ["re:.*weight"]
    |       leave_enabled: True
    |       inter_func: cubic
    |       log_types: __ALL__
    |       mask_type: unstructured

    :param init_sparsity: initial sparsity for each param to start with at
        start_epoch. __FROM_PARAM__ will set initial sparsity for each param to
        the existing sparsity level in that param
    :param final_sparsity: the final sparsity for the param to end with at end_epoch.
        Can also be a Dict of final sparsity values to a list of parameters to apply
        them to. If given a Dict, then params must be set to [] and the params to
        be pruned will be read from the final_sparsity Dict
    :param start_epoch: The epoch to start the modifier at
    :param end_epoch: The epoch to end the modifier at
    :param update_frequency: The number of epochs or fraction of epochs to update at
        between start and end
    :param params: A list of full parameter names or regex patterns of names to apply
        pruning to.  Regex patterns must be specified with the prefix 're:'. __ALL__
        will match to all parameters. __ALL_PRUNABLE__ will match to all ConvNd
        and Linear layers' weights. If a sparsity to param mapping is defined by
        final_sparsity, then params should be set to []
    :param leave_enabled: True to continue masking the weights after end_epoch,
        False to stop masking. Should be set to False if exporting the result
        immediately after or doing some other prune
    :param inter_func: the type of interpolation function to use:
        [linear, cubic, inverse_cubic]
    :param log_types: The loggers to allow the learning rate to be logged to,
        default is __ALL__
    :param mask_type: String to define type of sparsity to apply. May be 'unstructred'
        for unstructured pruning or 'block' for four block pruning
    """

    # just an alias for GMPruningModifier
    pass


@PyTorchModifierYAML()
class GlobalMagnitudePruningModifier(GMPruningModifier):
    """
    Gradually applies kernel sparsity to a given parameter or parameters from
    init_sparsity until final_sparsity is reached over a given amount of time
    and applied with an interpolated function for each step taken.

    Applies based on magnitude pruning unless otherwise specified by mask_type.

    | Sample yaml:
    |   !GlobalMagnitudePruningModifier
    |       init_sparsity: 0.05
    |       final_sparsity: 0.8
    |       start_epoch: 0.0
    |       end_epoch: 10.0
    |       update_frequency: 1.0
    |       params: ["re:.*weight"]
    |       leave_enabled: True
    |       inter_func: cubic
    |       log_types: __ALL__
    |       mask_type: unstructured

    :param init_sparsity: initial sparsity for each param to start with at
        start_epoch. __FROM_PARAM__ will set initial sparsity for each param to
        the existing sparsity level in that param
    :param final_sparsity: the final sparsity for the param to end with at end_epoch.
        Can also be a Dict of final sparsity values to a list of parameters to apply
        them to. If given a Dict, then params must be set to [] and the params to
        be pruned will be read from the final_sparsity Dict
    :param start_epoch: The epoch to start the modifier at
    :param end_epoch: The epoch to end the modifier at
    :param update_frequency: The number of epochs or fraction of epochs to update at
        between start and end
    :param params: A list of full parameter names or regex patterns of names to apply
        pruning to.  Regex patterns must be specified with the prefix 're:'. __ALL__
        will match to all parameters. __ALL_PRUNABLE__ will match to all ConvNd
        and Linear layers' weights. If a sparsity to param mapping is defined by
        final_sparsity, then params should be set to []
    :param leave_enabled: True to continue masking the weights after end_epoch,
        False to stop masking. Should be set to False if exporting the result
        immediately after or doing some other prune
    :param inter_func: the type of interpolation function to use:
        [linear, cubic, inverse_cubic]
    :param log_types: The loggers to allow the learning rate to be logged to,
        default is __ALL__
    :param mask_type: String to define type of sparsity to apply. May be 'unstructred'
        for unstructured pruning or 'block' for four block pruning
    """

    def __init__(
        self,
        init_sparsity: Union[float, str],
        final_sparsity: Union[float, Dict[float, List[str]]],
        start_epoch: float,
        end_epoch: float,
        update_frequency: float,
        params: Union[str, List[str]],
        leave_enabled: bool = True,
        inter_func: str = "cubic",
        log_types: Union[str, List[str]] = ALL_TOKEN,
        mask_type: str = "unstructured",
    ):
        super(GlobalMagnitudePruningModifier, self).__init__(
            params=params,
            init_sparsity=init_sparsity,
            final_sparsity=final_sparsity,
            start_epoch=start_epoch,
            end_epoch=end_epoch,
            update_frequency=update_frequency,
            inter_func=inter_func,
            log_types=log_types,
            mask_type=mask_type,
            leave_enabled=leave_enabled,
        )

    @property
    def _use_global_sparsity(self) -> bool:
        return True
