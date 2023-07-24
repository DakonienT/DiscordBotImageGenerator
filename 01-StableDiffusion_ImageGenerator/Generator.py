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
import logging
from datetime import datetime
import asyncio 

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

def between_async(pipe_thread, prompt_thread, channel_image):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(GenerationThread(pipe_thread, prompt_thread, channel_image))
    loop.close
    
async def GenerationThread(pipe_thread, prompt_thread, channel_image):
    logging.info("Startin GenerationThread for prompt " + prompt_thread)
    #image = pipe_thread(prompt_thread).images[0]
    image_id = random.randint(0,9999999)
    #image.save('/home/'+ str(image_id) + ".png")
    with open ('/home/test.jpg', 'rb') as img:
    #with open ('/home/' + str(image_id) + ".png", 'rb') as img:
        picture = discord.File(img)
        await channel_image.send(file=picture)

@bot.event
async def on_ready():
    logging.info('We have logged in as {0.user}'.format(bot))
    channel = bot.get_channel(TEXT_CHANNEL_ID)
    await channel.send("Hello ! VirIGo Bot is ready.")
    
@bot.command()
async def generateImage(ctx, prompt):
    logging.info(str(ctx.author.name) + " requested image generation with prompt : " + prompt)
    await ctx.send("I will generate an image for " + ctx.author.mention + " with prompt : " + prompt)
    channel = bot.get_channel(TEXT_CHANNEL_ID)
    threading.Thread(target=between_async, args=(pipe, prompt, channel)).start()
    
if __name__ == '__main__':
    now = datetime.now()
    logName = "/home/" + now.strftime("%d-%m-Y-%H-%M-%S") + ".log"
    logging.basicConfig(filename=logName, encoding='utf-8',level=logging.DEBUG)
    logging.info("LOG File name : " + logName)
    logging.info("Starting Bot")
    bot.run(token)