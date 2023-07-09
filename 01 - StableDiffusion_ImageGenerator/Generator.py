import torch
from torch import autocast
from diffusers import StableDiffusionPipeline


HF_TOKEN="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"
MODEL_ID = "CompVis/stable-diffusion-v1-4"
DEVICE = "cuda"

#print("Creating generator with device " + DEVICE)
#generator = torch.Generator(DEVICE)
print("Calling pipe")
pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,revision="fp16", 
    height = 512,
    width = 512, 
    safety_checker = None,
    num_inference_steps=15,
    use_auth_token = HF_TOKEN)
#pipe = pipe.to(DEVICE)
pipe.enable_sequential_cpu_offload()

prompt = "a photograph of an astronaut riding a horse"

print("The prompt is : " + prompt)


print("Getting image")
image = pipe(prompt).images[0]
image.save("test.png")

print("Done.")
