# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

__all__ = ["ViewportBuffers"]

import base64
import ctypes
import io
import time
from typing import List, Tuple

import carb
import numpy as np
import omni.kit.viewport.utility as vp_util
import omni.ui as ui
from omni.kit.widget.viewport.capture import ByteCapture, MultiAOVByteCapture
from PIL import Image
from pxr import Sdf, Usd, UsdGeom, UsdRender
import omni.kit.app


class ViewportBuffersCapture:
    def __init__(self):
        self._viewport = vp_util.get_active_viewport()

        # Optionally resize the image to the target size , (0, 0) mean no resize
        self._target_size = [0, 0]
        # self._target_size = [1024, 1024]

        # Storage for the last captured viewport buffers
        self._viewport_buffers: dict = {}
        self._supported_buffer_types = ["LdrColor", "DepthLinearized", "SmoothNormal"]
        self.active_buffer_types = []
        self.active_capture_types = []

        self._send_image_fn = None

    @property
    def supported_buffer_types(self):
        return self._supported_buffer_types

    def _add_render_vars(self, stage, render_product_path, render_vars, add_to_session_layer: bool):
        rp_product = UsdRender.Product(stage.GetPrimAtPath(render_product_path))
        if not rp_product:
            carb.log_error(f"No UsdRender.Product was found at '{render_product_path}'")
            return False

        ordered_vars_rel = rp_product.GetOrderedVarsRel()
        ordered_vars = ordered_vars_rel.GetForwardedTargets()

        with Usd.EditContext(stage, stage.GetSessionLayer() if add_to_session_layer else stage.GetRootLayer()):
            for render_var in render_vars:
                render_var_path = Sdf.Path(f"/Render/Vars/{render_var}")

                if render_var_path in ordered_vars:
                    carb.log_warn(f"'{render_var_path} already existed, skipping")
                    continue

                data_type = "color3f"
                if "Depth" in render_var:
                    data_type = "float"
                # if "Normal" in render_var:
                #    data_type = "float3f"

                render_var_prim = UsdRender.Var.Define(stage, render_var_path)
                render_var_prim.GetSourceNameAttr().Set(render_var)
                render_var_prim.GetDataTypeAttr().Set(data_type)

                ordered_vars_rel.AddTarget(render_var_path)

    def get_viewport_buffers(self):
        return self._viewport_buffers

    def set_active_buffer_types(self, buffer_types: List[str]):
        self.active_buffer_types = buffer_types

    def set_active_capture_types(self, capture_types: List[Tuple[str, str, str, str]]):
        self.active_capture_types = capture_types

    def _on_viewport_captured(
        self, buffer, buffer_size, width, height, pixel_format, aov_name, control_name  # , capture_buffer_key, masking
    ):
        print(
            f"Callback invoked for AOV: {aov_name} @ {width} x {height} with format: {pixel_format}, buffer_size: {buffer_size}"
        )
        start_time = time.time()
        try:
            # Parsing pixel format to get the buffer and convert it to numpy array
            if pixel_format == pixel_format.RGBA8_UNORM:
                pod_type, pod_size, n_channels = ctypes.c_ubyte, 1, 4
                dtype = np.uint8
            elif pixel_format == pixel_format.R32_SFLOAT:
                pod_type, pod_size, n_channels = ctypes.c_float, 4, 1
                dtype = np.float32
            elif pixel_format == pixel_format.RGBA16_SFLOAT:
                pod_type, pod_size, n_channels = ctypes.c_ushort, 2, 4
                dtype = np.float16
            elif pixel_format == pixel_format.RGBA32_SFLOAT:
                pod_type, pod_size, n_channels = ctypes.c_float, 4, 4
                dtype = np.float32
            else:
                raise ValueError(f"Unsupported pixel format: {pixel_format}")

            array_len = width * height * n_channels
            assert array_len == (buffer_size / pod_size)

            ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.POINTER(pod_type)
            ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object, ctypes.c_char_p]

            content = ctypes.pythonapi.PyCapsule_GetPointer(buffer, None)

            np_array_time = time.time()
            np_array = np.ctypeslib.as_array(content, shape=(height, width, n_channels)).astype(dtype)
            print(f"Time to create numpy array: {time.time() - np_array_time:.4f} seconds")

            # Convert the depth (numpy) array to PIL image handling RGB or depth
            if pixel_format == pixel_format.RGBA8_UNORM:
                im = Image.fromarray(np_array, "RGBA")
            elif pixel_format == pixel_format.R32_SFLOAT:
                depth_array = np_array.squeeze()  # Remove single-dimensional entries

                # Define a threshold for "infinity" (adjust if needed)
                # Replace "infinity" values with NaN (to be clamped)
                inf_threshold = -3.402e38
                depth_array[depth_array <= inf_threshold] = np.nan
                inf_threshold = 3.402e38
                depth_array[depth_array >= inf_threshold] = np.nan

                # Debug information
                print(f"Depth array shape: {depth_array.shape}")
                print(f"Depth min: {np.nanmin(depth_array)}, max: {np.nanmax(depth_array)}")
                print(f"Number of nan values: {np.sum(np.isnan(depth_array))}")
                print(f"Number of negative values: {np.sum(depth_array < 0)}")
                print(f"Number of positive values: {np.sum(depth_array > 0)}")
                print(f"Number of finite values: {np.sum(np.isfinite(depth_array))}")

                # You can flip depth values here
                depth_array = -depth_array

                # Histogram of depth values for debugging
                hist, bin_edges = np.histogram(depth_array[np.isfinite(depth_array)], bins=10)
                print("Depth histogram:")
                for i, (count, edge) in enumerate(zip(hist, bin_edges[:-1])):
                    print(f"\tBin {i}: {edge:.2f} to {bin_edges[i+1]:.2f}: {count} values")

                depth_norm_time = time.time()
                valid_depths = depth_array[np.isfinite(depth_array) & (depth_array < 0)]
                if valid_depths.size > 0:
                    percentile_time = time.time()
                    depth_min = np.min(valid_depths)
                    depth_max = np.max(valid_depths)

                    print(f"Time to calculate percentiles: {time.time() - percentile_time:.4f} seconds")
                    print(f"Depth range: min = {depth_min}, max = {depth_max}")

                    normalize_time = time.time()
                    # Replace invalid values with max depth before normalization
                    depth_array_clean = np.where(np.isfinite(depth_array), depth_array, 0)
                    normalized_depth = np.clip((depth_array_clean - depth_min) / (depth_max - depth_min), 0, 1)

                    # This is good because its absolute - all depth will be aligned
                    depth_max = -200
                    depth_min = depth_max - 400
                    normalized_depth = np.clip((depth_array_clean - depth_min) / (depth_max - depth_min), 0, 1)

                    # This is good bc its easier for user to set it to a meaningful value, but depth will be relatively
                    # aligned
                    # depth_max = 1.0
                    # depth_min = 0.8
                    # normalized_depth = np.clip((normalized_depth - depth_min) / (depth_max - depth_min), 0, 1)
                    # Invert colors (1 - color)
                    final_depth = normalized_depth

                    print(f"Time to normalize, apply gamma, and invert: {time.time() - normalize_time:.4f} seconds")
                else:
                    final_depth = np.ones_like(depth_array)  # Set to white if no valid depths
                    print("Warning: No valid depth values found")

                print(f"Final depth min: {np.min(final_depth)}, max: {np.max(final_depth)}")

                im = Image.fromarray((final_depth * 255).astype(np.uint8), "L")
                print(f"Total time for depth processing: {time.time() - depth_norm_time:.4f} seconds")

                # Save debug image
                # debug_image_path = "debug_depth_image.png"
                # im.save(debug_image_path)
                # print(f"Debug depth image saved to: {debug_image_path}")
            elif pixel_format == pixel_format.RGBA16_SFLOAT:
                im = Image.fromarray((np_array * 255).astype(np.uint8), "RGBA")
            elif pixel_format == pixel_format.RGBA32_SFLOAT:
                im = Image.fromarray((((np_array * 0.5) + 0.5) * 255).astype(np.uint8), "RGBA")
            else:
                im = None

            if im:
                resize_time = time.time()
                aspect = im.width / im.height
                if self._target_size[0] > 0 and self._target_size[1] > 0:
                    sizex = int(self._target_size[0] * aspect)
                    sizey = int(self._target_size[1])
                    self._image_size = [sizex, sizey]
                    im_resized = im.resize((sizex, sizey))
                else:
                    im_resized = im
                print(f"Time to resize image: {time.time() - resize_time:.4f} seconds")

                encode_time = time.time()
                buffer = io.BytesIO()
                path = "buffer_" + control_name + ".png"
                # im_resized.save(path)
                # print(f"Debug image saved to: {path}")

                im_resized.save(buffer, format="PNG")
                imgString = base64.b64encode(buffer.getvalue()).decode()
                print(f"Time to encode image: {time.time() - encode_time:.4f} seconds")

                print(f"Captured {aov_name} buffer of size {len(imgString)} bytes")
                # self._viewport_buffers[aov_name] = imgString
                # self._viewport_buffers[capture_buffer_key] = imgString
                self._viewport_buffers[control_name] = imgString

                if self._send_image_fn:
                    self._send_image_fn(None, None, im, "BufferTransferEvent", control_name, max_size=256)

        except Exception as e:
            carb.log_error(f"Error in viewport capture: {str(e)}")
            import traceback

            print(traceback.format_exc())

        finally:
            print(f"Total time for _on_viewport_captured: {time.time() - start_time:.4f} seconds")

    # Capture the viewport and convert it to a scaled base64 encoded imagePrompt String
    async def capture_viewport_async(self):
        if not self._viewport:
            self._viewport = vp_util.get_active_viewport()
        # Make sure the render var are present
        self._add_render_vars(self._viewport.stage, self._viewport.render_product_path, self.active_buffer_types, True)

        FRAMES_TO_WAIT = 5
        i = 0
        for aov_name, control_name, asset_path, visibility in self.active_capture_types:
            frames_to_wait = 0
            if visibility == "hideme":
                prim = self._viewport.stage.GetPrimAtPath(asset_path)
                if prim.IsValid():
                    prim_visibility = prim.GetAttribute("visibility")
                    prim_visibility.Set("invisible")
                    # prim.SetActive(False)
                frames_to_wait = FRAMES_TO_WAIT
            elif visibility == "hideothers":
                prim = self._viewport.stage.GetPrimAtPath(asset_path)
                parent_prim = prim.GetParent()

                # Go through siblings
                if parent_prim.IsValid():
                    for sibling_prim in parent_prim.GetChildren():
                        if prim != sibling_prim:
                            prim_visibility = sibling_prim.GetAttribute("visibility")
                            prim_visibility.Set("invisible")
                            # sibling_prim.SetActive(False)
                frames_to_wait = FRAMES_TO_WAIT
            elif visibility == "walls_hideothers":
                prim = self._viewport.stage.GetPrimAtPath(asset_path)
                parent_prim = prim.GetParent()

                # Go through siblings
                if parent_prim.IsValid():
                    for sibling_prim in parent_prim.GetChildren():
                        if prim != sibling_prim:
                            prim_visibility = sibling_prim.GetAttribute("visibility")
                            prim_visibility.Set("invisible")
                            # sibling_prim.SetActive(False)

                prim = self._viewport.stage.GetPrimAtPath(asset_path + "/Kitchen/walls")
                parent_prim = prim.GetParent()

                # Go through siblings
                if parent_prim.IsValid():
                    for sibling_prim in parent_prim.GetChildren():
                        if prim != sibling_prim:
                            prim_visibility = sibling_prim.GetAttribute("visibility")
                            prim_visibility.Set("invisible")
                            # sibling_prim.SetActive(False)
                frames_to_wait = FRAMES_TO_WAIT
            elif visibility == "walls_hideme":
                prim = self._viewport.stage.GetPrimAtPath(asset_path)
                parent_prim = prim.GetParent()

                # Go through siblings
                if parent_prim.IsValid():
                    for sibling_prim in parent_prim.GetChildren():
                        if prim != sibling_prim:
                            prim_visibility = sibling_prim.GetAttribute("visibility")
                            prim_visibility.Set("invisible")
                            # sibling_prim.SetActive(False)

                prim = self._viewport.stage.GetPrimAtPath(asset_path + "/Kitchen/walls")
                parent_prim = prim.GetParent()

                # Go through siblings
                if parent_prim.IsValid():
                    for sibling_prim in parent_prim.GetChildren():
                        if sibling_prim.GetName() == "window1":
                            continue
                        if sibling_prim.GetName() == "countertops":
                            continue
                        if sibling_prim.GetName() == "cabinets":
                            continue
                        prim_visibility = sibling_prim.GetAttribute("visibility")
                        prim_visibility.Set("invisible")
                        # sibling_prim.SetActive(False)

                prim = self._viewport.stage.GetPrimAtPath(asset_path + "/Kitchen/window1/window")
                if prim.IsValid():
                    prim_visibility = prim.GetAttribute("visibility")
                    prim_visibility.Set("invisible")
                    #prim.SetActive(False)
                frames_to_wait = FRAMES_TO_WAIT

            if aov_name == "DepthLinearized":
                win_asset_path = "/World/Assets/KitchenBase/Kitchen/window1/window_pane"
                prim = self._viewport.stage.GetPrimAtPath(win_asset_path)
                if prim.IsValid():
                    prim_visibility = prim.GetAttribute("visibility")
                    prim_visibility.Set("invisible")
                    #prim.SetActive(False)
                frames_to_wait = FRAMES_TO_WAIT
            if frames_to_wait > 0:
                await vp_util.next_viewport_frame_async(self._viewport, n_frames=frames_to_wait)

            callback_fns = []
            callback_fns.append(
                lambda buffer, buffer_size, width, height, fmt, aov_name=aov_name, control_name=control_name: self._on_viewport_captured(
                    buffer, buffer_size, width, height, fmt, aov_name, control_name  # , asset_path, True
                )
            )
            capture = self._viewport.schedule_capture(MultiAOVByteCapture([aov_name], callback_fns))
            # await capture.wait_for_result(completion_frames=10)
            await capture.wait_for_result()

            frames_to_wait = 0
            if visibility == "hideme":
                prim = self._viewport.stage.GetPrimAtPath(asset_path)
                if prim.IsValid():
                    prim_visibility = prim.GetAttribute("visibility")
                    prim_visibility.Set("inherited")
                    # prim.ClearActive()
                frames_to_wait = FRAMES_TO_WAIT
            elif visibility == "hideothers":
                prim = self._viewport.stage.GetPrimAtPath(asset_path)
                parent_prim = prim.GetParent()

                # Go through siblings
                if parent_prim.IsValid():
                    for sibling_prim in parent_prim.GetChildren():
                        if prim != sibling_prim:
                            prim_visibility = sibling_prim.GetAttribute("visibility")
                            prim_visibility.Set("inherited")
                            # sibling_prim.ClearActive()
                frames_to_wait = FRAMES_TO_WAIT
            elif visibility == "walls_hideothers":
                prim = self._viewport.stage.GetPrimAtPath(asset_path)
                parent_prim = prim.GetParent()

                # Go through siblings
                if parent_prim.IsValid():
                    for sibling_prim in parent_prim.GetChildren():
                        prim_visibility = sibling_prim.GetAttribute("visibility")
                        prim_visibility.Set("inherited")
                        # sibling_prim.ClearActive()

                prim = self._viewport.stage.GetPrimAtPath(asset_path + "/Kitchen/walls")
                parent_prim = prim.GetParent()

                # Go through siblings
                if parent_prim.IsValid():
                    for sibling_prim in parent_prim.GetChildren():
                        prim_visibility = sibling_prim.GetAttribute("visibility")
                        prim_visibility.Set("inherited")
                        # sibling_prim.ClearActive()
                frames_to_wait = FRAMES_TO_WAIT
            elif visibility == "walls_hideme":
                prim = self._viewport.stage.GetPrimAtPath(asset_path)
                parent_prim = prim.GetParent()

                # Go through siblings
                if parent_prim.IsValid():
                    for sibling_prim in parent_prim.GetChildren():
                        prim_visibility = sibling_prim.GetAttribute("visibility")
                        prim_visibility.Set("inherited")
                        # sibling_prim.ClearActive()

                prim = self._viewport.stage.GetPrimAtPath(asset_path + "/Kitchen/walls")
                parent_prim = prim.GetParent()

                # Go through siblings
                if parent_prim.IsValid():
                    for sibling_prim in parent_prim.GetChildren():
                        if sibling_prim.GetName() == "window1":
                            continue
                        if sibling_prim.GetName() == "countertops":
                            continue
                        if sibling_prim.GetName() == "cabinets":
                            continue
                        prim_visibility = sibling_prim.GetAttribute("visibility")
                        prim_visibility.Set("inherited")
                        # sibling_prim.ClearActive()

                prim = self._viewport.stage.GetPrimAtPath(asset_path + "/Kitchen/window1/window")
                if prim.IsValid():
                    prim_visibility = prim.GetAttribute("visibility")
                    prim_visibility.Set("inherited")
                    # prim.ClearActive()
                frames_to_wait = FRAMES_TO_WAIT

            if aov_name == "DepthLinearized":
                win_asset_path = "/World/Assets/KitchenBase/Kitchen/window1/window_pane"
                prim = self._viewport.stage.GetPrimAtPath(win_asset_path)
                if prim.IsValid():
                    prim_visibility = prim.GetAttribute("visibility")
                    prim_visibility.Set("inherited")
                    # prim.ClearActive()
                frames_to_wait = FRAMES_TO_WAIT
            if frames_to_wait > 0:
                await vp_util.next_viewport_frame_async(self._viewport, n_frames=frames_to_wait)
            i += 1

        prim_lakeview = self._viewport.stage.GetPrimAtPath("/World/Cameras/ProjectionTemplate_LakeView")
        prim_lakeview_visibility = prim_lakeview.GetAttribute("visibility")
        prim_lakeview_visibility_value = prim_lakeview_visibility.Get()
        prim_lookout = self._viewport.stage.GetPrimAtPath("/World/Cameras/ProjectionTemplate_lookout")
        prim_lookout_visibility = prim_lookout.GetAttribute("visibility")
        prim_lookout_visibility_value = prim_lookout_visibility.Get()
        if prim_lakeview_visibility_value == "inherited" and prim_lookout_visibility_value == "inherited":
            new_payload = {"variant": "Lake_view"}
            _sender_id = carb.events.acquire_events_interface().acquire_unique_sender_id()
            new_event_type = carb.events.type_from_string("setBackdropVariant")
            bus = omni.kit.app.get_app().get_message_bus_event_stream()
            bus.push(new_event_type, sender=_sender_id, payload=new_payload)
            app = omni.kit.app.get_app()
            for _ in range(5):
                await app.next_update_async()

            new_payload = {"variant": "Lookout"}
            _sender_id = carb.events.acquire_events_interface().acquire_unique_sender_id()
            new_event_type = carb.events.type_from_string("setBackdropVariant")
            bus = omni.kit.app.get_app().get_message_bus_event_stream()
            bus.push(new_event_type, sender=_sender_id, payload=new_payload)
            app = omni.kit.app.get_app()
            for _ in range(5):
                await app.next_update_async()

        return



"""
Rt:
/// Temporally upscaled and accumulated into high res combined depth.
StableDepth
/// Smooth, unbumped normal.
SmoothNormal
/// Bump mapped normal.
BumpNormal
/// Ambient Occlusion.
AmbientOcclusion
/// Motion vectors in 2d screen space.
Motion2d
/// Diffuse albedo.
DiffuseAlbedo
/// Specular albedo.
SpecularAlbedo
/// Material roughness.
Roughness
/// Direct diffuse lighting.
DirectDiffuse
/// Direct specular lighting.
DirectSpecular
/// Specular reflections.
Reflections
/// Indirect diffuse lighting, a.k.a diffuse global illumination.
IndirectDiffuse
/// Depth but linearized and non-inverted, i.e. larger values means further away.
DepthLinearized
/// Emission in rgb channels. .w is a foreground mask, 0 for background.
EmissionAndForegroundMask
/// Emission in rgb channels. .w is a foreground mask, 0 for background.
StableId
"""

"""
Pt:
PtDirectIllumation
PtGlobalIllumination
PtReflections
PtRefractions
PtSelfIllumination
PtBackground
PtWorldNormal
PtWorldPos
PtViewNormal
PtZDepth
PtVolumes
PtDiffuseFilter
PtReflectionFilter
PtRefractionFilter
PtSubsurfaceFilter
PtMotion
"""
