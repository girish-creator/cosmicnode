FROM ubuntu:latest

MAINTAINER cosmicnode girikripa@outlook.com

# run update
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/*

# add repositories
RUN add-apt-repository universe
RUN add-apt-repository ppa:mosquitto-dev/mosquitto-ppa

# install python3 and pip
RUN apt-get install -y python3-pip

# install mqtt
RUN apt-get install -y mosquitto
RUN apt-get install -y mosquitto-clients

# install build-essential
RUN apt-get install -y build-essential

# make a clean apt
RUN apt clean

WORKDIR /app

# copy files from local host to docker container
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# run a few commands
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD [ "python3", "./common/runner.py"]