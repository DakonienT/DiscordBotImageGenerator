import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
import discord
from discord.ext.commands.bot import Bot
from discord.ext import commands

#Set discord client
intents = discord.Intents.all()
client = Bot(command_prefix='!', intents=intents)

MODEL_ID = "CompVis/stable-diffusion-v1-4" #Used for stable diffusion
DEVICE = "cpu" #Set device on which to run stable diffusin

#Stable diffusion pipeline setup
print("Creating generator with device " + DEVICE)
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

#image = pipe(prompt).images[0]
#image.save("test.png")


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
client.run('MTEyNzcwNzU1NTAzNzE4NDExMA.GysFei.mS8FUEXMsQUOnNjjb74cYwfZAHQdxihLObuWiY')