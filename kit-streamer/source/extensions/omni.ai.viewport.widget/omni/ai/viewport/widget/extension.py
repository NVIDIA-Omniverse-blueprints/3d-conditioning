# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

__all__ = ["AIViewportWidgetExtension"]

import asyncio
from functools import partial

import omni.ext
import omni.kit.app
import omni.kit.ui
import omni.ui as ui
from omni.ai.viewport.core import AIViewportCoreExtension


class AIViewportWidgetExtension(omni.ext.IExt):
    """Viewport AI Widget"""

    INPUT_WINDOW_NAME = "Viewport AI Widget for Input"
    OUTPUT_WINDOW_NAME = "Viewport AI Widget for Output"
    INPUT_MENU_PATH = f"Window/{INPUT_WINDOW_NAME}"
    OUTPUT_MENU_PATH = f"Window/{OUTPUT_WINDOW_NAME}"
    WIN_WIDTH = 720
    WIN_HEIGHT = 800

    def on_startup(self):
        self._input_window = None
        self._output_window = None

        # The ability to show the window if the system requires it. We use it in QuickLayout.
        ui.Workspace.set_show_window_fn(
            AIViewportWidgetExtension.INPUT_WINDOW_NAME, partial(self.show_input_window, True)
        )
        ui.Workspace.set_show_window_fn(
            AIViewportWidgetExtension.OUTPUT_WINDOW_NAME, partial(self.show_output_window, True)
        )

        # Add the new menu
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            self._menu = editor_menu.add_item(
                AIViewportWidgetExtension.INPUT_MENU_PATH, self.show_input_window, toggle=True, value=True
            )
            self._menu = editor_menu.add_item(
                AIViewportWidgetExtension.OUTPUT_MENU_PATH, self.show_output_window, toggle=True, value=True
            )

        # Show the window. It will call `self.show_window`
        ui.Workspace.show_window(AIViewportWidgetExtension.INPUT_WINDOW_NAME, True)
        ui.Workspace.show_window(AIViewportWidgetExtension.OUTPUT_WINDOW_NAME, True)

    def on_shutdown(self):
        self._menu = None
        if self._input_window:
            self._input_window.destroy()
            self._input_window = None
        if self._output_window:
            self._output_window.destroy()
            self._output_window = None

        # Deregister the function that shows the window from omni.ui
        ui.Workspace.set_show_window_fn(AIViewportWidgetExtension.INPUT_WINDOW_NAME, None)
        ui.Workspace.set_show_window_fn(AIViewportWidgetExtension.OUTPUT_WINDOW_NAME, None)

    def _set_input_menu(self, value):
        """Set the menu to create this window on and off"""
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            editor_menu.set_value(AIViewportWidgetExtension.INPUT_MENU_PATH, value)

    def _set_output_menu(self, value):
        """Set the menu to create this window on and off"""
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            editor_menu.set_value(AIViewportWidgetExtension.OUTPUT_MENU_PATH, value)

    async def _destroy_input_window_async(self):
        # Wait one frame, this is due to the one frame defer in Window::_moveToMainOSWindow()
        await omni.kit.app.get_app().next_update_async()
        if self._input_window:
            self._input_window.destroy()
            self._input_window = None

    async def _destroy_output_window_async(self):
        # Wait one frame, this is due to the one frame defer in Window::_moveToMainOSWindow()
        await omni.kit.app.get_app().next_update_async()
        if self._output_window:
            self._output_window.destroy()
            self._output_window = None

    def _visibility_input_changed_fn(self, visible):
        # Called when the user presses "X"
        self._set_input_menu(visible)
        if not visible:
            # Destroy the window, since we are creating a new window in show_window
            asyncio.ensure_future(self._destroy_input_window_async())

    def _visibility_output_changed_fn(self, visible):
        # Called when the user presses "X"
        self._set_output_menu(visible)
        if not visible:
            # Destroy the window, since we are creating a new window in show_window
            asyncio.ensure_future(self._destroy_output_window_async())

    def show_input_window(self, menu, value):
        if value:
            from .uplift_input_window import UpliftInputWindow

            viewport_core_instance = AIViewportCoreExtension.get_instance()

            self._uplift_model = viewport_core_instance._uplift_model
            self._input_window = UpliftInputWindow(
                AIViewportWidgetExtension.INPUT_WINDOW_NAME,
                self._uplift_model,
                self,
                width=AIViewportWidgetExtension.WIN_WIDTH,
                height=AIViewportWidgetExtension.WIN_HEIGHT,
            )
            self._input_window.set_visibility_changed_fn(self._visibility_input_changed_fn)
        elif self._input_window:
            self._input_window.visible = False

    def show_output_window(self, menu, value):
        if value:
            from .uplift_output_window import UpliftOutputWindow

            viewport_core_instance = AIViewportCoreExtension.get_instance()

            self._uplift_model = viewport_core_instance._uplift_model
            self._output_window = UpliftOutputWindow(
                AIViewportWidgetExtension.OUTPUT_WINDOW_NAME,
                self._uplift_model,
                width=AIViewportWidgetExtension.WIN_WIDTH,
                height=AIViewportWidgetExtension.WIN_HEIGHT,
            )
            self._output_window.set_visibility_changed_fn(self._visibility_output_changed_fn)
        elif self._output_window:
            self._output_window.visible = False
