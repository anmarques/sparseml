import pytest

from onnx import load_model
from neuralmagicML.onnx.utils import (
    extract_node_id,
    extract_node_shapes,
    get_node_by_id,
    get_init_by_name,
    NodeParam,
    conv_node_params,
    gemm_node_params,
    matmul_node_params,
    get_node_params,
    get_prunable_nodes,
    onnx_nodes_sparsities,
    SparsityMeasurement,
)
from neuralmagicML.utils import available_models

from tests.onnx.helpers import extract_node_models


def test_onnx_node_sparsities():
    # runs through nearly all other onnx functions imported above as well
    models = available_models(
        domains=["cv"],
        sub_domains=["classification"],
        architectures=["mobilenet-v1"],
        datasets=["imagenet"],
        descs=["recal-perf"],
    )
    assert len(models) > 0

    for model in models:
        file_path = model.download_onnx_file()

        tot, nodes = onnx_nodes_sparsities(file_path)

        assert len(nodes) == 28

        assert isinstance(tot, SparsityMeasurement)
        assert tot.sparsity > 0.5
        assert tot.params_count == 4209088
        assert tot.params_zero_count > 0.5 * tot.params_count

        for node, val in nodes.items():
            assert isinstance(val, SparsityMeasurement)
            assert val.params_count > 0

            if "sections" not in node and "classifier" not in node:
                continue

            if (
                "depth" in node
                or "sections.0" in node
                or "sections_0" in node
                or "sections.1" in node
                or "sections_1" in node
            ):
                continue

            assert val.sparsity > 0.2
            assert val.sparsity < 0.95
            assert val.params_zero_count > 0


def test_extract_node_shape(extract_node_models):
    model_path, expected_output = extract_node_models
    onnx_model = load_model(model_path)
    node_shapes = extract_node_shapes(onnx_model)
    for node in node_shapes:
        assert node_shapes[node].input_shapes == expected_output[node][0]
        assert node_shapes[node].output_shapes == expected_output[node][1]
