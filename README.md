<h2><img align="center" src="https://github.com/user-attachments/assets/cbe0d62f-c856-4e0b-b3ee-6184b7c4d96f">NVIDIA Omniverse Blueprint: 3D Conditioning for Precise Visual Generative AI</h2>

<img src="images/kitchen_options.gif" width="400">

*Image generated with live interactive demo.*

Developers can integrate NVIDIA NIM microservices to build applications that leverage controllable generative AI for efficient 3D scene creation.

In this workflow guide, we outline how to create a system that allows users to quickly generate and manipulate scene elements, using an espresso machine sample asset. We then describe how other NIM microservices, including USD Code and USD Search, can be used to extend that base workflow for enhanced features such as scene layout.

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
* **USD Code NIM**: A  language model that answers OpenUSD knowledge queries and generates USD Python code.
* **USD Search NIM**: An AI-powered search for OpenUSD data, 3D models, images, and assets using text or image-based inputs.


All microservices are currently available as a preview on the [NVIDIA API Catalog](https://build.nvidia.com/explore/discover/), where developers can make API calls for evaluation.

By the end of this workflow guide, you will be able to run the application on it's own or if you want to customize your own kit application, you will learn how to create a custom workflow with AI to enable and accelerate your creative teams.

# Table of Contents
- [Workflow Summary](./docs/00_workflow.md)
  - [Standard Workflow](./docs/00_workflow.md/#standard_workflow)
  - [Workflow Diagram](./docs/00_workflow.md/#workflow_diagram)
- [Get Started](./docs/01_get_started.md)
  - [System Requirements](./docs/01_get_started.md/#system_requirements)
  - [Preview API Key (optional, required for custom workflow)](./docs/02_api_key.md)
- [Run the Application (no custom workflow)](./docs/03_run_app.md)
- [Create Your Own Application (optional, custom workflow)](./docs/04_create_app.md)
  - [Add Extensions](./docs/05_add_ext.md)
    - [Configure Extensions with NIM](./docs/06_config_ext.md)
  - [ComfyUI Overview](./docs/07_comfyui.md)
    - [Requirements & Installation](./docs/08_comfyui_install.md)
    - [Graph Setup](./docs/09_comfyui_graph_setup.md)
    - [Configure Image Generation Service](./docs/10_config_img_srv.md)
    - [Assigning References & Models](./docs/11_assign_models_refs.md)
    - [Graph Breakdown](./docs/12_graph_breakdown.md)
    - [Connecting Kit Application to Image Generation Service](./docs/13_connect_comfyui_app.md)
- [Prompting Best Practices](./docs/14_prompt_bp.md)
- [Add Other NIMs(optional)](./docs/15_opt_nims.md)
  - [Scene Layout With NIM](./docs/16_scene_layout.md)
  - [Content Library Management](./docs/17_content_library.md)
- [Scene Structure and Assets](./docs/18_scene_struc.md)
- [Scene Navigation with ActionGraph](./docs/19_scene_nav.md)
- [Messaging for Web Based Front End](./docs/20_messaging_web.md)
- [Deployment](./docs/21_deployment.md)
  - [Creating a Deployable Service for ComfyUI](./docs/22_deployable_srv.md)
  - [Building Containers from Source](./docs/23_containers_source.md)
  - [Run Locally without Kubernetes](./docs/24_run_without_kubernetes.md)
- [Additional Usage](./docs/25_addtl_uses.md)
  - [Batch Prompt Ideation](./docs/25_addtl_uses.md/#batch-prompt-ideation)
  - [Improved Lighting](./docs/26_improve_lighting.md)
  - [Reuse Masks](./docs/28_reuse_masks.md)
  - [NSFW Filtering](./docs/29_nsfw_filters.md)
- [Known Issues and Limitations](./docs/30_known_issues.md)
- [Troubleshooting](./docs/31_troubleshooting.md)

----
<div align="right">
  <table>
    <tr>⠀⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀       </td>
      <td><a href="./docs/00_workflow.md">Workflow Summary &rarr;</a></td>
    </tr>
  </table>
</div>
