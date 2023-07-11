import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
import discord
from discord.ext.commands.bot import Bot
from discord.ext import commands
import random
import os
import threading
import time

#Set discord client
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
token = os.getenv('DISCORD_TOKEN')
TEXT_CHANNEL_ID = 1068254639750922260
print("Bot will use token " + token)

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
pipe = pipe.to(DEVICE)
#pipe.enable_sequential_cpu_offload()

#image = pipe(prompt).images[0]
#image.save("test.png")

def GenerationThread(pipe_thread, prompt_thread, channel_image):
    print("Starting generation thread")
    image = pipe_thread(prompt_thread).images[0]
    image_id = random.randint(0,9999999)
    image.save(str(image_id) + ".png")
    with open ('/home/' + str(image_id) + ".png", 'rb') as img:
        picture = discord.File(img)
        channel_image.send(file=picture)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    channel = bot.get_channel(TEXT_CHANNEL_ID)
    await channel.send("Hello ! VirIGo Bot is ready.")
    
@bot.command()
async def generateImage(ctx, prompt):
    await ctx.send("I will generate an image for " + ctx.author.mention + " with prompt : " + prompt)
    channel = bot.get_channel(TEXT_CHANNEL_ID)
    threading.Thread(target=GenerationThread, args=(pipe,prompt,channel)).start()

bot.run(token)