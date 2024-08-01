# Use the specified Bitnami Python image
FROM bitnami/python:3.11.9

# Install system dependencies
RUN apt-get update && \
    apt-get install -y gnupg2 && \
    apt-key update && \
    apt-get update && \
    apt-get install -y \
    libsm6 libxext6 \
    libasound-dev \
    libportaudio2 \
    libportaudiocpp0 \
    portaudio19-dev \
    ffmpeg \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.8.3
  
# System deps:
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml ./

# Project initialization:
RUN poetry install $(test "$YOUR_ENV" == production && echo "--only=main") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Copy the startup script
COPY start.sh .
RUN chmod +x start.sh

# Set the startup script as the entry point
ENTRYPOINT ["./start.sh"]