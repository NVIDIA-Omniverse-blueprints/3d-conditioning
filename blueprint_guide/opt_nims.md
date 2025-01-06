# **Augmentation Results and Analysis**

The examples below demonstrate generations from the sample images with the RealViz4 model. This model is a finetune on the base SDXL model, with an emphasis on photographic quality. Additionally, this model is a lightning model, (distilled) to perform much faster than the base SDXL model. As always, check the licenses on the models you choose to ensure your use is compliant.

<img src="../images/comfi_espresso.png">

*Image generated with live interactive demo.*

## **Optional NIM**

Edify3D, 360, USD Code, and USD Search are all optional NIM that you can extend this workflow with.  The following sections point you to resources to get started.

### **Edify 360**

*Optional*

With Shutterstock's Generative 3D service, users can now simply describe the exact environment they need in text or with an image, and out comes a high-dynamic-range panoramic image (360 HDRI) in brilliant 16K resolution. (See video below.)   
[blogs.nvidia.com/wp-content/uploads/2024/07/3\_HDRi\_SD\_30fps\_fast.mp4?\_=1](https://blogs.nvidia.com/wp-content/uploads/2024/07/3_HDRi_SD_30fps_fast.mp4?_=1)

* You can try out the preview model directly on build.nvidia.com here: [NVIDIA NIM | edify-360-hdri-early-access](https://build.nvidia.com/shutterstock/edify-360-hdri-early-access)  
* Developers can get API access here: [The Ultimate Generative 3D API ToolKit | Shutterstock](https://www.shutterstock.com/discover/generative-ai-3d)  
* In this NVIDIA Omniverse Blueprint, we have supplied example HDRI images for you to test with.

  > **Note** \- The Espresso Machine sample file includes two 360 HDRI images. Both were generated with  this NIM. You can switch between them in the interactive demo or the local kit app using the espresso machine configuration section. 

### **Edify 3D**

*Optional* 

Available now for enterprises in commercial beta, Shutterstock's Edify 360 service enables  designers and art directors to quickly generate 3D objects that help them prototype or populate virtual environments. For this example, Edify 3D uses generative AI to create assets like the cutting board on the kitchen counter, so you can focus on designing the espresso machine or developing the application.

* You can try out the preview model directly on build.nvidia.com here: [NVIDIA NIM | edify-3d](https://build.nvidia.com/shutterstock/edify-3d)  
* Developers can get API access here: [The Ultimate Generative 3D API ToolKit | Shutterstock](https://www.shutterstock.com/discover/generative-ai-3d)  
* Learn more below in the [Augmenting the Content Library](#augment-the-content-library) section.


    >**Note** \- The Espresso Machine sample file includes a cutting board. This was generated with this NIM and included in the file to demonstrate more ways to seed your scene. 

### **USD Code and USD Search**

*Optional* 

Optionally, you can integrate USD Code and USD Search to enable users to build scenes to place your configurable product asset. USD Code and USD Search help art directors add set dressing without needing to write the code themselves. USD Search uses AI to help identify and find the assets, while USD Code helps write Python code snippets and can execute scene modification directly. 

* [USD Code NIM — Omniverse Services latest documentation (nvidia.com)](https://docs.omniverse.nvidia.com/services/latest/services/usd-code/overview.html)  
* [USD Search NIM — Omniverse Services latest documentation (nvidia.com)](https://docs.omniverse.nvidia.com/services/latest/services/usd-search/overview.html)

If you want to develop Python code for OpenUSD directly in VS Code, you can use these links to easily set up [USD Code NIM](https://docs.omniverse.nvidia.com/services/latest/services/usd-code/overview.html) in [VS Code](https://docs.omniverse.nvidia.com/services/latest/services/usd-code/get-started.html#nim-vscode).

Learn more below in the [Scene Layout with NIM](./scene_layout.md) section.


----
<span style="float:left;">[&larr; Back to Guide](../README.md)</span>                     <span style="float: right;">[Next (Scene Layout with NIM)](./scene_layout.md)</span>