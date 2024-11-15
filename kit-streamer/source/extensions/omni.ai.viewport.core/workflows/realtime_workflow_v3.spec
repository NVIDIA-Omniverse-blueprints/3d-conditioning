[
  {
    "name": "globalPrompt",
    "control_name": "Global Prompt",
    "input_name": "string",
    "type": "string",
    "description": "This prompt describes the overall kitchen setting and sets the tone for the final image.",
    "default_value": "Modern farmhouse kitchen, bright.  Clean and crisp.  Marble countertops."
  },
  {
    "name": "vasePrompt",
    "control_name": "Prompt - Jar",
    "input_name": "string",
    "type": "string",
    "description": "This prompt targets the masked region the jar is in.",
    "default_value": "Stainless steel pitcher."
  },
  {
    "name": "teaCupPrompt",
    "control_name": "Prompt - Plate",
    "input_name": "string",
    "type": "string",
    "description": "This prompt targets the masked region the plate is in.",
    "default_value": "Wooden salad plate."
  },
  {
    "name": "counterPrompt",
    "control_name": "Prompt - Board",
    "input_name": "string",
    "type": "string",
    "description": "This prompt targets the masked region the Cutting Board is in.",
    "default_value": "Olive wood cutting board with a beautiful wood grain pattern."
  },
  {
    "name": "cabinetsPrompt",
    "control_name": "Prompt - Backsplash",
    "input_name": "string",
    "type": "string",
    "description": "This prompt describes the wall area directly behind the counter and the espresso machine.",
    "default_value": "Variety of small grey subway tiles, soft limestone with white veins. White grout."
  },
  {
    "name": "Image Input",
    "control_name": "ImageInput",
    "input_name": "image",
    "type": "image",
    "buffer_name": "LdrColor",
    "asset_path": "/World",
    "default_value": ""
  },
  {
    "name": "Depth Input",
    "control_name": "DepthInput",
    "input_name": "image",
    "type": "image",
    "buffer_name": "DepthLinearized",
    "asset_path": "/World",
    "default_value": ""
  },
  {
    "name": "Normal Input",
    "control_name": "NormalInput",
    "input_name": "image",
    "type": "image",
    "buffer_name": "SmoothNormal",
    "asset_path": "/World",
    "default_value": ""
  },
  {
    "name": "Depth Input Coffee Machine",
    "control_name": "DepthInputCoffeeMachine",
    "input_name": "image",
    "type": "image",
    "buffer_name": "DepthLinearized",
    "asset_path": "/World/Assets/EspressoMachine_adjust",
    "visibility": "hideothers",
    "default_value": ""
  },
  {
    "name": "Depth Input Jar",
    "control_name": "DepthInputJar",
    "input_name": "image",
    "type": "image",
    "buffer_name": "DepthLinearized",
    "asset_path": "/World/Assets/Spatula_Holder",
    "visibility": "hideothers",
    "default_value": ""
  },
  {
    "name": "Depth Input Board",
    "control_name": "DepthInputBoard",
    "input_name": "image",
    "type": "image",
    "buffer_name": "DepthLinearized",
    "asset_path": "/World/Assets/wood_cutting_board_seed_5_num_samp_1__mesh_sav_usdz__mesh_tex_2048__mesh_tar_10000_1",
    "visibility": "hideothers",
    "default_value": ""
  },
  {
    "name": "Depth Input Plate",
    "control_name": "DepthInputPlate",
    "input_name": "image",
    "type": "image",
    "buffer_name": "DepthLinearized",
    "asset_path": "/World/Assets/Espresso_Cup",
    "visibility": "hideothers",
    "default_value": ""
  },
  {
    "name": "Depth Input Kitchen",
    "control_name": "DepthInputKitchen",
    "input_name": "image",
    "type": "image",
    "buffer_name": "DepthLinearized",
    "asset_path": "/World/Assets/KitchenBase",
    "visibility": "hideothers",
    "default_value": ""
  },
  {
    "name": "Depth Input Walls",
    "control_name": "DepthInputWalls",
    "input_name": "image",
    "type": "image",
    "buffer_name": "DepthLinearized",
    "asset_path": "/World/Assets/KitchenBase",
    "visibility": "walls_hideothers",
    "default_value": ""
  },
  {
    "name": "Depth Input Nonwalls",
    "control_name": "DepthInputNonwalls",
    "input_name": "image",
    "type": "image",
    "buffer_name": "DepthLinearized",
    "asset_path": "/World/Assets/KitchenBase",
    "visibility": "walls_hideme",
    "default_value": ""
  }
]
