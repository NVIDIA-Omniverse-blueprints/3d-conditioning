
## **Set Up and Open the ComfyUI Graph Example**

ComfyUI is a powerful backend and GUI for building and executing pipelines using diffusion models and more.

<img src="../images/comfi_07.png" width=600>

1. #### Run ComfyUI.  
   1. Windows Portable \- Run `ComfyUI_windows_portable\run_nvidia_gpu.bat`  
   2. Windows and Linux Manual Install \- Using the command line, run `python main.py`  
   3. The ComfyUI server process runs in a command line window. There, you can view what ComfyUI is doing if you need to check for errors, warnings, or to see the progress of image generations.  
   4. When fully loaded ComfyUI  opens a window in your Internet browser with the local address '[http://127.0.0.1:8188/](http://127.0.0.1:8188/)'. This is connecting the visual frontend to the ComfyUI server now running in the background.  
</br>
2. #### Loading the example graph.  
   1. Next, 'Load' the file `latest_example.json` that was downloaded earlier from the example links. 
      1. Click the **Load** button on the ComfyUI menu. 
      2. Navigate to the location of the downloaded `.json` graph and open it.  
      <img src="../images/comfi_13.png" width=200>  
   2. You will see an error window showing missing dependencies, along with red 'missing' nodes behind it. This is expected.  
      <img src="../images/comfi_12.png" width=600>  
   3. This issue can be resolved by following the steps below.  
      1. Click the **Manager** button at the bottom of the ComfyUI menu.  
         <img src="../images/comfi_06.png" width=200> 
      2. If you do not see a **Manager** button, see the [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager) section in the 'Requirements and Installation' section of this guide.  
      3. Select the **Install Missing Custom Nodes** button in the middle top section of the ComfyUI Manager Menu.  
         <img src="../images/comfi_02.png" width=600>  
      4. Select **Install** for each of the listed node dependencies, or you can select the checkbox next to ID (upper left) to select them all, then select **Install**. These may take several minutes, depending on your Internet speed and hardware. You can check the progress of these downloads in ComfyUI's command line window.  
         <img src="../images/comfi_14.png" width=800>  
      5. Once you have installed all node dependencies, click on the red **Restart** button at the bottom. This restarts the ComfyUI local server to enable the newly added dependencies. 
            > Note that you do not need to close the browser window, but a 'Reconnecting…' dialog is  displayed until the server has been restarted.  
      6. This first restart may take several minutes, downloading more dependencies as needed. You can always view the progress in the command line window.  
      7. After installing the dependencies, your graph will no longer display any bright red missing nodes and you can move to the next section.

----
<span style="float:left;">[&larr; Back to Guide](../README.md)</span>                     <span style="float: right;">[Next (ComfyUI Configure Image Gen Service) &rarr;](./config_img_srv.md)</span>