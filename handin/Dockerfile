# Ubuntu Linux as the base image
FROM ubuntu:16.04

# Install the packages
RUN apt-get update -y && \
    apt-get install -y python3

# Open the following ports
EXPOSE 8000

# Add the files
ADD ./task6.tar /
# Define the command which runs when the container starts
CMD ["cp -r dependency/* /usr/local/lib/python3.5/dist-packages/ && python3 ./mysite/manage.py runserver 0.0.0.0:8000 && while true; do echo hello world; sleep 1000; done"]

# Use bash as the container's entry point
ENTRYPOINT ["/bin/bash", "-c"]
