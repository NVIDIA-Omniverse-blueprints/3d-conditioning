# **Augment the Content Library**

*Optional* 

In some cases, creators may need assets that do not already exist in their current 3D model library. Edify 3D and Edify 360 can generate additional assets and HDRI environments to fill these gaps. These new assets can then be added to your content library for team-wide use. Furthermore, USD Search, from the [previous section](./scene_layout.md), can be integrated to help locate assets within the content library efficiently. 

As a developer, you can integrate Edify 3D to generate assets that can be used in a composition. Here is a workflow to incorporate this functionality:

1. **Generate 3d objects**: Use Edify 3D or Edify 360 to create new assets or HDRI environments.  
2. **Add to content library**: Store generated assets in your content library.  
3. **Import assets:** Use drag-and-drop or **USD Search** to locate and add assets to the scene.  
4. **Apply materials**. If desired, apply the white materials to lean on just the shape of the objects or apply basic materials to help influence the AI, depending on the creator's goals.   
5. **Position and transform**. Use USD Code to place and transform the assets within the scene.

----
| [&larr; Back to Guide](../README.md) |___________________________________________________________________________  | [Next (Scene Structure & Assets) &rarr;](./scene_struc.md)|
|-------------------------------|--|---------------------------------------------|