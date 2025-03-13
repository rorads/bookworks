# Use Python 3.10 slim image as base
FROM python:3.10-slim-bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.6.6 /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Install system dependencies including pandoc and build essentials
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    pandoc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


# Copy project files
COPY . .

# Install dependencies via uv
RUN uv sync --frozen

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD ["uv", "run", "python", "-m", "flask", "run", "--host=0.0.0.0"]
