# Use an official lightweight Python runtime as the base image.
# The 'slim-bullseye' variant is recommended for a good balance of size and functionality.
FROM python:3.11-slim-bullseye

# Set environment variables
# Prevents Python from writing pyc files to disk and buffering stdout/stderr
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory inside the container.
# All subsequent commands (COPY, RUN, CMD) will be executed in this directory.
WORKDIR /app

# Copy the requirements file first.
# This is a Docker optimization: dependencies change less frequently than code,
# so this allows Docker to cache this layer and speed up subsequent builds.
COPY requirements.txt .

# Install the Python dependencies defined in requirements.txt.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's source code from the host machine to the container's working directory.
COPY . .

# Expose port 8000 on the container.
# This tells Docker that the container listens on this port at runtime.
EXPOSE 8000

# Define the command to run the application.
# Uses uvicorn to run the app (found in `app.main`) and binds it to all interfaces (0.0.0.0)
# so it's accessible from outside the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
