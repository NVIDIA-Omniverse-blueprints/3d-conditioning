# **Configure the Extensions with NIM**

The extensions from the previous section, [adding extentions](./add_ext.md), will connect your custom Kit application to ComfyUI and the generative image ai model connected to it, as well as the configurable options with USD Variants and event messaging with Omni Graph.  It also uses the same style UI as shown in the interactive web experience demonstrating how the Kit UI can be customized. Understanding the following connections will help you connect your own content.

> **Note** \- Follow each NIM extension, where applicable, to add your API key to enable your NIM.

## Add NIM to your custom application

*Required*

There are a variety of ways to use AI to augment a workflow in a directable manner. First, you must integrate the NIM to a custom Kit extension and add it to your custom Kit application.

The microservices in this workflow are currently available as a preview on the [NVIDIA API Catalog](https://build.nvidia.com/explore/discover/), where developers can make API calls for evaluation. 

You will need your API Catalog API key for this section. Please refer back to the [API key](./api_key.md) section of this blueprint to acquire your API key.

In order to integrate NIM into your application, you will be making API calls to the various endpoints. NIMs are purposefully made to be easy to deploy anywhere in an optimized fashion. Depending on how you deploy the NIM, your setup will vary; however, once NIMS are operating, it is a simple task of making your API calls and working with the results.

The first part of this workflow is to integrate the Image Generation Service using ComfyUI, please see the next section to get started. 

----
| [&larr; Back to Guide](../README.md) |___________________________________________________________________________  | [Next (ComfyUI) &rarr;](./comfyui.md)|
|-------------------------------|--|---------------------------------------------|