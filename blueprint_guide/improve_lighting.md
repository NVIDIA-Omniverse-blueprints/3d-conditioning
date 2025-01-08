# Improved Lighting Options

You may want to alter the set up to help render the hero asset seat into the scene more naturally, depending on your existing scene and lighting.  While we didn't demonstrate this in this blueprint, it is something you can develop in addition using the basic technique mentioned below.

<img src="../images/espresso_reflection.png" width="400">

*Image generated with live interactive demo.*

Example workflow:
1. Run the steps necessary to render a final image but without the hero asset (espresso machine).
2. Then take the result of that rendered image back into your kit based app and map that to a mesh ( plane, cylinder, projection etc...)  
3. With this in place you can now render the hero asset with the reflections baked in.
4. Send this result back to do a second pass with the same prompt or re-composite in ComfyUI 
5. Now the hero asset should have nicer reflections baked in.


----
| [&larr; Back to Guide](../README.md) |___________________________________________________________________________  | [Next (Reuse Masks) &rarr;](./reuse_masks.md)|
|-------------------------------|--|---------------------------------------------|