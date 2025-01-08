# Get Started

*Required*

**Manifest**  
For this NVIDIA Omniverse Blueprint, you need the following components:

| Component | Notes |
| :---- | :---- |
| Blueprint Sample repo | The repo you are currently in [https://github.com/NVIDIA-Omniverse-blueprints/3d-conditioning](https://github.com/NVIDIA-Omniverse-blueprints/3d-conditioning) |
| NIM | [https://build.nvidia.com/explore/discover](https://build.nvidia.com/explore/discover) |
| Kit-app-template 106.2 | [NVIDIA-Omniverse/Kit-app-template: Omniverse Kit App Template (github.com)](https://github.com/NVIDIA-Omniverse/kit-app-template/) |
| ComfyUI | [https://github.com/comfyanonymous/ComfyUI](https://github.com/comfyanonymous/ComfyUI) |
| SDXL or similar image to image model | [https://huggingface.co/SG161222/RealVisXL\_V4.0\_Lightning/blob/main/RealVisXL\_V4.0\_Lightning.safetensors](https://huggingface.co/SG161222/RealVisXL_V4.0_Lightning/blob/main/RealVisXL_V4.0_Lightning.safetensors) |

# Set Up the Environment

*Required*

### **System Requirements**

* See [NVIDIA Omniverse Blueprint Card](https://build.nvidia.com/nvidia/conditioning-for-precise-visual-generative-ai/blueprintcard)

### **Required Software Dependencies**

* Git: For version control and repository management  
* Git LFS: For managing large files within the repository  
* (Windows) Microsoft Visual C++ Redistributable: Many Windows systems already have this installed. If not, you can obtain it from [latest-supported-vc-redist](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#latest-microsoft-visual-c-redistributable-version).  
* (Linux) build-essentials: A package that includes make and other essential tools for building applications. For Ubuntu, install with `sudo apt-get install build-essential`. For deployment, you must use Linux and have Kubernetes.  
* Node.js

### **Recommended Software**

* VS Code (or your preferred IDE): For code editing and development.
  
----

| [&larr; Back to Guide](../README.md) |___________________________________________________________________________  | [Next (API Key) &rarr;](./api_key.md)|
|-------------------------------|--|---------------------------------------------|