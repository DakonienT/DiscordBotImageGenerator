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
import typing
import functools

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


async def run_blocking(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
    func = functools.partial(blocking_func, *args, **kwargs)
    return await bot.loop.run_in_executor(None, func)

def generate(file_path, prompt, image_id,channel):
    image = pipe(prompt).images[0]
    
    image.save(file_path)
    logging.info("Image with ID " + str(image_id) + " has been saved in " + str(file_path))


@bot.event
async def on_ready():
    logging.info('We have logged in as {0.user}'.format(bot))
    channel = bot.get_channel(TEXT_CHANNEL_ID)
    await channel.send("Hello ! VirIGo Bot is ready.")
    
_loop = asyncio.get_event_loop()    

@bot.command()
async def generateimage(ctx, prompt):
    image_id = random.randint(0,9999999)
    logging.info(str(ctx.author.name) + " requested image generation with prompt : " + prompt + ". Image ID will be " + str(image_id))
    await ctx.send("I will generate an image for " + ctx.author.mention + " with prompt : " + prompt)
    channel = bot.get_channel(TEXT_CHANNEL_ID)
    #threading.Thread(target=between_async, args=(pipe, prompt, channel)).start()
    file_path = str(image_id) + ".png"
    #asyncio.run_coroutine_threadsafe(generate(file_path, prompt,image_id, channel), _loop)
    #await generate(file_path, prompt,image_id, channel)
    r = await run_blocking(generate, file_path, prompt, image_id, channel)
    print(r)
    with open ( file_path, 'rb') as img:
        picture = discord.File(img)
        await channel.send(file=picture)

    
    
    
if __name__ == '__main__':
    mylogs = logging.getLogger(__name__)
    mylogs.setLevel(logging.INFO)
    now = datetime.now()
    logName =  now.strftime("%d-%m-Y-%H-%M-%S") + ".log"
    file = logging.FileHandler(logName)
    mylogs.setLevel(logging.DEBUG)
    fileformat = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s",datefmt="%H:%M:%S")
    file.setFormatter(fileformat)
    mylogs.addHandler(file)
    #logging.basicConfig(filename=logName, encoding='utf-8',level=logging.DEBUG)
    logging.info("LOG File name : " + logName)
    logging.info("Starting Bot")
    bot.run(token)