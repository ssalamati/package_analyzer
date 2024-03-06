# Use an Ubuntu base image
FROM ubuntu:22.04

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Install Snapd
RUN apt-get update && \
    apt-get install -y snapd sudo && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["tail", "-f", "/dev/null"]
