# Deployment

This part describes how to deploy the blueprint on Linux kubernetes cluster. The purpose of this is to demonstrate how the architecture works. Recall that the image generation service is a stub where it will return static image (You are expected to see [this image](#the-stub-image-generation-output) as an output) instead of running diffusion models. We provide guide to create your own image generation service specifically [here](#configure-the-image-generation-service).

## Deploying Default Distribution

The distribution goes with a simple image generation stub, which takes the viewport rendered image, puts some text over it, and that is all it does. This means that the web UI dropdowns will affect the final picture, because they affect the initial rendering, but the composition prompts will not affect the final picture, as this simple stub just copies over an image.

It is expected that the user will have a kubernetes cluster with GPU available. Single deployment of the default blueprint requires a single NVIDIA GPU to run the rendering/streaming container. NOTE: [the system requirements](#system-requirements)
The instructions here are for the microk8s edition of kubernetes specifically.
The user also needs to have access to the NGC container registry where the default containers are registered. Please refer to [NGC Private Registry User Guide](https://docs.nvidia.com/ngc/gpu-cloud/ngc-private-registry-user-guide/index.html#accessing-ngc-registry)

Deployment is a single-machine configuration, i.e. user has to access the application through the web browser on the same machine where it was deployed.

Steps
1. Clone this repository
2. Go to the folder where it was cloned.
3. Once you get your NGC API key, please set these environment variables as follows:
   ```
   export DOCKER_API_KEY=$NGC_CLI_API_KEY
   ```
   Env variables `DOCKER_REPO` and `DOCKER_API_UNAME` are not required to be set as they use default values for `nvcr.io` – but they can be set in the env to override the default values (which is not needed unless custom docker repo is used).

4. Execute `./deploy.sh`

   After blueprint deployment is finished, you will see a text saying

   > Use the following URL to launch the blueprint:
   > http://<IP_ADDRESS>:<PORT>/?server=<IP_ADDRESS>

   (e.g. http://10.152.183.212:3000/?server=10.152.183.16)

5. Copy the provided URL as-is (including the `?server=..`. part, this is important) and put it into the browser address bar. Access the application through the browser on the same machine where it was deployed.
6. The initial launch of the Kit application in the streamer container after it was created will take some time to compile shaders of the complex materials. On some machines, this time can be up to several minutes. During this time, the streaming window on the web playground will display a black square - this is normal, waiting for some time should resolve this, and you will see the rendered image.

You can interact with the application now.

If you are blocked because your node does not have gpu, try `microk8s enable nvidia` / `microk8s enable gpu`.

Useful to know that the streamer pod will contain logs related to rendering and streaming of the rendered image. You can check logs by first examining all available pods on a cluster, and then executing the log viewing command for the streamer pod using its identifier:
```
microk8s kubectl get pods
microk8s kubectl logs -f streamer-698dc4687d-xcwtq
```

----
| [&larr; Back to Guide](../README.md) |___________________________________________________________________________  | [Next (Deployable Service) &rarr;](./deployable_srv.md)|
|-------------------------------|--|---------------------------------------------|