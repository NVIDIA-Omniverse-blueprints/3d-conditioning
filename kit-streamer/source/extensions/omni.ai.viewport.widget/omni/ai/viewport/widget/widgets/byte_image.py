# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

__all__ = ["ByteImage"]

import functools
import pathlib
from typing import List, Tuple

import carb.settings
import omni.kit.app
import omni.ui as ui


@functools.lru_cache()
def get_extension_path():
    return pathlib.Path(omni.kit.app.get_app().get_extension_manager().get_extension_path_by_module(__name__))


class ByteImage:
    def __init__(self):
        # The image
        self._image_with_provider = None

        # The content of the viewport
        self._byte_provider = None

        # Preview image
        settings = carb.settings.get_settings()
        preview = settings.get("/exts/omni.ai.viewport.widget/preview_image") or "coffee_machine_0.png"
        self._preview_provider = ui.RasterImageProvider(f"{get_extension_path()}/data/{preview}")

        # We build the frame of the viewport
        self._frame = ui.Frame(width=512, height=512)
        self._frame.set_build_fn(self._build_fn)

    def destroy(self):
        self._frame.destroy()
        self._frame = None
        if self._byte_provider:
            self._byte_provider.destroy()
            self._byte_provider = None
        if self._preview_provider:
            self._preview_provider.destroy()
            self._preview_provider = None

    def get_size(self) -> Tuple[int, int]:
        """Return the current image size as a tuple of (width, height)."""
        return (self._image_with_provider.width.value, self._image_with_provider.height.value)

    def _build_fn(self):
        provider = self._byte_provider or self._preview_provider
        self._image_with_provider = ui.ImageWithProvider(
            provider,
            name="previewImage",
            style={
                "ImageWithProvider": {
                    "fill_policy": ui.IwpFillPolicy.IWP_PRESERVE_ASPECT_CROP,
                    "alignment": ui.Alignment.CENTER_BOTTOM,
                }
            },
        )

    # update the image
    def update_image(self, pixels: List[int], size: List[int]):
        """Update the image with new pixel data and size."""
        if not self._byte_provider:
            self._byte_provider = ui.ByteImageProvider()

            with self._frame:
                self._build_fn()

        if pixels:
            self._image_with_provider.width = ui.Pixel(size[0])
            self._image_with_provider.height = ui.Pixel(size[1])
            self._byte_provider.set_bytes_data(pixels, size)
