FROM ubuntu
RUN apt-get update && apt-get upgrade -y
RUN apt install python3-pip -y
ADD 01-StableDiffusion_ImageGenerator/requirements.txt /home/
ADD 01-StableDiffusion_ImageGenerator/Generator.py /home/
RUN pip3 install -r /home/requirements.txt
RUN useradd -u 8877 discord 
RUN mkdir -p /home/discord_bot_cache
RUN chown discord: /home/discord_bot_cache/
RUN mkdir -p /home/discord/
RUN chown discord: /home/discord/
ENV TRANSFORMERS_CACHE=/home/discord_bot_cache/
ENV CUDA_VISIBLE_DEVICES=""
USER discord
CMD ["python3", "/home/Generator.py" ]