# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

add website/ website/

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local website directory to the working directory
COPY website/ .

# command to run on container start
CMD [ "python", "./app.py" ]
