# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import asyncio
from typing import Optional, Tuple

import omni.kit.viewport.utility as vp_util
from omni.kit.widget.viewport.capture import ByteCapture
import omni.ui as ui


class ViewportSuppress:
    """
    A class to suppress the viewport display.
    """

    def __init__(self, viewport_frame_name: str = "Viewport Frame Suppress"):
        """
        Initialize the ViewportSuppress instance.

        Args:
            viewport_frame_name (str): Name of the viewport frame to suppress.
        """
        self._viewport_frame_name: str = viewport_frame_name
        self._viewport_api, self._viewport_window = self._get_viewport()
        self._byte_provider: Optional[ui.ByteImageProvider] = None

    def __del__(self):
        """Cleanup when the instance is deleted."""
        self._end()

    async def begin(self) -> None:
        """
        Begin viewport suppression by capturing and displaying a static image.
        """
        await self._viewport_api.schedule_capture(ByteCapture(self._on_capture_completed)).wait_for_result()

    async def end(self) -> None:
        """
        End viewport suppression and restore normal viewport display.
        """
        self._end()

    def _get_viewport(self) -> Tuple["ViewportAPI", ui.Window]:
        """
        Get the active viewport and window.

        Returns:
            Tuple[vp_util.ViewportAPI, vp_util.ViewportWindow]: Active viewport and window.
        """
        return vp_util.get_active_viewport_and_window()

    def _on_capture_completed(self, buffer: bytes, buffer_size: int, width: int, height: int, format) -> None:
        """
        Callback function when viewport capture is completed.

        Args:
            buffer (bytes): Captured image buffer.
            buffer_size (int): Size of the buffer.
            width (int): Width of the captured image.
            height (int): Height of the captured image.
            format: Format of the captured image.
        """
        with self._viewport_window.get_frame(self._viewport_frame_name):
            with ui.ZStack():
                # Image on top of the viewport
                self._byte_provider = ui.ByteImageProvider()
                self._byte_provider.set_raw_bytes_data(buffer, [width, height], format)
                ui.ImageWithProvider(self._byte_provider, fill_policy=ui.IwpFillPolicy.IWP_STRETCH)
                # A small overlay label
                with ui.VStack():
                    ui.Spacer()
                    ui.Label(
                        "Capturing", style={"color": ui.color(0, 0, 0, 10)}, alignment=ui.Alignment.CENTER, height=0
                    )

    def _end(self) -> None:
        """
        Internal method to end viewport suppression and clean up resources.
        """
        if self._viewport_window is not None:
            self._viewport_window.get_frame(self._viewport_frame_name).clear()
            self._viewport_api = None
            self._viewport_window = None
            self._byte_provider = None
