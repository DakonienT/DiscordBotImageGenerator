import torch
from torch import autocast
from diffusers import StableDiffusionPipeline


HF_TOKEN="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"
MODEL_ID = "CompVis/stable-diffusion-v1-4"
DEVICE = "cpu"

#print("Creating generator with device " + DEVICE)
generator = torch.Generator(DEVICE)
print("Calling pipe")
pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID, 
    safety_checker = None,
    guidance_scale=2,
    generator=generator
    )
#pipe = pipe.to(DEVICE)
pipe.enable_sequential_cpu_offload()

prompt = "a photograph of an astronaut riding a horse"

print("The prompt is : " + prompt)


print("Getting image")
image = pipe(prompt).images[0]
image.save("test.png")

print("Done.")
