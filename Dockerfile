FROM python:3.9-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    unzip \
    chromium \
    chromium-driver

# Set environment variables
ENV CHROME_DRIVER=/usr/bin/chromedriver

# Add ChromeDriver to PATH
ENV PATH=/usr/bin/chromedriver:$PATH

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the ports for Flask app and Torpy proxy
EXPOSE 5000 9050 9053

# Run Torpy proxy and Flask application
CMD ./init.sh