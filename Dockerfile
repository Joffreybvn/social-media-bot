
FROM python:3.9-slim-buster

# Install the security updates
RUN apt-get update
RUN apt-get -y upgrade

# Remove all cached file. Get a smaller image
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# Copy the application
COPY . /opt/app
WORKDIR /opt/app

# Install python libraries
RUN pip install -r requirements.txt

# Start the app
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]