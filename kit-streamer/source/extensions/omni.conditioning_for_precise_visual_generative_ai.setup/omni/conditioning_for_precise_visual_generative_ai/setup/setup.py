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
import functools
import pathlib
from pathlib import Path
import json

import carb
import carb.settings
import carb.tokens
import omni.ext
import omni.kit.app
import omni.kit.imgui as _imgui
import omni.kit.viewport
import omni.usd
import carb.events
from omni.ai.viewport.core import AIViewportCoreExtension
from omni.kit.mainwindow import get_main_window
from omni.kit.quicklayout import QuickLayout
from omni.kit.viewport.utility import get_viewport_from_window_name
from PIL import Image
from typing import Dict, List
import omni.kit.livestream.messaging as messaging
from .viewport_suppress import ViewportSuppress
import csv
import os
import numpy as np

COMMAND_MACRO_SETTING = "/exts/omni.kit.command_macro.core/"
COMMAND_MACRO_FILE_SETTING = COMMAND_MACRO_SETTING + "macro_file"

# Maximum message size in bytes
MAX_MESSAGE_SIZE = 32768

# Global variable to store the SetupExtension instance
setup_extension_instance = None


@functools.lru_cache()
def get_extension_path():
    return pathlib.Path(omni.kit.app.get_app().get_extension_manager().get_extension_path_by_module(__name__))


async def _load_layout(layout_file: str):
    """Loads a provided layout file and ensures the viewport is set to FILL."""
    await omni.kit.app.get_app().next_update_async()
    QuickLayout.load_file(layout_file)

    # Set the viewport resolution
    settings = carb.settings.get_settings()
    width = settings.get("/app/renderer/resolution/width")
    height = settings.get("/app/renderer/resolution/height")
    if width and height:
        settings.set("/persistent/app/viewport/Viewport/Viewport0/resolution", [width, height])

    fill_viewport = settings.get("/app/viewport/defaults/fillViewport")
    if fill_viewport is not None:
        settings.set("/persistent/app/viewport/Viewport/Viewport0/fillViewport", fill_viewport)


class SetupExtension(omni.ext.IExt):
    """Extension that sets up the USD Viewer application."""

    def on_startup(self, _ext_id: str):
        """This is called every time the extension is activated. It is used to
        set up the application and load the stage."""
        global setup_extension_instance
        setup_extension_instance = self

        import carb.settings

        self._settings = carb.settings.get_settings()

        # get auto load stage name
        # stage_url = self._settings.get_as_string("/app/auto_load_usd")
        stage_url = "${omni.conditioning_for_precise_visual_generative_ai.setup}/data/Collected_EspressoMachine_Asset/product_configurator_base.usd"
        import carb.tokens

        stage_url = carb.tokens.get_tokens_interface().resolve(stage_url)
        # check if setup have benchmark macro file to activate - ignore setup
        # auto_load_usd name, in order to run proper benchmark.

        benchmark_macro_file_name = self._settings.get(COMMAND_MACRO_FILE_SETTING)
        if benchmark_macro_file_name:
            stage_url = None

        # if no benchmark is activated (not applicable on production -
        # provided macro file name will always be None) -
        # load provided by setup stage.
        if stage_url:
            stage_url = carb.tokens.get_tokens_interface().resolve(stage_url)
            asyncio.ensure_future(self.__open_stage(stage_url))

        self._await_layout = asyncio.ensure_future(self._delayed_layout())
        get_main_window().get_main_menu_bar().visible = False

        viewport_core_instance = AIViewportCoreExtension.get_instance()
        self._viewport_buffers_capture = viewport_core_instance._viewport_buffers_capture
        self._uplift_model = viewport_core_instance._uplift_model
        self._setup_viewport_buffers()

        new_event_type = carb.events.type_from_string("queryComfyUI")
        bus = omni.kit.app.get_app().get_message_bus_event_stream()
        self._event = bus.create_subscription_to_pop_by_type(new_event_type, self._on_generate)

        #self._on_generate(None)

    async def _delayed_layout(self):
        """This function is used to delay the layout loading until the
        application has finished its initial setup."""
        main_menu_bar = get_main_window().get_main_menu_bar()
        main_menu_bar.visible = False
        # few frame delay to allow automatic Layout of window that want their
        # own positions
        app = omni.kit.app.get_app()
        for _ in range(4):
            await app.next_update_async()  # type: ignore

        settings = carb.settings.get_settings()
        # setup the Layout for your app
        token = "${omni.conditioning_for_precise_visual_generative_ai.setup}/layouts"

        layouts_path = carb.tokens.get_tokens_interface().resolve(token)
        layout_name = settings.get("/app/layout/name")
        layout_file = Path(layouts_path).joinpath(f"{layout_name}.json")

        asyncio.ensure_future(_load_layout(f"{layout_file}"))

        # using imgui directly to adjust some color and Variable
        imgui = _imgui.acquire_imgui()

        # DockSplitterSize is the variable that drive the size of the
        # Dock Split connection
        imgui.push_style_var_float(_imgui.StyleVar.DockSplitterSize, 2)

    async def __open_stage(self, url, frame_delay: int = 5):
        """Opens the provided USD stage and loads the render settings."""
        # default 5 frame delay to allow for Layout
        if frame_delay:
            app = omni.kit.app.get_app()
            for _ in range(frame_delay):
                await app.next_update_async()

        usd_context = omni.usd.get_context()
        await usd_context.open_stage_async(url, omni.usd.UsdContextInitialLoadSet.LOAD_ALL)

        # If this was the first Usd data opened, explicitly restore
        # render-settings now as the renderer may not have been fully
        # setup when the stage was opened.
        if not bool(self._settings.get("/app/content/emptyStageOnStart")):
            usd_context.load_render_settings_from_stage(usd_context.get_stage_id())

        # Set variant to enable caching
        new_payload = {"variant": "Display1"}
        _sender_id = carb.events.acquire_events_interface().acquire_unique_sender_id()
        new_event_type = carb.events.type_from_string("setDisplayVariant")
        bus = omni.kit.app.get_app().get_message_bus_event_stream()
        bus.push(new_event_type, sender=_sender_id, payload=new_payload)

        app = omni.kit.app.get_app()
        for _ in range(5):
            await app.next_update_async()

        new_payload = {"variant": "Display2"}
        _sender_id = carb.events.acquire_events_interface().acquire_unique_sender_id()
        new_event_type = carb.events.type_from_string("setDisplayVariant")
        bus = omni.kit.app.get_app().get_message_bus_event_stream()
        bus.push(new_event_type, sender=_sender_id, payload=new_payload)

        app = omni.kit.app.get_app()
        for _ in range(5):
            await app.next_update_async()


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
        self._viewport_buffers_capture._send_image_fn = self._send_image


    def _on_generate(self, event: carb.events.IEvent):
        """This setup the Prompt with the current viewport and schedule an image update"""
        prompt_names = ["globalPrompt", "teaCupPrompt", "vasePrompt", "counterPrompt", "cabinetsPrompt"]

        if event is None:
            carb.log_error(f"Unexpected message payload")
            return

        for prompt_name in prompt_names:
            if prompt_name not in event.payload:
                carb.log_error(f"Unexpected message payload: missing key '{prompt_name}'. Payload: '{event.payload}'")
                return

        # Update spec
        for prompt_name in prompt_names:
            prompt_data = event.payload[prompt_name]
            if prompt_data and prompt_data != "":
                self._uplift_model.set_parameters(prompt_name, "string", prompt_data)

        async def _generate_async():
            suppress = ViewportSuppress()
            await suppress.begin()

            # Update the model with the current viewport buffers
            await self._viewport_buffers_capture.capture_viewport_async()

            # Then we update the model
            self._uplift_model.update_viewport_buffers(self._viewport_buffers_capture.get_viewport_buffers())

            await suppress.end()
            suppress = None

            # The prompt is ready to schedule the inference update
            uplifted_image, size = await self._uplift_model.generate()

            # update the viewport with the new image
            # self._uplift_canvas.update_image(uplifted_image, size)
            # self._ext._output_window._uplift_canvas.update_image(uplifted_image, size)

            self._send_image(size[0], size[1], uplifted_image)

        # Start the async task to generate the prompt
        asyncio.ensure_future(_generate_async())

    def _on_generate_batch(self, parameters: List[Dict[str, str]]):
        """
        Generate a batch of images based on the provided parameters.

        This function processes a list of parameter dictionaries, each representing
        a single image generation task. It handles setting variants, updating the model,
        generating the image, and saving it to disk.

        Args:
            parameters (List[Dict[str, str]]): A list of dictionaries, where each dictionary
                contains parameters for a single image generation task.

        Each parameter dictionary may include the following keys:
        - Variant keys: "setDisplayVariant", "setCupVariant", "setColorVariant", "setBackdropVariant"
        - Prompt keys: "globalPrompt", "teaCupPrompt", "vasePrompt", "counterPrompt", "cabinetsPrompt"
        - Output key: "_output" (specifies the output filename)

        Variant options:
        - setDisplayVariant: "Display1", "Display2"
        - setCupVariant: "Glass_Mug", "Espresso_Cup", "Coffee_Mug"
        - setColorVariant: "Black", "Blue", "Cream", "Olive"
        - setBackdropVariant: "Lake_view", "Lookout", "None"

        Example:
            parameters = [
                {
                    "setDisplayVariant": "Display1",
                    "setCupVariant": "Glass_Mug",
                    "setColorVariant": "Black",
                    "setBackdropVariant": "Lake_view",
                    "globalPrompt": "A sleek coffee machine",
                    "_output": "output_1.png"
                },
                # ... more parameter dictionaries
            ]
            self._on_generate_batch(parameters)
        """
        async def _set_variant(variant_name: str, variant_value: str):
            """Set a specific variant in the scene."""
            new_payload = {"variant": variant_value}
            _sender_id = carb.events.acquire_events_interface().acquire_unique_sender_id()
            new_event_type = carb.events.type_from_string(variant_name)
            bus = omni.kit.app.get_app().get_message_bus_event_stream()
            bus.push(new_event_type, sender=_sender_id, payload=new_payload)

        async def _generate_single_async(params: Dict[str, str]):
            """Generate a single image based on the provided parameters and save associated JSON."""
            # Save JSON file with original, unchanged input parameters
            output_filename = params["_output"]
            json_filename = os.path.splitext(output_filename)[0] + ".json"
            with open(json_filename, 'w') as json_file:
                json.dump(params, json_file, indent=2)
            carb.log_info(f"Saved input parameters to: {json_filename}")

            # Set variants
            variant_keys = ["setDisplayVariant", "setCupVariant", "setColorVariant", "setBackdropVariant"]
            for key in variant_keys:
                if key in params:
                    await _set_variant(key, params[key])

            # Extract output filename and remove it from params
            output_filename = params.pop("_output", "output.png")

            # Update prompt parameters
            prompt_keys = ["globalPrompt", "teaCupPrompt", "vasePrompt", "counterPrompt", "cabinetsPrompt"]
            for key in prompt_keys:
                if key in params:
                    self._uplift_model.set_parameters(key, "string", params[key])

            # Capture viewport and update model
            await self._viewport_buffers_capture.capture_viewport_async()
            self._uplift_model.update_viewport_buffers(self._viewport_buffers_capture.get_viewport_buffers())

            # Generate image
            uplifted_image, size = await self._uplift_model.generate()

            # Convert image data to bytes if it's a list
            if isinstance(uplifted_image, list):
                uplifted_image = np.array(uplifted_image, dtype=np.uint8).tobytes()

            # Save image to disk
            img = Image.frombytes("RGBA", size, uplifted_image)
            img.save(output_filename, "PNG")
            carb.log_info(f"Saved generated image to: {output_filename}")

        async def _generate_batch_async(params_list: List[Dict[str, str]]):
            """Process the entire batch of image generation tasks."""
            for i, params in enumerate(params_list):
                try:
                    carb.log_info(f"Generating image {i+1}/{len(params_list)}")
                    await _generate_single_async(params)
                except Exception as e:
                    carb.log_error(f"Error generating batch item {i}: {e}")

        # Start the async task to generate the batch
        asyncio.ensure_future(_generate_batch_async(parameters))

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

    @staticmethod
    def _send_image(
        width, height, data, event_type="ImageTransferEvent", event_name=None, max_size=None, max_message_size=65535
    ):
        """
        Send an image to the web frontend by splitting it into chunks and dispatching events.

        Args:
            width (int): The width of the image.
            height (int): The height of the image.
            data (bytes, list, or PIL.Image.Image): The image data. Can be raw bytes, a list of RGB/RGBA tuples, or a PIL Image object.
            event_type (str, optional): The type of event to dispatch. Defaults to "ImageTransferEvent".
            event_name (str, optional): An optional name for the event. Defaults to None.
            max_size (int, optional): Maximum size (in pixels) for the image's width or height. If specified, the image will be resized while maintaining aspect ratio. Defaults to None.
            max_message_size (int, optional): Maximum size (in bytes) for each message chunk. Defaults to 65535.

        Raises:
            ValueError: If the data format is invalid or cannot be processed.

        Note:
            This method splits the image data into chunks and sends them as separate events to accommodate message size limitations.
            The image is converted to RGBA format before sending.
        """
        # Register custom event type
        messaging.register_event_type_to_send(event_type)

        message_bus = omni.kit.app.get_app().get_message_bus_event_stream()
        event_type = carb.events.type_from_string(event_type)
        event_status = "success"

        # Check if data is a PIL Image
        if isinstance(data, Image.Image):
            img = data
            width, height = img.size
        else:

            # Convert list of tuples to bytes if necessary
            if isinstance(data, list):
                data = b"".join(bytes(pixel) for pixel in data)
            elif not isinstance(data, bytes):
                raise ValueError("data must be either bytes, a list of RGB/RGBA tuples, or a PIL Image")

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

        print(
            f"[Send Image] Received image data: width={width}, height={height}, "
            f"data type={type(data)}, "
            f"data length={len(data) if isinstance(data, (list, bytes)) else 'N/A'} "
            f"type={event_type} "
            f"name={event_name} "
            f"event_status={event_status}"
        )

        # Convert to RGBA if it's not already
        if img.mode != "RGBA":
            img = img.convert("RGBA")

        # Resize the image if max_size is set
        if max_size:
            # Calculate the scaling factor
            scale = min(max_size / img.width, max_size / img.height)
            if scale < 1:
                new_width = int(img.width * scale)
                new_height = int(img.height * scale)
                img = img.resize((new_width, new_height), Image.LANCZOS)
                print(f"[Send Image] Resized image to: {new_width}x{new_height}")

        # Convert the image to raw RGBA bytes
        img_bytes = img.tobytes()

        print(f"[Send Image] Sending image data: width={img.width}, height={img.height}, data length={len(img_bytes)}")

        # Estimate metadata size
        metadata_size = len(
            json.dumps(
                {
                    "event_type": event_type,
                    "payload": {
                        "width": img.width,
                        "height": img.height,
                        "part": 999,
                        "total_parts": 999,
                        "data": "",
                        "name": event_name,
                        "status": event_status,
                    },
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
                "status": event_status,
            }

            if event_name:
                payload["name"] = event_name

            payload["data"] = encoded_chunk

            # Dispatch the event
            message_bus.dispatch(event_type, payload=payload)

        print(f"[Send Image] Sent image in {total_parts} parts")

    def on_shutdown(self):
        """This is called every time the extension is deactivated."""
        global setup_extension_instance
        setup_extension_instance = None

    def _generate_csv(self, csv_file_path: str):
        """
        Generate batch images based on parameters specified in a CSV file.

        This function reads a CSV file containing image generation parameters,
        processes each row, and generates images accordingly. The output images
        are saved in the same folder as the input CSV file.

        Args:
            csv_file_path (str): Path to the CSV file containing image generation parameters.

        The CSV file should have the following columns:
        - Display Type: "Touch Screen" or "Analog"
        - Machine Color: "Blue", "Black", "Cream", or "Olive"
        - Mug Type: "Glass Mug", "Espresso Cup", or "Coffee Mug"
        - HDRI: "Lighting 1" or "Lighting 2"
        - Global: Global prompt for the image
        - Plate: Prompt for the plate/cup area
        - Vase: Prompt for the vase area
        - Cutting Board: Prompt for the cutting board area
        - Kitchen: Prompt for the kitchen/cabinets area
        - File: Output file path (not used, included for compatibility)

        The function will process each row and generate an image using the specified parameters.
        """
        parameters = []
        output_folder = os.path.dirname(csv_file_path)

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for i, row in enumerate(reader):
                    row_id = i + 2  # Add 2 to account for the header row and 0-based index
                    output_filename = f"output_{row_id:03d}.png"
                    output_path = os.path.join(output_folder, output_filename)

                    param = {
                        "setDisplayVariant": "Display1" if row["Display Type"] == "Touch Screen" else "Display2",
                        "setColorVariant": row["Machine Color"],
                        "setCupVariant": "Glass_Mug" if row["Mug Type"] == "Glass Mug" else
                                         "Espresso_Cup" if row["Mug Type"] == "Espresso Cup" else
                                         "Coffee_Mug",
                        "setBackdropVariant": "Lake_view" if row["HDRI"] == "Lighting 1" else "Lookout",
                        "globalPrompt": row["Global"],
                        "teaCupPrompt": row["Plate"],
                        "vasePrompt": row["Jar"],
                        "counterPrompt": row["Cutting Board"],
                        "cabinetsPrompt": row["Kitchen"],
                        "_output": output_path
                    }
                    parameters.append(param)

            carb.log_info(f"Loaded {len(parameters)} image generation tasks from CSV.")
            carb.log_info(f"Output images will be saved in: {output_folder}")
            self._on_generate_batch(parameters)

        except FileNotFoundError:
            carb.log_error(f"CSV file not found: {csv_file_path}")
        except csv.Error as e:
            carb.log_error(f"Error reading CSV file: {e}")
        except Exception as e:
            carb.log_error(f"Unexpected error processing CSV: {e}")


# Global functions to call SetupExtension methods
def generate_batch(parameters: List[Dict[str, str]]):
    """
    Generate a batch of images based on the provided parameters.

    Args:
        parameters (List[Dict[str, str]]): A list of dictionaries, where each dictionary
            contains parameters for a single image generation task.
    """
    if setup_extension_instance:
        setup_extension_instance._on_generate_batch(parameters)
    else:
        carb.log_error("SetupExtension instance not initialized.")

def generate_csv(csv_file_path: str):
    """
    Generate batch images based on parameters specified in a CSV file.

    Args:
        csv_file_path (str): Path to the CSV file containing image generation parameters.
    """
    if setup_extension_instance:
        setup_extension_instance._generate_csv(csv_file_path)
    else:
        carb.log_error("SetupExtension instance not initialized.")
