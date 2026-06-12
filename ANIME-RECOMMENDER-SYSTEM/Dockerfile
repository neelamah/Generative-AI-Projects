## Parent image
FROM python:3.11-slim


#__pycache__ is created by Python to store compiled bytecode files for faster execution. In Docker-based deployments, we can disable it by setting PYTHONDONTWRITEBYTECODE=1 in the Dockerfile, so Python does not generate .pyc files inside the container.

## Essential environment variables
## PYTHONDONTWRITEBYTECODE=1 prevents Python from writing __pycache__  .pyc files,it is created by Python for py file and store compiled bytecode files for faster execution.
## PYTHONUNBUFFERED=1 ensures that Python output is sent straight to the terminal without being buffered, which is important for real-time logging and debugging in a Docker environment.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app


## Work directory inside the docker container
WORKDIR /app

## Installing system dependancies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files first (better Docker caching)
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

## Copying ur all contents from local to app
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
#--server.headless=true means we don't want Streamlit to open a browser window when it starts, which is important in a Docker container.
#--server.address=0.0.0.0 means Streamlit will listen on all network interfaces, allowing it to be accessed from outside the container.
#--server.port=8501 specifies the port Streamlit will run on, which is the default port for Streamlit applications.
CMD ["uv", "run", "streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]