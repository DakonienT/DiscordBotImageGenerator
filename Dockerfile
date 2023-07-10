FROM ubuntu
RUN apt-get update && apt-get upgrade -y
RUN apt install python3-pip -y
ADD 01-StableDiffusion_ImageGenerator/requirements.txt /home/
ADD 01-StableDiffusion_ImageGenerator/Generator.py /home/
RUN pip3 install -r /home/requirements.txt
RUN useradd -u 8877 discord
USER discord
CMD ["python3", "/home/Generator.py" ]