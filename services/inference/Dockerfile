# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /inference

# Copy the requirements.txt file into the container
COPY requirements.txt ./

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container

ADD . /inference


# Run app.py when the container launches
ENTRYPOINT [ "python" ]
CMD ["-u", "app.py"]