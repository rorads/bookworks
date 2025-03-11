# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies including pandoc
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    pandoc \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Copy application files
COPY . .

# Configure poetry to not create a virtual environment
ENV POETRY_VIRTUALENVS_CREATE=false

# Install dependencies
RUN /root/.local/bin/poetry install --no-interaction --no-ansi

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD ["/root/.local/bin/poetry", "run", "python", "-m", "flask", "run", "--host=0.0.0.0"] 