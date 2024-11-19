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
import base64
import json
import os
import time
import uuid
from io import BytesIO
from typing import List, Tuple
from urllib import parse, request

import numpy as np
import aiohttp
import carb
import carb.settings
import websockets
from PIL import Image
from better_profanity import profanity

from ...abstract_uplift_model import AbstractUpliftModel

SERVER_ADDRESS = "/exts/omni.ai.viewport.core/comfy/server_address"

WORKFLOW_FOLDER = "/exts/omni.ai.viewport.core/comfy/workflows_folder"
DEFAULT_WORKFLOW = "/exts/omni.ai.viewport.core/comfy/default_workflow"

WEBSOCKET_MAX_SIZE = 10 * 1024 * 1024  # 10MB

from pathlib import Path

EXT_ROOT = Path(__file__).parent.parent.parent.parent.parent.parent.parent

import omni.ui as ui


class ComfyUplift(AbstractUpliftModel):
    def __init__(self):
        self.settings = carb.settings.get_settings()

        # Env var version
        if "COMFYUI_SERVER" in os.environ:
            self._comfy_url = os.environ.get("COMFYUI_SERVER")
        else:
            # You can use a Local or remote Server
            print("[Warning] Could not find env variable. Defaulting to use what we have on extension toml")
            self._comfy_url = self.settings.get(SERVER_ADDRESS)

        self._workflow_folder = self.settings.get(WORKFLOW_FOLDER)
        self._default_workflow = self.settings.get(DEFAULT_WORKFLOW)

        self.load_workflow(self._default_workflow)

        profanity.load_censor_words_from_file(f"{EXT_ROOT}/data/profanity_wordlist.txt")

        self._websocket_client_id = str(uuid.uuid4())
        self.busy = False

        super().__init__()

    def get_available_mode(self) -> List[str]:
        full_workflow_path = f"{EXT_ROOT}/{self._workflow_folder}"
        workflows = []
        list_files = os.listdir(full_workflow_path)
        for file in list_files:
            if ".json" in file:
                base_name = file.replace(".json", "")
                workflows.append(base_name)
        return workflows

    def set_mode(self, mode: str):
        self.load_workflow(mode)

    def load_workflow(self, name: str):
        full_workflow_path = f"{EXT_ROOT}/{self._workflow_folder}/{name}"
        # Read the workflow file (TODO check existance)
        comfy_path = f"{full_workflow_path}.json"
        if os.path.isfile(comfy_path):
            with open(comfy_path, "r") as f:
                self._comfy_json = json.load(f)
        else:
            raise ValueError(f"Failure to open ComfyUI Workflow API Format file: {comfy_path}")

        spec_path = f"{full_workflow_path}.spec"
        if os.path.isfile(spec_path):
            # Read the spec file
            with open(spec_path, "r") as f:
                self._comfy_parameters = json.load(f)
        else:
            # We are in auto mode the spec are in the workflow
            # This need to error clearly if the spec are not defined
            self._comfy_parameters = self._get_params_from_workflow()

        # We identify all the controls
        self._identifyControls()
        self.reset_parameters()

    def _get_params_from_workflow(self):
        """Get the parameters from the workflow file"""
        comfy_parameters = []
        for key, value in self._comfy_json.items():
            title = value["_meta"]["title"]
            if title.startswith("CAVA"):
                # Extract the input parameters from CAVA(<input>): name
                input = title.split("(")[1].split(")")[0]
                name = title.split(":")[1].strip()
                input_type = "float"
                if "image" in input:
                    input_type = "image"
                elif "text" in input:
                    input_type = "string"

                values = {
                    "name": name,
                    "control_name": title,
                    "input_name": input,
                    "type": input_type,
                    "default_value": value["inputs"][input],
                }

                if input_type == "image":
                    if "RGB" in name:
                        values["buffer_name"] = "LdrColor"
                    elif "Depth" in name:
                        values["buffer_name"] = "DepthLinearized"

                comfy_parameters.append(values)

        return comfy_parameters

    def _init_parameters(self):
        """Initialize the parameters"""
        params_spec = self.get_parameters_spec()
        for param in params_spec:
            self._parameters[param["name"]] = param["default_value"]

    def _identifyControls(self):
        """Based on the Parameter name in the Spec, this will add the control id in the json"""

        # We iterate all the json keys to find our Parameter Spec
        for key, value in self._comfy_json.items():
            title = value["_meta"]["title"]

            # Iterate the parameters and find the key
            for param in self._comfy_parameters:
                if title in param["control_name"]:
                    param["control_id"] = key

        # Validate we found all the controls
        for param in self._comfy_parameters:
            if "control_id" not in param:
                carb.log_warn("Control not found for %s" % param["control_name"])

    def get_parameters_spec(self) -> dict:
        return self._comfy_parameters

    def _generate_prompt(self, generation_params: dict) -> dict:
        """Generate the prompt for the comfy"""

        updated_prompt = self._comfy_json.copy()
        for key, value in generation_params.items():
            for param in self._comfy_parameters:
                if key == param["name"]:
                    if "control_id" not in param:
                        continue
                    control_id = param["control_id"]
                    input_name = param["input_name"]

                    if param["type"] == "image":
                        control_name = param["control_name"]
                        updated_prompt[control_id]["inputs"][input_name] = self._viewport_buffers[control_name]
                    else:
                        updated_prompt[control_id]["inputs"][input_name] = value
                    break

        return updated_prompt

    def _get_history(self, prompt_id, server_address):
        with request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
            return json.loads(response.read())

    def _get_image(self, filename, subfolder, folder_type, server_address):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = parse.urlencode(data)
        with request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
            return response.read()

    def _get_images(self, prompt_id, server_address, allow_preview=False, interval=1, timeout=600):
        output_images = []

        num_try = timeout // interval
        for try_id in range(num_try):
            try:
                history = self._get_history(prompt_id, server_address)[prompt_id]
                for node_id in history["outputs"]:
                    node_output = history["outputs"][node_id]
                    # output_data = {}
                    if "images" in node_output:
                        output_data = None
                        for image in node_output["images"]:
                            if "filename" not in image or "subfolder" not in image or "type" not in image:
                                continue

                            if allow_preview and image["type"] == "temp":
                                preview_data = self._get_image(
                                    image["filename"], image["subfolder"], image["type"], server_address
                                )
                                output_data = preview_data
                            if image["type"] == "output":
                                image_data = self._get_image(
                                    image["filename"], image["subfolder"], image["type"], server_address
                                )
                                output_data = image_data
                        if output_data is not None:
                            output_images.append(output_data)
            except Exception as e:
                if try_id == num_try - 1:
                    raise TimeoutError(f"TIMEOUT ({timeout}): {str(e)}")
                # logging.warning("waiting for result ...")
                time.sleep(interval)
                continue
            break

        if len(output_images) == 0:
            raise RuntimeError("No output images")

        return output_images

    def _is_safe(self, text):
        # Filter 1
        adjusted_text = text.replace("\"", " ").replace("'", " ").replace(",", " ").replace(".", " ")
        if profanity.contains_profanity(text) or profanity.contains_profanity(adjusted_text):
            return False

        # Filter 2
        # NOTE: Enter any custom NSFW filter here

        return True

    async def generate(self, progress_model: ui.SimpleFloatModel = None, **kwargs) -> Tuple[list, list]:
        if self.busy:
            carb.log_warn("Comfy is busy")
            return

        self.busy = True

        try:
            if progress_model:
                progress_model.set_value(0.2)
            generation_params = self._parameters.copy()
            generation_params.update(kwargs)
            generation_params.update(self._viewport_buffers)

            json_prompt = self._generate_prompt(generation_params)

            merged_prompts = ""
            for key in self._parameters.keys():
                merged_prompts += self._parameters[key] + "\n"

            print(merged_prompts)
            if len(merged_prompts) > 0:
                if not self._is_safe(merged_prompts):
                    print("Not safe")
                    imageSize = [1024, 1024]
                    data = np.zeros(imageSize)
                    rgba_image = Image.fromarray(data, mode="RGBA")
                    pixels = list(rgba_image.getdata())
                    return pixels, imageSize

            request_data = {
                "prompt": json_prompt,
                "client_id": self._websocket_client_id,
            }

            data = json.dumps(request_data).encode("utf-8")
            headers = {"Content-Type": "application/json"}
            req = request.Request("http://{}/prompt".format(self._comfy_url), data=data, headers=headers)
            prompt_id = json.loads(request.urlopen(req).read())["prompt_id"]

            if progress_model:
                progress_model.set_value(0.3)
            output_images = []

            output_images = self._get_images(prompt_id, self._comfy_url)
            if output_images:
                # print(f"Received {len(output_images)} images")

                image_base64 = base64.b64encode(output_images[0]).decode()
                image_file = BytesIO(base64.b64decode(image_base64))
                image = Image.open(image_file)

                # image = Image.open(BytesIO(output_images[0][8:]))
                imageSize = [image.width, image.height]
                rgba_image = image.convert("RGBA")
                pixels = list(rgba_image.getdata())
                return pixels, imageSize

        except Exception as e:
            carb.log_error(f"An error occurred during generation: {e}")
        finally:
            self.busy = False

    def destroy(self):
        pass
