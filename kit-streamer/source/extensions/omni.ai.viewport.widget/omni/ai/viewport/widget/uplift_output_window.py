# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

__all__ = ["UpliftOutputWindow"]

import asyncio

import carb
import omni.ui as ui
from omni.ai.viewport.core import AIViewportCoreExtension
from omni.ai.viewport.core.abstract_uplift_model import AbstractUpliftModel

from .style import get_style
from .widgets.uplift_canvas import UpliftCanvas
from .widgets.uplift_parameters import UpliftParameterWidget


class UpliftOutputWindow(ui.Window):
    def __init__(self, title: str, uplift_model: AbstractUpliftModel, **kwargs):
        super().__init__(title, **kwargs)

        # Hold the uplift canvas
        self._uplift_canvas = None
        self._uplift_model = None
        # set the uplift model and do the init
        self.set_uplift_model(uplift_model)

        self._mode_context_menu = ui.Menu()

        # Apply the style to all the widgets of this window
        self.frame.style = get_style()

        # Set the function that is called to build widgets when the window is
        self.frame.set_build_fn(self._build_fn)

    def destroy(self):
        if self._uplift_canvas:
            self._uplift_canvas.destroy()
            self._uplift_canvas = None

        if self._uplift_model:
            # self._uplift_model.destroy()
            self._uplift_model = None

        super().destroy()

    def set_uplift_model(self, uplift_model: AbstractUpliftModel):
        # The Model/API that generate the Uplift version of the Viewport
        self._uplift_model = uplift_model

    def _set_mode(self, mode: str):
        self._uplift_model.set_mode(mode)

        # Rebuild the connection
        self.set_uplift_model(self._uplift_model)
        # self._uplift_parameter_widget.set_uplift_model(self._uplift_model)

    def _show_mode_context_menu(self, x, y, button, modifier):
        """The context menu to copy the text"""
        # Display context menu only if the right button is pressed
        if button != 1:
            return

        # Reset the previous context popup
        self._mode_context_menu.clear()
        modes = self._uplift_model.get_available_mode()

        with self._mode_context_menu:
            for mode in modes:
                ui.MenuItem(mode, triggered_fn=lambda mode=mode: self._set_mode(mode))

        # Show it
        self._mode_context_menu.show()

    def _build_fn(self):
        with ui.VStack(spacing=5) as stack:
            # Uplift Canvas
            self._uplift_canvas = UpliftCanvas()

        stack.set_mouse_pressed_fn(self._show_mode_context_menu)
