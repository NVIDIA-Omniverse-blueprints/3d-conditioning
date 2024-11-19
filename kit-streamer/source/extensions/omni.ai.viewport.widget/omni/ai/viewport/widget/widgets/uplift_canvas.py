# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

__all__ = ["UpliftCanvas"]

from typing import List

import omni.ui as ui
from carb.input import KeyboardInput as Key

from .byte_image import ByteImage


class UpliftCanvas:
    def __init__(self):
        self._frame = ui.Frame()
        with self._frame:
            self._canvas = ui.CanvasFrame(draggable=True, style_type_name_override="UpliftCanvas")
            with self._canvas:
                self._image = ByteImage()
        self._canvas.set_key_pressed_fn(self._on_key_pressed)

    def destroy(self):
        self._canvas.destroy()
        self._canvas = None
        self._image.destroy()
        self._image = None

    def _on_key_pressed(self, key: int, key_mod: int, key_down: bool):
        key = Key(key)  # Convert to enumerated type

        if key == Key.F and key_down:
            self.fit_image()

        if key == Key.R:
            self.reset_image()

    def update_image(self, pixels: List[int], size: List[int]):
        if pixels:
            self._image.update_image(pixels, size)
            self.fit_image()

    def reset_image(self):
        """This will reset the image to fit the view"""
        self._canvas.pan_x = 0
        self._canvas.pan_y = 0

        self._canvas.zoom = 1

    def fit_image(self):
        image_size = self._image.get_size()
        frame_size = (self._frame.computed_width, self._frame.computed_height)
        fit_zoom = min(frame_size[0] / image_size[0], frame_size[1] / image_size[1])

        print(f"Image size: {image_size}")
        print(f"Frame size: {frame_size}")
        print(f"Calculated fit zoom: {fit_zoom}")

        # Calculate the centered position
        centered_x = (frame_size[0] - image_size[0] * fit_zoom) / 4 / fit_zoom
        centered_y = (frame_size[1] - image_size[1] * fit_zoom) / 4 / fit_zoom

        print(f"Centered position: x = {centered_x}, y = {centered_y}")

        # Apply zoom and centering
        self._canvas.zoom = fit_zoom
        self._canvas.pan_x = centered_x
        self._canvas.pan_y = 0 # centered_y

        print(f"Applied zoom: {self._canvas.zoom}")
        print(f"Applied pan: x = {self._canvas.pan_x}, y = {self._canvas.pan_y}")
