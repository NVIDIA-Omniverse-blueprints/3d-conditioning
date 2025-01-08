<h2><img align="center" src="https://github.com/user-attachments/assets/cbe0d62f-c856-4e0b-b3ee-6184b7c4d96f">NVIDIA Omniverse Blueprint: 3D Conditioning for Precise Visual Generative AI</h2>

<img src="images/kitchen_options.gif" width="400">

*Image generated with live interactive demo.*

Developers can integrate NVIDIA NIM microservices to build applications that leverage controllable generative AI for efficient 3D scene creation.

In this workflow guide, we outline how to create a system that allows users to quickly generate and manipulate scene elements, using an espresso machine sample asset. We then describe how other NIM microservices, including USD Code, USD Search, Edify 360 and Edify 3D, can be used to extend that base workflow for enhanced features such as scene layout. 

This guide includes:

1. The standard workflow to replicate what is on the NVIDIA Omniverse Blueprint web page.  
2. Optional NIM that you could integrate on your own to further accelerate scene layout beyond the demonstration in the standard workflow guide.

[NVIDIA NIM](https://www.nvidia.com/en-us/ai/) microservices are a set of accelerated inference microservices that allow developers to easily deploy AI models on NVIDIA GPUs anywhere.

For this workflow, we specifically explore microservices that enable developers to use generative backgrounds, while also taking advantage of OpenUSD for 3D application and workflow development. 

<img src="images/brutalist.png" width="400">

*Image generated with live interactive demo.*

These workflows may include:

* **SDXL \+ ComfyUI**: A fast generative text-to-image model that can synthesize photorealistic images from a text prompt in a single network evaluation with a graph/nodes interface for advanced developers.  

   *The following NIM are optional microservices.*
* **Edify 360 NIM**: Shutterstock Early Access preview of Generative 3D service for 360 HDRI (High Dynamic Range Image) generation. Trained on NVIDIA Edify using Shutterstock's licensed creative libraries.  
* **Edify 3D NIM**: Shutterstock Generative 3D service for 3D asset generation. Trained on NVIDIA Edify using Shutterstock's licensed creative libraries.  
* **USD Code NIM**: A  language model that answers OpenUSD knowledge queries and generates USD Python code.  
* **USD Search NIM**: An AI-powered search for OpenUSD data, 3D models, images, and assets using text or image-based inputs.


All microservices are currently available as a preview on the [NVIDIA API Catalog](https://build.nvidia.com/explore/discover/), where developers can make API calls for evaluation.

By the end of this workflow guide, you will be able to run the application on it's own or if you want to customize your own kit application, you will learn how to create a custom workflow with AI to enable and accelerate your creative teams.

# Table of Contents 
- [Workflow Summary](./blueprint_guide/workflow.md)
  - [Standard Workflow](./blueprint_guide/workflow.md/#standard_workflow)
  - [Workflow Diagram](./blueprint_guide/workflow.md/#workflow_diagram)
- [Get Started](./blueprint_guide/get_started.md)
  - [System Requirements](./blueprint_guide/get_started.md/#system_requirements)
  - [Preview API Key (optional, required for custom workflow)](./blueprint_guide/api_key.md)
- [Run the Application (no custom workflow)](./blueprint_guide/customize_app.md)
- [Create Your Own Application (optional, custom workflow)](./blueprint_guide/create_app.md)
  - [Add Extensions](./blueprint_guide/add_ext.md)
    - [Configure Extensions with NIM](./blueprint_guide/config_ext.md)
  - [ComfyUI Overview](./blueprint_guide/comfyui.md)
    - [Requirements & Installation](./blueprint_guide/comfyui_install.md)
    - [Graph Setup](./blueprint_guide/comfyui_graph_setup.md)
    - [Configure Image Generation Service](./blueprint_guide/config_img_srv.md)
    - [Assigning References & Models](./blueprint_guide/assign_models_refs.md)
    - [Graph Breakdown](./blueprint_guide/graph_breakdown.md)
    - [Connecting Kit Application to Image Generation Service](./blueprint_guide/connect_comfyui_app.md)
- [Prompting Best Practices](./blueprint_guide/prompt_bp.md)
- [Add Other NIMs(optional)](./blueprint_guide/opt_nims.md)
  - [Scene Layout With NIM](./blueprint_guide/scene_layout.md)
  - [Augment the Content Library with Edify](./blueprint_guide/content_library.md)
- [Scene Structure and Assets](./blueprint_guide/scene_struc.md)
- [Scene Navigation with ActionGraph](./blueprint_guide/scene_nav.md)
- [Messaging for Web Based Front End](./blueprint_guide/messaging_web.md)
- [Deployment](./blueprint_guide/deployment.md)
  - [Creating a Deployable Service for ComfyUI](./blueprint_guide/deployable_srv.md)
  - [Building Containers from Source](./blueprint_guide/containers_source.md)
  - [Run Locally without Kubernetes](./blueprint_guide/run_without_kubernetes.md)
- [Additional Usage](./blueprint_guide/addtl_uses.md)
  - [Batch Prompt Ideation](./blueprint_guide/addtl_uses.md/#batch-prompt-ideation)
  - [Improved Lighting](./blueprint_guide/improve_lighting.md)
  - [Reuse Masks](./blueprint_guide/reuse_masks.md)
  - [NSFW Filtering](./blueprint_guide/nsfw_filters.md)
- [Known Issues and Limitations](./blueprint_guide/known_issues.md)
- [Troubleshooting](./blueprint_guide/troubleshooting.md)
