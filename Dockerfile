# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Run migrations
RUN python manage.py migrate

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define the command to run your application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "social_network.wsgi:application"]
