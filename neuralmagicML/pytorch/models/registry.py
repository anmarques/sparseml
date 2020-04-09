"""
Code related to the PyTorch model registry for easily creating models.
"""

from typing import Union, List, Callable, Dict, Any, Tuple
from merge_args import merge_args
from torch.nn import Module

from neuralmagicML.utils.frameworks import PYTORCH_FRAMEWORK
from neuralmagicML.utils import RepoModel, wrapper_decorator
from neuralmagicML.pytorch.utils import load_model


__all__ = ["ModelRegistry"]


class ModelRegistry(object):
    """
    Registry class for creating models
    """

    _CONSTRUCTORS = {}
    _INPUT_SHAPES = {}

    @staticmethod
    def create(
        key: str,
        pretrained: Union[bool, str] = False,
        pretrained_path: str = None,
        pretrained_dataset: str = None,
        load_strict: bool = True,
        ignore_error_tensors: List[str] = None,
        pre_load_func: Callable[[Module], Module] = None,
        post_load_func: Callable[[Module], Module] = None,
        **kwargs
    ) -> Module:
        """
        Create a new model for the given key

        :param key: the model key (name) to create
        :param pretrained: True to load pretrained weights; to load a specific version
            give input a string with the name of the version, default None
        :param pretrained_path: A model file path to load into the created model
        :param pretrained_dataset: The dataset to load for the model
        :param load_strict: True to make sure all states are found in and
            loaded in model, False otherwise; default True
        :param ignore_error_tensors: tensors to ignore if there are errors in loading
        :param pre_load_func: a function to run before loading the pretrained weights
        :param post_load_func: a function to run after loading the pretrained weights
        :param kwargs: any keyword args to supply to the model constructor
        :return: the instantiated model
        """
        if key not in ModelRegistry._CONSTRUCTORS:
            raise ValueError(
                "key {} is not in the model registry; available: {}".format(
                    key, ModelRegistry._CONSTRUCTORS
                )
            )

        return ModelRegistry._CONSTRUCTORS[key](
            pretrained=pretrained,
            pretrained_path=pretrained_path,
            pretrained_dataset=pretrained_dataset,
            load_strict=load_strict,
            ignore_error_tensors=ignore_error_tensors,
            pre_load_func=pre_load_func,
            post_load_func=post_load_func,
            **kwargs
        )

    @staticmethod
    def input_shape(key: str):
        """
        :param key: the model key (name) to create
        :return: the specified input shape for the model
        """
        if key not in ModelRegistry._CONSTRUCTORS:
            raise ValueError(
                "key {} is not in the model registry; available: {}".format(
                    key, ModelRegistry._CONSTRUCTORS
                )
            )

        return ModelRegistry._INPUT_SHAPES[key]

    @staticmethod
    def register(
        key: Union[str, List[str]],
        input_shape: Any,
        domain: str,
        sub_domain: str,
        architecture: str,
        sub_architecture: str,
        default_dataset: str,
        default_desc: str,
        def_ignore_error_tensors: List[str] = None,
        desc_args: Dict[str, Tuple[str, Any]] = None,
    ):
        """
        Register a model with the registry. Should be used as a decorator

        :param key: the model key (name) to create
        :param input_shape: the specified input shape for the model
        :param domain: the domain the model belongs to; ex: cv, nlp, etc
        :param sub_domain: the sub domain the model belongs to;
            ex: classification, detection, etc
        :param architecture: the architecture the model belongs to;
            ex: resnet, mobilenet, etc
        :param sub_architecture: the sub architecture the model belongs to;
            ex: 50, 101, etc
        :param default_dataset: the dataset to use by default for loading
            pretrained if not supplied
        :param default_desc: the description to use by default for loading
            pretrained if not supplied
        :param def_ignore_error_tensors: tensors to ignore if there are
            errors in loading
        :param desc_args: args that should be changed based on the description
        :return: the decorator
        """
        if not isinstance(key, List):
            key = [key]

        def decorator(const_func):
            const = ModelRegistry._registered_wrapper(
                const_func,
                domain,
                sub_domain,
                architecture,
                sub_architecture,
                default_dataset,
                default_desc,
                def_ignore_error_tensors,
                desc_args,
            )

            for r_key in key:
                if r_key in ModelRegistry._CONSTRUCTORS:
                    raise ValueError("key {} is already registered".format(key))

                ModelRegistry._CONSTRUCTORS[r_key] = const
                ModelRegistry._INPUT_SHAPES[r_key] = input_shape

            return const

        return decorator

    @staticmethod
    def _registered_wrapper(
        const_func: Callable,
        domain: str,
        sub_domain: str,
        architecture: str,
        sub_architecture: str,
        default_dataset: str,
        default_desc: str,
        def_ignore_error_tensors: List[str] = None,
        desc_args: Dict[str, Tuple[str, Any]] = None,
    ):
        @merge_args(const_func)
        @wrapper_decorator(const_func)
        def wrapper(
            pretrained_path: str = None,
            pretrained: Union[bool, str] = False,
            pretrained_dataset: str = None,
            load_strict: bool = True,
            ignore_error_tensors: List[str] = None,
            pre_load_func: Callable[[Module], Module] = None,
            post_load_func: Callable[[Module], Module] = None,
            *args,
            **kwargs
        ):
            """
            :param pretrained_path: A path to the pretrained weights to load,
                if provided will override the pretrained param
            :param pretrained: True to load the default pretrained weights,
                a string to load a specific pretrained weight
                (ex: dense, recal, recal-perf),
                or False to not load any pretrained weights
            :param pretrained_dataset: The dataset to load pretrained weights for
                (ex: imagenet, mnist, etc).
                If not supplied will default to the one preconfigured for the model.
            :param load_strict: True to raise an error on issues with state dict
                loading from pretrained_path or pretrained, False to ignore
            :param ignore_error_tensors: Tensors to ignore while checking the state dict
                for weights loaded from pretrained_path or pretrained
            :param pre_load_func: A function to run over the created Model before
                weights can be loaded
            :param post_load_func: A function to run over the created Model after
                weights have been loaded
            """
            if desc_args and pretrained in desc_args:
                kwargs[desc_args[pretrained][0]] = desc_args[pretrained[1]]

            model = const_func(*args, **kwargs)
            ignore = []

            if ignore_error_tensors:
                ignore.extend(ignore_error_tensors)
            elif def_ignore_error_tensors:
                ignore.extend(def_ignore_error_tensors)

            if pre_load_func:
                model = pre_load_func(model)

            if pretrained_path:
                load_model(pretrained_path, model, load_strict, ignore)
            elif pretrained:
                desc = pretrained if isinstance(pretrained, str) else default_desc
                dataset = pretrained_dataset if pretrained_dataset else default_dataset
                repo_model = RepoModel(
                    domain,
                    sub_domain,
                    architecture,
                    sub_architecture,
                    dataset,
                    PYTORCH_FRAMEWORK,
                    desc,
                )
                try:
                    paths = repo_model.download_framework_files()
                    load_model(paths[0], model, load_strict, ignore)
                except Exception as ex:
                    # try one more time with overwrite on in case file was corrupted
                    paths = repo_model.download_framework_files(overwrite=True)
                    load_model(paths[0], model, load_strict, ignore)

            if post_load_func:
                model = post_load_func(model)

            return model

        return wrapper
