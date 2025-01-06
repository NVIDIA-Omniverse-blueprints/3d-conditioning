## **Prompting Techniques and Best Practices**

We're in the early days of generative models as a technology. The techniques within this example affect results in different ways. Below are some considerations to keep in mind.

**Prompting**

There is a 'global prompt' and 'regional' prompts. The global prompt guides the entire generation, including (to a degree) the regional areas. It's best practice to keep the global description to the lighting, the quality and style of the scene, and avoid words like colors which can get misinterpreted.

Prompt adherence and natural language is an improving area for diffusion models, but this base model (SDXL) is not perfect. It can be challenging to successfully generate outputs with detailed descriptions. Each generation uses a random seed, and several tried may be needed to get the best results.

The weights of words in prompts can be altered. '(blue:1.5)' will increase the prompt weight by 1.5 times against other words in that prompt. Lastly, the ordering of words in prompts matters. 

[Best practices for prompting with ComfyUI can be found here.](https://comfyui-wiki.com/tutorial/basic/stable-diffusion-prompt-basic)

Keeping Prompts to 3-5 phrases generally is recommended to yield the best results.


----
<span style="float:left;">[&larr; Back to Guide](../README.md)</span>                     <span style="float: right;">[Next (Add Other NIMs) &rarr;](./opt_nims.md)</span>