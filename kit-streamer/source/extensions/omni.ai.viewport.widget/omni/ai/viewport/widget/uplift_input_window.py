# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

__all__ = ["UpliftInputWindow"]

import asyncio
import base64
import functools
import io
import pathlib
import json

import carb
import carb.events
import omni.kit.app
import omni.kit.livestream.messaging as messaging
import omni.ui as ui
from omni.ai.viewport.core import AIViewportCoreExtension
from omni.ai.viewport.core.abstract_uplift_model import AbstractUpliftModel
from PIL import Image

from .style import get_style
from .widgets.uplift_canvas import UpliftCanvas
from .widgets.uplift_parameters import UpliftParameterWidget


@functools.lru_cache()
def get_extension_path():
    return pathlib.Path(omni.kit.app.get_app().get_extension_manager().get_extension_path_by_module(__name__))


class UpliftInputWindow(ui.Window):
    def __init__(self, title: str, uplift_model: AbstractUpliftModel, ext, **kwargs):
        super().__init__(title, **kwargs)

        # Utility to capture the various buffer of the viewport
        viewport_core_instance = AIViewportCoreExtension.get_instance()
        self._viewport_buffers_capture = viewport_core_instance._viewport_buffers_capture

        # Hold the uplift canvas
        self._uplift_canvas = None
        self._ext = ext
        self._uplift_model = None
        # set the uplift model and do the init
        self.set_uplift_model(uplift_model)

        # Auto update the viewport
        self._auto_update_model = ui.SimpleBoolModel(False)

        self._mode_context_menu = ui.Menu()

        # Apply the style to all the widgets of this window
        self.frame.style = get_style()

        # Set the function that is called to build widgets when the window is
        self.frame.set_build_fn(self._build_fn)

    def destroy(self):
        # if self._uplift_canvas:
        #    self._uplift_canvas.destroy()
        #    self._uplift_canvas = None

        if self._uplift_parameter_widget:
            self._uplift_parameter_widget.destroy()
            self._uplift_parameter_widget = None

        if self._uplift_model:
            # self._uplift_model.destroy()
            self._uplift_model = None

        if self._viewport_buffers_capture:
            self._viewport_buffers_capture = None

        # Remove any event subscriptions or callbacks
        if hasattr(self, "_auto_update_model"):
            self._auto_update_model = None

        super().destroy()

    def set_uplift_canvas(self, canvas):
        # The Model/API that generate the Uplift version of the Viewport
        self._uplift_canvas = canvas

    def set_uplift_model(self, uplift_model: AbstractUpliftModel):
        # The Model/API that generate the Uplift version of the Viewport
        self._uplift_model = uplift_model

        # Make sure we are using the right buffers
        self._setup_viewport_buffers()

    def _setup_viewport_buffers(self):
        """Set the viewport buffer with all the required buffer"""
        required_buffer = []
        required_capture_types = []
        params = self._uplift_model.get_parameters_spec()
        for param in params:
            if param["type"] == "image":
                buffer_name = param["buffer_name"]
                if buffer_name in self._viewport_buffers_capture.supported_buffer_types:
                    control_name = param["control_name"]
                    asset_path = param["asset_path"]
                    if "visibility" in param:
                        visibility = param["visibility"]
                    else:
                        visibility = "showall"
                    required_buffer.append(buffer_name)
                    required_capture_types.append([buffer_name, control_name, asset_path, visibility])
                else:
                    carb.log_error(f"'{buffer_name} is not supported")

        self._viewport_buffers_capture.set_active_buffer_types(required_buffer)
        self._viewport_buffers_capture.set_active_capture_types(required_capture_types)

    def _set_mode(self, mode: str):
        self._uplift_model.set_mode(mode)

        # Rebuild the connection
        self.set_uplift_model(self._uplift_model)
        self._uplift_parameter_widget.set_uplift_model(self._uplift_model)

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
            self._progress_bar = ui.ProgressBar(height=10, visible=False)
            # Uplift Canvas
            # self._uplift_canvas = UpliftCanvas()
            # Options
            self._uplift_parameter_widget = UpliftParameterWidget(
                self._uplift_model, self._auto_update_model, self._on_generate
            )

        stack.set_mouse_pressed_fn(self._show_mode_context_menu)

    def _on_generate(self):
        """This setup the Prompt with the current viewport and schedule an image update"""

        async def _generate_async():
            # self._progress_bar.visible = True
            progress_model = self._progress_bar.model
            progress_model.set_value(0)

            # Update the model with the current viewport buffers
            await self._viewport_buffers_capture.capture_viewport_async()

            # Then we update the model
            self._uplift_model.update_viewport_buffers(self._viewport_buffers_capture.get_viewport_buffers())

            progress_model.set_value(0.1)
            # The prompt is ready to schedule the inference update
            uplifted_image, size = await self._uplift_model.generate(progress_model)

            self._progress_bar.visible = False
            # update the viewport with the new image
            # self._uplift_canvas.update_image(uplifted_image, size)
            self._ext._output_window._uplift_canvas.update_image(uplifted_image, size)

            self._send_image(size[0], size[1], uplifted_image)

            # Check if auto-update is enabled and queue the next generation if it is
            if self._auto_update_model.as_bool:
                # Use asyncio.get_event_loop().call_soon to schedule the next generation
                # This allows the current execution to complete before starting the next one
                asyncio.get_event_loop().call_soon(self._on_generate)

        # Start the async task to generate the prompt
        asyncio.ensure_future(_generate_async())

    def _on_send(self):
        """Send test image to the web frontend"""
        # Get image path
        preview = "coffee_machine_0.png"
        image_path = f"{get_extension_path()}/data/{preview}"

        # Open and send the image
        with Image.open(image_path) as img:
            width, height = img.size
            img_data = img.tobytes()
            self._send_image(width, height, img_data)

    def _send_image(self, width, height, data, max_size=None, max_message_size=65535):
        # Register custom event type
        messaging.register_event_type_to_send("ImageTransferEvent")

        message_bus = omni.kit.app.get_app().get_message_bus_event_stream()
        event_type = carb.events.type_from_string("ImageTransferEvent")
        event_status = "success"

        print(
            f"Received image data: width={width}, height={height}, data type={type(data)}, data length={len(data) if isinstance(data, (list, bytes)) else 'N/A'}"
        )

        # Convert list of tuples to bytes if necessary
        if isinstance(data, list):
            data = b"".join(bytes(pixel) for pixel in data)
        elif not isinstance(data, bytes):
            raise ValueError("data must be either bytes or a list of RGB/RGBA tuples")

        # Determine if the image is RGB or RGBA
        channels = 3 if len(data) == width * height * 3 else 4
        mode = "RGB" if channels == 3 else "RGBA"

        # Create an image from the data
        try:
            img = Image.frombytes(mode, (width, height), data)
        except ValueError as e:
            print(f"Error creating image: {e}")
            print(f"Expected data length: {width * height * channels}, Actual data length: {len(data)}")
            return

        if not img.getbbox():
            event_status = "error"

        # Convert to RGBA if it's not already
        if img.mode != "RGBA":
            img = img.convert("RGBA")

        # Resize the image if max_size is set
        if max_size:
            # Calculate the scaling factor
            scale = min(max_size / width, max_size / height)
            if scale < 1:
                new_width = int(width * scale)
                new_height = int(height * scale)
                img = img.resize((new_width, new_height), Image.LANCZOS)
                print(f"Resized image to: {new_width}x{new_height}")

        # Convert the image to raw RGBA bytes
        img_bytes = img.tobytes()

        print(f"Sending image data: width={img.width}, height={img.height}, data length={len(img_bytes)}")

        # Estimate metadata size
        metadata_size = len(
            json.dumps(
                {
                    "event_type": "ImageTransferEvent",
                    "payload": {"width": img.width, "height": img.height, "part": 999, "total_parts": 999, "data": "", "status": event_status},
                },
                indent=2,
            )
        )

        # Calculate the maximum data size per chunk
        max_data_size = (max_message_size - metadata_size) // 2

        # Calculate the number of parts
        total_parts = -(-len(img_bytes) // max_data_size)  # Ceiling division

        for part in range(total_parts):
            start = part * max_data_size
            end = min((part + 1) * max_data_size, len(img_bytes))
            chunk = img_bytes[start:end]

            # Encode the chunk as a hex string
            encoded_chunk = chunk.hex()

            # Prepare the payload
            payload = {
                "width": img.width,
                "height": img.height,
                "part": part,
                "total_parts": total_parts,
                "data": encoded_chunk,
                "status": event_status,
            }

            # Dispatch the event
            message_bus.dispatch(event_type, payload=payload)

        print(f"Sent image in {total_parts} parts")
