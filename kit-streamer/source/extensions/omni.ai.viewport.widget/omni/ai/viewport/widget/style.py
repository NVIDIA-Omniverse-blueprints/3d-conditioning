# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

__all__ = ["get_extension_path", "get_style"]

import functools
import json
import pathlib

import carb.tokens
import omni.kit.app
import omni.ui as ui
from omni.ui import color as cl
from omni.ui import constant as fl
from omni.ui import url


@functools.lru_cache()
def get_extension_path():
    return pathlib.Path(omni.kit.app.get_app().get_extension_manager().get_extension_path_by_module(__name__))


@functools.lru_cache()
def get_style():
    # Read colors from JSON file
    json_path = get_extension_path() / "data" / "FigmaStyleTokens.json"
    with open(json_path, "r") as f:
        data = json.load(f)

    # Extract colors from the JSON data
    colors = data["themes"]["auto_extract"]["color"]["component"]
    for key, value in colors.items():
        color_name = "canva_" + value["name"].replace("-", "_")
        color_value = value["value"]
        setattr(cl, color_name, cl(color_value))

    # Extract font sizes from the JSON data
    FONT_MULTIPLIER = 0.7
    fonts = data["themes"]["auto_extract"]["font"]
    for key, value in fonts.items():
        font_name = "canva_" + key.replace("-", "_")
        font_size = value["value"]["size"]
        setattr(fl, font_name, int(font_size * FONT_MULTIPLIER))

    token = carb.tokens.get_tokens_interface()
    font_regular = token.resolve("${kit}/resources/fonts/NVIDIASans_Rg.ttf")

    # Pre-defined constants. It's possible to change them at runtime.
    cl.window_bg_color = cl.canva_background
    cl.window_title_text = cl(0.9, 0.9, 0.9, 0.9)
    cl.collapsible_header_text = cl(0.8, 0.8, 0.8, 0.8)
    cl.collapsible_header_text_hover = cl(0.95, 0.95, 0.95, 1.0)
    cl.main_attr_label_text = cl(0.65, 0.65, 0.65, 1.0)
    cl.main_attr_label_text_hover = cl(0.9, 0.9, 0.9, 1.0)
    cl.multifield_label_text = cl(0.65, 0.65, 0.65, 1.0)
    cl.combobox_label_text = cl(0.65, 0.65, 0.65, 1.0)
    cl.field_bg = cl(0.18, 0.18, 0.18, 1.0)
    cl.field_border = cl(1.0, 1.0, 1.0, 0.2)
    cl.btn_border = cl(1.0, 1.0, 1.0, 0.4)
    cl.slider_fill = cl(1.0, 1.0, 1.0, 0.3)
    cl.revert_arrow_enabled = cl(0.25, 0.5, 0.75, 1.0)
    cl.revert_arrow_disabled = cl(0.35, 0.35, 0.35, 1.0)
    cl.transparent = cl(0, 0, 0, 0)
    cl.field_background = cl(0.07, 0.07, 0.07)

    fl.main_label_attr_hspacing = 10
    fl.attr_label_v_spacing = 3
    fl.collapsable_group_spacing = 2
    fl.outer_frame_padding = 15
    fl.tail_icon_width = 15
    fl.border_radius = 10
    fl.border_width = 1
    fl.window_title_font_size = 18
    fl.field_text_font_size = 14
    fl.main_label_font_size = 14
    fl.multi_attr_label_font_size = 14
    fl.radio_group_font_size = 14
    fl.collapsable_header_font_size = 16
    fl.range_text_size = 10

    url.closed_arrow_icon = f"{get_extension_path()}/data/icons/closed.svg"
    url.open_arrow_icon = f"{get_extension_path()}/data/icons/opened.svg"
    url.revert_arrow_icon = f"{get_extension_path()}/data/icons/revert_arrow.svg"
    url.checkbox_on_icon = f"{get_extension_path()}/icons/checkbox_on.svg"
    url.checkbox_off_icon = f"{get_extension_path()}/icons/checkbox_off.svg"
    url.radio_btn_on_icon = f"{get_extension_path()}/icons/radio_btn_on.svg"
    url.radio_btn_off_icon = f"{get_extension_path()}/icons/radio_btn_off.svg"
    url.diag_bg_lines_texture = f"{get_extension_path()}/icons/diagonal_texture_screenshot.png"
    url.combobox_arrow = f"{get_extension_path()}/data/ComboBox.svg"

    url.nvidia_font_regular = f"{get_extension_path()}/data/fonts/NVIDIASans_Rg.ttf"
    url.nvidia_font_medium = f"{get_extension_path()}/data/fonts/NVIDIASans_Md.ttf"
    fl.ai_texture_font_size = 15
    fl.ai_texture_panel_title_font_size = 20

    cl.ai_texture_background = cl("#454545")
    cl.ai_texture_panel_background = cl("#333333")
    cl.ai_texture_button_background = cl("#292929")
    cl.ai_texture_dark = cl("#1F2124")
    cl.ai_texture_blue = cl("#1A91C5")
    cl.ai_texture_light_blue = cl("#76ADC5")
    cl.ai_texture_link = cl("#526FA0")
    cl.ai_texture_white = cl("#A8A8A8")

    fl.ai_texture_button_radius = 2

    # The main style dict
    style = {
        "Label": {
            "font": url.font_regular,
            "color": cl.red,
        },
        "Label::sceneTitle": {
            "font_size": fl.canva_body_p4,
            "color": cl.canva_sceneTitle_font,
        },
        "Label::label": {
            "font_size": fl.canva_body_p5,
            "color": cl.canva_sceneTitle_font,
            "margin": 3,
        },
        "ComboBox": {
            "border_radius": 15,
            "border_width": 1,
            "secondary_selected_color": cl.canva_heading_font,
            "secondary_background_color": cl.canva_background_pressed,
            "padding": 12,
            "margin": 3,
            # "border_color": cl.red,
        },
        "ComboBox.Label": {
            "font": url.font_regular,
            "font_size": fl.canva_body_p4,
            "color": cl.canva_heading_font,
            "margin": 12,
        },
        "ComboBox.Arrow": {
            "image_url": url.combobox_arrow,
            "color": cl.canva_heading_font,
            "margin": 12,
        },
        "Button::PandoraCatalogFormInput": {
            "background_color": cl.transparent,
        },
        "Button.Label::PandoraCatalogFormInput": {
            # "color": cl.btn_border,
            "color": cl.transparent,
        },
        "Button::PandoraCatalogFormInput:hovered": {
            "background_color": cl.transparent,
            "border_color": cl.transparent,
        },
        "Button.Label::PandoraCatalogFormInput:hovered": {
            "color": cl.canva_sceneTitle_font,
        },
        "Field::PandoraCatalogFormInput": {
            "background_color": cl.field_background,
            "font": url.font_regular,
            "font_size": fl.canva_body_p4,
            "color": cl.btn_border,
            "border_radius": 8,
            "border_width": 1,
            "border_color": cl.revert_arrow_disabled,
            "padding": 12,
            "margin": 3,
        },
        "Button::PandoraCatalogButton": {
            "background_color": cl.canva_border_selected,
            "border_radius": 18,
            "border_width": 0,
            "padding": 8,
        },
        "Button::PandoraCatalogButton:hovered": {
            "background_color": cl.canva_border_selected,
            "border_radius": 18,
        },
        "Button::PandoraCatalogButton:pressed": {
            "background_color": cl.ai_texture_link,
        },
        "Button.Label::PandoraCatalogButton": {
            "font": url.font_regular,
            "font_size": fl.canva_body_p3,
            "color": cl.field_background,
        },
        "Separator": {
            "margin": 5,
        },
        "Label::additional": {
            "font_size": fl.canva_body_p6,
            "color": cl.revert_arrow_disabled,
            "margin": 4,
        },
        "Circle::additional": {
            "border_color": cl.revert_arrow_disabled,
            "border_width": 1,
        },
        "Tooltip": {
            "background_color": cl.canva_background_pressed,
            "border_radius": 30,
            "border_width": 0,
            "padding": 10,
        },
        "Label::tooltipHeading": {
            "color": cl.canva_heading_font,
            "font_size": fl.canva_body_p4,
        },
        "Label::tooltipHint": {
            "color": cl.canva_sceneTitle_font,
            "font_size": fl.canva_body_p5,
        },
        "Label::tooltip": {
            "color": cl.canva_heading_font,
            "font_size": fl.canva_body_p6,
        },
        "Slider": {
            "background_color": cl.ai_texture_dark,
            "secondary_color": cl.ai_texture_background,
            "draw_mode": ui.SliderDrawMode.FILLED,
            "font": url.nvidia_font_medium,
            "font_size": fl.ai_texture_font_size,
            "color": cl.ai_texture_white,
        },
        "TabButton": {
            "background_color": cl.ai_texture_background,
        },
        "TabButton.Label": {
            "font": url.nvidia_font_regular,
            "font_size": fl.ai_texture_font_size,
            "color": cl.ai_texture_white,
        },
        "TabButton.Label:checked": {
            "color": cl.ai_texture_blue,
        },
        "TabButton.Label:hovered": {
            "color": cl.ai_texture_light_blue,
        },
        "TabSeparator": {
            "background_color": cl.ai_texture_background,
            "color": cl.ai_texture_white,
        },
        "Button": {
            "background_color": cl.ai_texture_button_background,
            "border_radius": fl.ai_texture_button_radius,
            "border_width": 1,
        },
        "Button:checked": {
            "background_color": cl.ai_texture_blue,
        },
        "Button.Label:checked": {
            "color": cl.black,
        },
        "Button:hovered": {
            # "background_color": cl.picasso_dark,
            "border_color": cl.ai_texture_light_blue,
        },
        "Button:pressed": {
            # "background_color": cl.picasso_dark,
            "border_color": cl.ai_texture_blue,
        },
        "CollapsableFrame": {
            "font": url.nvidia_font_regular,
            "font_size": fl.ai_texture_font_size,
            "background_color": cl.ai_texture_panel_background,
            "color": cl.ai_texture_white,
        },
        "Rectangle::panel": {
            "background_color": cl.ai_texture_panel_background,
        },
        "MemoryUsageWidget.Background": {
            "background_color": cl.ai_texture_button_background,
            "border_radius": fl.ai_texture_button_radius,
        },
        "MemoryUsageWidget.Used": {
            "background_color": cl.ai_texture_white,
            "border_radius": fl.ai_texture_button_radius,
        },
        "UpliftCanvas": {"background_color": cl.black},
        "Window": {
            "background_color": cl.canva_background,
            "padding": 30,
        },
        "ViewportImage": {"border_radius": 15},
        "ImageWithProvider::previewImage": {"border_radius": 15},
    }

    # Viewport window style
    import omni.kit.viewport.window

    omni.kit.viewport.window.ViewportWindow.set_default_style(style)

    return style
