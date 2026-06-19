# Use official Python 3.12 slim image as the base image
# Slim version is lightweight and reduces Docker image size
FROM python:3.12-slim

# Environment Variables
# PYTHONDONTWRITEBYTECODE=1
#   Prevents Python from creating .pyc files inside container , on local it will create
#
# PYTHONUNBUFFERED=1
#   Sends logs directly to terminal without buffering
#   Useful for Docker logs and ECS monitoring
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
# All subsequent commands run from /app
WORKDIR /app

# Update Linux package index
# Install required OS-level packages
#
# build-essential:
#   GCC compiler and build tools needed by some Python packages
#
# curl:
#   Used for API calls, health checks, and debugging
#
# rm -rf:
#   Removes apt cache to keep image size small
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
# uv is a faster replacement for pip
RUN pip install uv

# Copy dependency files first
# This helps Docker cache dependency installation
# Dependencies won't reinstall unless these files change
COPY pyproject.toml uv.lock ./

# Install dependencies exactly as defined in uv.lock
#
# --frozen:
#   Ensures versions match uv.lock exactly
#   Fails build if lock file and pyproject.toml differ
RUN uv sync --frozen

# Copy application source code into container
COPY . .

# Document that application listens on port 5000
# This does not actually expose the port externally
EXPOSE 5001

# Start Flask application
#
# uv run:
#   Runs command inside uv-managed environment
#
# python app.py:
#   Executes Flask application
CMD ["uv", "run", "python", "app.py"]

#Interview Question: What happens when Docker runs this image?
#1. Docker downloads Python 3.12 image.
#2. Creates /app directory.
#3. Installs Linux packages (gcc, curl).
#4. Copies source code into container.
#5. Installs Python dependencies from setup.py.
#6. Opens port 5000.
#7. Executes python app.py.
#8. Flask server starts and listens for requests.



#I using UV 
#Interview Explanation

#When Docker runs:

#Downloads Python 3.12 slim image.
#Creates /app directory.
#Installs Linux packages (curl, gcc, etc.).
#Installs uv.
#Copies pyproject.toml and uv.lock.
#Installs exact dependency versions from uv.lock.
#Copies application source code.
#Exposes port 5000.
#Runs uv run python app.py.
#Flask application starts.


#Interview Explanation (Line by Line)

#FROM python:3.12-slim ->	Creates container with Python 3.12
#ENV --> Sets Python runtime settings
#WORKDIR /app ->	Creates and switches to /app folder
#apt-get install	Installs Linux dependencies
#pip install uv	Installs UV package manager
#COPY pyproject.toml uv.lock ./	Copies dependency files
#uv sync --frozen	Installs dependencies from lock file
#COPY . .	Copies project source code
#EXPOSE 5000	Documents application port
#CMD ["uv","run","python","app.py"]	Starts Flask application