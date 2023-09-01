#Deriving the latest base image
FROM python:3

# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/app/src

#set up environment
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#to COPY the remote file at working directory in container
COPY main.py ./

#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

CMD [ "python", "./main.py"]
