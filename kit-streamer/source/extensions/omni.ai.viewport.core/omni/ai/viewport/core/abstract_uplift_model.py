# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import base64
from typing import List, Tuple

import omni.ui as ui


class AbstractUpliftModel:
    def __init__(self):
        # Hold the base64 of the different buffers of the viewport
        self._viewport_buffers = {}

        # Hold the parameters of the model and their values
        self._parameters = {}
        self._init_parameters()

    def reset_parameters(self):
        self._viewport_buffers = {}
        self._parameters = {}
        self._init_parameters()

    def get_available_mode(self) -> List[str]:
        return []

    def set_mode(self, mode: str):
        pass

    def destroy(self):
        pass

    def _init_parameters(self):
        """Initialize the parameters"""
        params_spec = self.get_parameters_spec()
        for param in params_spec:
            self._parameters[param["name"]] = param["default_value"]

    def set_parameters(self, name: str, value_type: str, value):
        """Set the value of a parameter"""
        if value_type == "float":
            self._parameters[name] = value
        elif value_type == "int":
            self._parameters[name] = value
        elif value_type == "string":
            self._parameters[name] = value
        elif value_type == "image":
            path = value
            with open(path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            self._parameters[name] = base64_image
        else:
            raise ValueError("Invalid value type")

        print(f"set_parameters {name} {self._parameters[name]}")

    def get_parameters_spec(self) -> dict:
        """Return the list of parameters names, tupe and default values"""
        pass

    def update_viewport_buffers(self, viewport_buffers: dict):
        """Update the viewport buffers"""
        self._viewport_buffers = viewport_buffers.copy()

    def generate(self, progress_model: ui.SimpleFloatModel = None, **kwargs) -> Tuple[list, list]:
        """
        Generate the uplifted image and return it as base64
        by default will use the internal parameters and their default
        but they can be overridden by the kwargs

        return the list of bytes as unit8 and [width, height]
        """
        pass
