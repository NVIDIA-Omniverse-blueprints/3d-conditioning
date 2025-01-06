# **Requirements and Installation | ComfyUI**

Before you get started with ComfyUI, review the following requirements, then follow the ComfyUI installation instructions below.  
   
>The document discusses legacy ComfyUI instead of V1 so you may experience a difference in UI in newer versions. 

Estimated time to complete this section is ~20min depending on internet connection.

1. Check your hardware matches the [Technical Requirements for the Omniverse Platform.](https://docs.omniverse.nvidia.com/embedded-web-viewer/latest/common/technical-requirements.html)  
2. Install [ComfyUI](https://github.com/comfyanonymous/ComfyUI) by following the installation instructions on their Github page.  
   1. **Windows** \- It is easiest to [install the portable standalone build](https://github.com/comfyanonymous/ComfyUI?tab=readme-ov-file#windows) for Windows, however a [manual install](https://github.com/comfyanonymous/ComfyUI?tab=readme-ov-file#manual-install-windows-linux) will also work.  
   2. **Linux** \- Use the [manual install](https://github.com/comfyanonymous/ComfyUI?tab=readme-ov-file#manual-install-windows-linux) method.  
3. Install [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager) by following the installation instructions on their Github page. Pay special attention to the different methods.  
   1. **Windows** with the portable version of ComfyUI should choose [method 2](https://github.com/ltdrdata/ComfyUI-Manager#installationmethod2-installation-for-portable-comfyui-version-comfyui-manager-only).  
      1. Skip to step 2 and save the link directly to avoid having to install git.   
   2. **Windows** or **Linux** with a manual install, choose [method 1](https://github.com/ltdrdata/ComfyUI-Manager#installationmethod1-general-installation-method-comfyui-manager-only).  
4. Download and install the required models and supporting files.  
   1. Download the RealVisXL_V4.0_Lightning model file  [RealVisXL_V4.0_Lightning.safetensors](https://huggingface.co/SG161222/RealVisXL_V4.0_Lightning/blob/main/RealVisXL_V4.0_Lightning.safetensors).   
      1. Move the file to the ComfyUI installation folder under `ComfyUI\models\checkpoints\`.  
   2. Download the ControlNet Union model [diffusion\_pytorch\_model.safetensors](https://huggingface.co/xinsir/controlnet-union-sdxl-1.0/blob/main/diffusion_pytorch_model.safetensors).  
      1. Move the file to the ComfyUI installation folder under `ComfyUI\models\controlnet\`.  
   3. Download or locate the example files provided for this workflow from the synthetic-data-examples on Github.  
      1. If you cloned this repository, the sample files can be found in the cloned repository file location under `{blueprint-repo/kit-streamer/source/extensions/omni.ai.viewport.core/data/sample_files}`
         1. OR download them directly here- [Sample files](https://github.com/NVIDIA-Omniverse-blueprints/3d-conditioning/blob/main/kit-streamer/source/extensions/omni.ai.viewport.core/data/sample_files)  
      2. The ComfyUI graph, `latest_example.json` at `{blueprint-repo/kit-streamer/source/extensions/omni.ai.viewport.core/data/latest_example.json}`
         1. OR download directly here - [latest_example.json](https://github.com/NVIDIA-Omniverse-blueprints/3d-conditioning/blob/main/kit-streamer/source/extensions/omni.ai.viewport.core/data/latest_example.json)

----
<span style="float:left;">[&larr; Back to Guide](../README.md)</span>                     <span style="float: right;">[Next (ComfyUI Graph Setup) &rarr;](./comfyui_graph_setup.md)</span>