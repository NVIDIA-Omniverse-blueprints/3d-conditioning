# Building Containers from Source

We also provide sources for certain containers, allowing users to experiment with them.
To build containers, users need to have access to the docker images repository.

### Steps:
1. Before pushing containers, login into the desired repository. For the `nvcr.io` repository, it will look like this (assuming **env var** `NGC_CLI_API_KEY` is set to the proper NGC key, refer to this [NGC document](https://org.ngc.nvidia.com/setup) for details):
   ```
   docker login nvcr.io -u "\$oauthtoken" -p $NGC_CLI_API_KEY
   ```
2. For example purposes, our internal repository is shown below. Users can adjust it to the repository of their choosing. In our case, the related **env var** would be defined as following:
   ```
   export REPOSITORY_URL=nvcr.io/nvidia/omniverse
   ```
3. For `imagegen_stub`, build steps are the following from the root:
   ```
   export CONTAINER_URL=$REPOSITORY_URL/conditioning-for-precise-visual-generative-ai-imagegen-stub
   export CONTAINER_VERSION=$(head -n 1 imagegen_stub/version.md)

   docker build -t $CONTAINER_URL:$CONTAINER_VERSION -f imagegen_stub/Dockerfile.stub imagegen_stub

   docker push $CONTAINER_URL:$CONTAINER_VERSION
   ```

4. For `kit-streamer`, build steps are the following from the root (you may need to install docker compose if it fails on packaging step):
   ```
   cd kit-streamer

   export CONTAINER_URL=$REPOSITORY_URL/conditioning-for-precise-visual-generative-ai-streaming
   export CONTAINER_VERSION=$(head -n 1 VERSION.md)

   ./build.sh -ru

   ./repo.sh package --container --target-app omni.app.conditioning_for_precise_visual_generative_ai_streaming.kit --name $CONTAINER_URL:$CONTAINER_VERSION

   docker push $CONTAINER_URL:$CONTAINER_VERSION
   ```

----
<div align="center">
  <table>
    <tr>
      <td align="left"><a href="./22_deployable_srv.md">&larr; Creating a Deployable Service for ComfyUI</a></td>
      <td align="center">⠀⠀⠀⠀⠀⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀       </td>
      <td align="right"><a href="./24_run_without_kubernetes.md">Run Locally without Kubernetes &rarr;</a></td>
    </tr>
  </table>
</div>
