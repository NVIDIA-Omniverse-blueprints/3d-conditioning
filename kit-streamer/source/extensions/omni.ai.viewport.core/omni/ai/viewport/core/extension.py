# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

__all__ = ["AIViewportCoreExtension"]

import omni.ext
import omni.kit.app

from .models.comfy_ui.comfy_uplift import ComfyUplift
from .viewport_buffers_capture import ViewportBuffersCapture

_extension_instance = None


class AIViewportCoreExtension(omni.ext.IExt):
    """Viewport AI Core"""

    def on_startup(self):
        global _extension_instance
        _extension_instance = self

        # Utility to capture the various buffer of the viewport
        self._viewport_buffers_capture = ViewportBuffersCapture()
        self._uplift_model = ComfyUplift()

    def on_shutdown(self):
        global _extension_instance
        _extension_instance = None

        if self._viewport_buffers_capture:
            self._viewport_buffers_capture = None
        if self._uplift_model:
            self._uplift_model = None

    @staticmethod
    def get_instance():
        """
        Returns the instance of the extension.

        Returns:
            The instance of the extension.
        """
        return _extension_instance
