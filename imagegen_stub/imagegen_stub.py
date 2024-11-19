# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

from typing import (
    Any,
)
import io
import os
import time
import json
import base64
import string
import hashlib
import logging
import uvicorn
import datetime

from pydantic import BaseModel
from fastapi import FastAPI, status, Response, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

IMAGES_FOLDER = "received_images"
IMAGE_STUB_PATH = "stub_picture.png"
image_stub = None

IMAGE_TEXT_OVERLAY = True
def save_image_with_text(image_binary, image_name: str):
    from PIL import (
        Image,
        ImageDraw,
    )
    image = Image.open(io.BytesIO(image_binary))
    image_draw = ImageDraw.Draw(image)
    for i in range(10):
        image_draw.text((  0 - 15*i, 30 + 100*i), "SAMPLE  IMAGE   |   "*20, fill=(255, 0, 255))
    image.save(image_name)

def save_image(image_binary, image_name: str):
    with open(image_name, 'wb') as fp:
        fp.write(image_binary)


ALLOWED_CHARACTERS = set(string.ascii_lowercase + string.digits + '_')
def is_valid_id(id: str):
    return set(id).issubset(ALLOWED_CHARACTERS)

def cleanup_old_files(path: str, age_seconds: int = 86400):
    if not os.path.isdir(path):
        return

    current_time = time.time()
    for entry in os.listdir(path):
        filepath = os.path.join(path, entry)
        if os.stat(filepath).st_mtime < current_time - age_seconds:
            if os.path.isfile(filepath):
                os.remove(filepath)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.error(f"{request}: {exc_str}")
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

class HealthCheck(BaseModel):
    status: str = "OK"

@app.get("/health", tags=["healthcheck"], summary="Perform a Health Check", response_description="Return HTTP Status Code 200 (OK)", status_code=status.HTTP_200_OK, response_model=HealthCheck)
def get_health() -> HealthCheck:
    return HealthCheck(status="OK")

@app.get("/history/{prompt_id}", summary="Perform a history lookup for a given prompt ID")
def get_history(prompt_id: str):
    history_dict = {
        prompt_id: {
            "outputs": {
                "001": {
                    'images': [
                        {'filename': prompt_id, 'subfolder': '', 'type': 'output'},
                    ]
                },
            },
        },
    }
    return history_dict

@app.get(
    "/view",
    summary="View image",
    responses = {
        200: {
            "content": {"image/png": {}}
        }
    },
)
def get_image(filename: str, subfolder: str, type: str) -> Response:
    cleanup_old_files(IMAGES_FOLDER)

    global image_stub
    if not image_stub:
        with open(IMAGE_STUB_PATH, mode="rb") as fp:
            image_stub = fp.read()

    response_image = image_stub

    if is_valid_id(filename):
        image_name = os.path.join(IMAGES_FOLDER, f"{filename}.png")
        if os.path.isfile(image_name):
            with open(image_name, mode="rb") as fp:
                response_image = fp.read()

    return Response(content=response_image, media_type="image/png")


class PromptData(BaseModel):
    prompt: Any
    client_id: str

@app.post("/prompt")
async def prompt(prompt_data: PromptData):
    cleanup_old_files(IMAGES_FOLDER)

    current_timestamp = datetime.datetime.now()
    formatted_timestamp = current_timestamp.strftime('%Y%m%d_%H%M%S')

    prompt_str = json.dumps(prompt_data.prompt)[:64]
    hash_result = hashlib.md5(prompt_str.encode())
    prompt_id = f"{formatted_timestamp}_{hash_result.hexdigest()[:16]}"

    os.makedirs(IMAGES_FOLDER, exist_ok=True)
    for node_name, node_data in prompt_data.prompt.items():
        image_present = ("inputs" in node_data) and ("image" in node_data["inputs"])
        binary_class_type = ("class_type" in node_data) and (node_data["class_type"] == "ETN_LoadImageBase64")
        if image_present and binary_class_type:
            image_name = node_name
            if "_meta" in node_data and "title" in node_data["_meta"] and node_data["_meta"]["title"] == "ImageInput":
                image_name = os.path.join(IMAGES_FOLDER, f"{prompt_id}.png")
                print(f"Writing '{image_name}'..", flush=True)
                image_data = node_data["inputs"]["image"]
                image_file = base64.b64decode(image_data)
                if IMAGE_TEXT_OVERLAY:
                    save_image_with_text(image_binary=image_file, image_name=image_name)
                else:
                    save_image(image_binary=image_file, image_name=image_name)


    response = {
        "prompt_id": prompt_id,
    }
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
