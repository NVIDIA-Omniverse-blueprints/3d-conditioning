# Run Locally without Kubernetes

Alternatively, you can run the **Kit application** and the **image generation service** locally. We do not provide the source for the web browser client, but it can be run as a container. You can also run only the Kit application and image generation service shown specifically in [Create your own Application](./create_app.md) section. Recall that the image generation service is a stub where it will return static image instead of running diffusion models. Refer back to the section [Configure Image Generation Service](./blueprint_guide/config_img_srv.md) to create your own image generation service.

1. Run the image generation service provided (the example stub service):
   1. Build `pip install -r requirements.txt` (you should be in `imagegen_stub` directory)
   2. `python imagegen_stub.py`
2. Ensure the your Kit App and your Image Generation Service are connected. Refer back to the section [Configure Image Generation Service](./blueprint_guide/config_img_srv.md) for more information.
3. Building and running the Kit application:
   1. `./build.sh -r` (you should be in `kit-streamer` directory)
   2. `./_build/linux-x86_64/release/omni.app.conditioning_for_precise_visual_generative_ai_streaming.sh` (note the `_streaming` postfix),
4. Pull the docker container of the web playground (available in `helm/charts/playground/values.yaml`, under `repository` key), and then run it through the `docker run -p 3000:3000 -t <container name:tag>`


----
| [&larr; Back to Guide](../README.md) |___________________________________________________________________________  | [Next (Additional Usage) &rarr;](./addtl_uses.md)|
|-------------------------------|--|---------------------------------------------|