# Use official Python 3.10 slim image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.8.2
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
    chromium \
    chromium-driver \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set work directory
WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock /app/

# Install project dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy project files
COPY . /app/

# Collect and compress static files
RUN python manage.py collectstatic --noinput && \
    python manage.py compress --force

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Expose port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]
