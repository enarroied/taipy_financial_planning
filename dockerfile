# Dockerfile for Monte Carlo Portfolio Simulator with Taipy
# Uses uv for fast, reliable dependency management
# NOT production-grade - uses Taipy's (Flask) default server

FROM python:3.12-slim-bookworm

# Install minimal system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies system-wide using uv (done once at build)
RUN uv pip install --system --no-cache-dir .

# Create a non-root user for security
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
USER appuser

# Copy application source
COPY --chown=appuser:appuser src/ .

# Expose Taipy default port
EXPOSE 5000

# Health check to ensure application is running
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl --fail http://localhost:5000/ || exit 1

# Run the Taipy application
CMD ["taipy", "run", "--no-debug", "--no-reloader", "main.py", "-H", "0.0.0.0", "-P", "5000"]