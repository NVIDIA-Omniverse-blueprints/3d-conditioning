# Additional Usage

This section will briefly go over some additional usage cases & techniques to inspire other ways you may use this blueprint.

## Batch Prompt Ideation

By utilizing some simple scripts, we can automate the app locally to run a bunch of prompts all at once. This allows a team to do achieve two things.

1. Test a variety of prompts while out to lunch to see what kind of prompts resonate the best.
2. Testing iterations of your pipeline with a series of benchmark prompts.

<img src="../images/batchOutput.png" width="600">

Steps (skip to the last step below using Script Editor if you wish to simply call the batch from your custom function or extension)
1. Modify the blueprint codebase to make menu bar visible

   1. Open [setup.py file](https://github.com/NVIDIA-Omniverse-blueprints/3d-conditioning/blob/markdown_edits/kit-streamer/source/extensions/omni.conditioning_for_precise_visual_generative_ai.setup/omni/conditioning_for_precise_visual_generative_ai/setup/setup.py) and edit:
      ```
      main_menu_bar.visible = True
      ```

   2. Open [extension.toml](https://github.com/NVIDIA-Omniverse-blueprints/3d-conditioning/blob/markdown_edits/kit-streamer/source/extensions/omni.conditioning_for_precise_visual_generative_ai.setup/config/extension.toml) file and edit:
      ```
      [settings.exts."omni.conditioning_for_precise_visual_generative_ai.setup"]
      menu_visible = true
      ```      

2. Build your kit app (for Blueprint sample, **cd kit-streamer**)

    **Linux**: `./repo.sh build`
    **Windows**: `.\repo.bat build`

2. Launch your application. For example, for our Blueprint sample, run the following command:

      **Linux** `./_build/linux-x86_64/release/omni.app.conditioning_for_precise_visual_generative_ai_desktop.sh --enable omni.kit.window.script_editor`

      **Windows** `.\_build\windows-x86_64\release\omni.app.conditioning_for_precise_visual_generative_ai_desktop.bat --enable omni.kit.window.script_editor`

3. Open a script editor from the menu bar and execute the following script (or add it to the function that you wish to run a batch for your own purposes):
      ```
      from omni.conditioning_for_precise_visual_generative_ai.setup.setup import generate_csv
      generate_csv(<PATH_TO_CSV_FILE>)
      ```

Sample CSV file

| Display Type | Machine Color | Mug Type | HDRI | Global | Plate | Jar | Cutting Board | Kitchen |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Touch Screen | Blue | Glass Mug | Lighting 1 | morning light | a red cup with yellow plate | green jar with red flowers | light wood cutting board | "light grey cabinets, dark brown granite counter top, beige limestone tiles that are oriented horizontal, window frame" |
| Analog | Black | Glass Mug | Lighting 2 | cool winter morning | add cheese cubes to the plate | cookie jar | dark brown cutting board with a block of cheese on it | "butcher block counter top, white cabinets, dark metal cabinet handles and knobs, large silver back splash tiles with ornate pattern" |

----
| [&larr; Back to Guide](../README.md) |___________________________________________________________________________  | [Next (Improved Lighting) &rarr;](./improve_lighting.md) |
|-------------------------------|--|---------------------------------------------|
