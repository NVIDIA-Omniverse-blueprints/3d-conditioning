# Creating a Deployable Service for ComfyUI

Follow this guide to take further steps to create a service that can be deployed in our [deployment section](./deployment.md). You may skip it for now if you not wish to deploy at the moment.

1. Inspect the ComfyUI installation directory
   1. `custom_nodes` contains the nodes you need to include in your service
   2. `models` contains the diffusion models and/or controlnet that you need to include in your service
2. We recommend you modify existing `imagegen_stub` directory to quickly come up with working service
   1. Modify the dockerfile to install essential packages to install Python3.10 or higher, pip, git, git lfs and wget
   2. `git clone` ComfyUI (you may prefer to pin the commit by `git checkout <COMMIT_HASH>`)
   3. `cd` into `custom_nodes` directory and `git clone` all the nodes with pinning
   4. `wget` the diffusion model and/or controlnet to `models` directory
   5. Expose the port you wish to use
   6. Run ComfyUI by specifying the ip address and the port number (Now `imagegen_stub.py` is no longer relevant, so you can delete it)

Here's an example of how you can structure your Dockerfile:

```
# Dockerfile for setting up ComfyUI environment
# Replace <BASE_UBUNTU_IMAGE> with your base Ubuntu Image
FROM <BASE_UBUNTU_IMAGE>

# Replace <PACKAGE_X> with packages you want to install
RUN apt update && apt install -y <PACKAGE_1> <PACKAGE_2> ... <PACKAGE_X>

# Replace <WORKDIR_PATH> with your working directory path for ComfyUI installation
WORKDIR <WORKDIR_PATH>

# Set virtual environment here

# Clone ComfyUI repository, pinning to a specific commit hash if needed
# When you are pip installing (Pytorch, xFormers, etc), beware of using proper options such as --index-url https://download.pytorch.org/whl/cu121
RUN git clone <COMFYUI_REPO_URL> && cd <COMFYUI_DIRECTORY> && git checkout <COMMIT_HASH> && pip install -r requirements.txt

# Download diffusion models and/or controlnet
RUN wget -c <DIFFUSION_MODEL_URL> -P <COMFYUI_DIRECTORY>/models/checkpoints/
wget  -c <CONTROLNET_URL> -P <COMFYUI_DIRECTORY>/models/controlnet/

# Clone ComfyUI custom node repository, pinning to a specific commit hash if needed
# Note that some ComfyUI custom nodes does not contain any installable packages, so you may skip it if it's not necessary for your use case
RUN cd <COMFYUI_DIRECTORY>/custom_nodes && git clone <COMFYUI_CUSTOM_NODE_REPO_URL> && cd <COMFYUI_CUSTOM_NODE_DIRECTORY> && git checkout <COMMIT_HASH> && pip install -r requirements.txt

# Create a directory for checkpoints if it doesn't exist already (you may change /tmp/ckpts path as per your requirements)
RUN mkdir -p /tmp/ckpts

EXPOSE <PORT>

ENTRYPOINT ["python", <COMFYUI_MAIN_PATH>, "--listen", <IP_ADDRESS>, "--port", <PORT>]
```

----
| [&larr; Back to Guide](../README.md) |___________________________________________________________________________  | [Next (Building Containers from Source) &rarr;](./containers_source.md)|
|-------------------------------|--|---------------------------------------------|