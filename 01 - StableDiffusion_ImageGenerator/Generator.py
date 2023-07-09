import torch
from torch import autocast
from diffusers import StableDiffusionPipeline


HF_TOKEN="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"
MODEL_ID = "CompVis/stable-diffusion-v1-4"
DEVICE = "cuda"

print("Creating generator with device " + DEVICE)
generator = torch.Generator(DEVICE)
print("Calling pipe")
pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,revision="fp16", 
    torch_dtype=torch.float16,
    height = 512,
    width = 512, 
    safety_checker = None,
    num_inference_steps=15,
    use_auth_token = HF_TOKEN, 
    generator=generator)
pipe = pipe.to(DEVICE)

prompt = "a photograph of an astronaut riding a horse"

print("The prompt is : " + prompt)

with autocast(DEVICE):
    print("Getting image")
    image = pipe(prompt, guidance_scale=7.5, generator=generator).images[0]
    image.save("test.png")
print("Done.")
