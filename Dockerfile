# Use Python 3.12.9 with Alpine as the base image
FROM python:3.12.9-alpine

# Install system dependencies required for Django and MySQL
RUN apk update && apk add --no-cache \
    build-base \
    libffi-dev \
    zlib-dev \
    libmagic \
    mysql-client \
    && rm -rf /var/cache/apk/*

# Set the working directory inside the container
WORKDIR /app/

# Set environment variables for Python
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONHASHSEED random
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on

# Install Poetry
RUN pip install poetry

# Configure poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Copy only dependency files first (for caching purposes)
COPY poetry.lock pyproject.toml ./

# Install dependencies (without development dependencies)
RUN poetry install --only main --no-interaction --no-ansi --no-root

# Copy the rest of the application code
COPY . .

# Copy the start_server.sh script
COPY start_server.sh .

# Expose port 8000
EXPOSE 8000

# Make sure the start script is executable
RUN chmod +x "/app/start_server.sh"

# Set the entrypoint to run the start script
ENTRYPOINT [ "./start_server.sh" ]
