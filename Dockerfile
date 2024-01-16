FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    build-essential \
    tesseract-ocr

# Set the working directory
WORKDIR /app

# Copy application code
COPY . /app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt
