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

import torch


def pruning_modifier_serialization_vals_test(
    yaml_modifier, serialized_modifier, obj_modifier
):
    assert (
        yaml_modifier.init_sparsity
        == serialized_modifier.init_sparsity
        == obj_modifier.init_sparsity
    )
    assert (
        yaml_modifier.final_sparsity
        == serialized_modifier.final_sparsity
        == obj_modifier.final_sparsity
    )
    assert (
        yaml_modifier.start_epoch
        == serialized_modifier.start_epoch
        == obj_modifier.start_epoch
    )
    assert (
        yaml_modifier.end_epoch
        == serialized_modifier.end_epoch
        == obj_modifier.end_epoch
    )
    assert (
        yaml_modifier.update_frequency
        == serialized_modifier.update_frequency
        == obj_modifier.update_frequency
    )
    assert yaml_modifier.params == serialized_modifier.params == obj_modifier.params
    assert (
        yaml_modifier.inter_func
        == serialized_modifier.inter_func
        == obj_modifier.inter_func
    )
    assert (
        str(yaml_modifier.mask_type)
        == str(serialized_modifier.mask_type)
        == str(obj_modifier.mask_type)
    )


def state_dict_save_load_test(
    test_obj,
    modifier_lambda,
    model_lambda,
    optim_lambda,
    test_steps_per_epoch,  # noqa: F811
    is_gm_pruning,
):
    # test state dict serialization/deserialization for pruning modifiers
    modifier = modifier_lambda()
    model = model_lambda()
    optimizer = optim_lambda(model)
    test_obj.initialize_helper(modifier, model)
    # apply first mask
    modifier.scheduled_update(
        model, optimizer, modifier.start_epoch, test_steps_per_epoch
    )
    # get state dict
    state_dict = modifier.state_dict()
    applied_sparsities = modifier.applied_sparsity if is_gm_pruning else None
    if not isinstance(applied_sparsities, list):
        applied_sparsities = [applied_sparsities] * len(state_dict)
    for mask, applied_sparsity in zip(state_dict.values(), applied_sparsities):
        if is_gm_pruning:
            # check that the mask sparsity is the applied one leaving a relatively
            # large margin of error since parameter sizes are small so the exact
            # sparsity cannot always be attained
            assert abs(1 - (mask.sum() / mask.numel()) - applied_sparsity) < 0.05
        else:
            # all weights should be non zero, pending randomness, so the mask should be
            # all ones for this constant_pruning modifier
            assert mask.sum() / mask.numel() >= 0.99

    # check that changing the state dict masks to all 0s and reapplying will affect
    # the model parameters
    for mask in state_dict.values():
        mask.mul_(0.0)
    modifier.load_state_dict(state_dict)
    param_names = {mask_name.split(".sparsity_mask")[0] for mask_name in state_dict}
    for param_name, param in model.named_parameters():
        if param_name in param_names:
            # check that the all zero mask has been applied
            assert torch.all(param == 0.0)
