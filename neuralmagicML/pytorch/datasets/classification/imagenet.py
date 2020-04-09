"""
Imagenet dataset implementations for the image classification field in computer vision.
More info for the dataset can be found `here <http://www.image-net.org/>`__.
"""

import os
import random
import PIL.Image as Image

from torchvision import transforms
from torchvision.datasets import ImageFolder

from neuralmagicML.pytorch.datasets.registry import DatasetRegistry
from neuralmagicML.pytorch.datasets.generic import default_dataset_path


__all__ = ["ImageNetDataset"]


_RGB_MEANS = [0.485, 0.456, 0.406]
_RGB_STDS = [0.229, 0.224, 0.225]


@DatasetRegistry.register(
    key=["imagenet"],
    attributes={
        "num_classes": 1000,
        "transform_means": _RGB_MEANS,
        "transform_stds": _RGB_STDS,
    },
)
class ImageNetDataset(ImageFolder):
    """
    Wrapper for the ImageNet dataset to apply standard transforms.

    :param root: The root folder to find the dataset at, if not found will
        download here if download=True
    :param train: True if this is for the training distribution,
        False for the validation
    :param rand_trans: True to apply RandomCrop and RandomHorizontalFlip to the data,
        False otherwise
    :param image_size: the size of the image to output from the dataset
    """

    def __init__(
        self,
        root: str = default_dataset_path("imagenet"),
        train: bool = True,
        rand_trans: bool = False,
        image_size: int = 224,
    ):
        non_rand_resize_scale = 256.0 / 224.0  # standard used
        init_trans = (
            [
                transforms.RandomResizedCrop(image_size),
                transforms.RandomHorizontalFlip(),
            ]
            if rand_trans
            else [
                transforms.Resize(
                    round(non_rand_resize_scale * image_size),
                    interpolation=Image.BICUBIC,
                ),
                transforms.CenterCrop(image_size),
            ]
        )

        trans = [
            *init_trans,
            transforms.ToTensor(),
            transforms.Normalize(mean=_RGB_MEANS, std=_RGB_STDS),
        ]
        root = os.path.join(
            os.path.abspath(os.path.expanduser(root)), "train" if train else "val"
        )

        super().__init__(root, transform=transforms.Compose(trans))

        if train:
            # make sure we don't preserve the folder structure class order
            random.shuffle(self.samples)
