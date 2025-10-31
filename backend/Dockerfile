FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN mkdir /home/movie-store

WORKDIR /home/movie-store

# Copy project configuration first for better Docker layer caching
COPY pyproject.toml ./

# Install dependencies using uv sync (native uv command, not pip!)
# This creates a .venv and installs all dependencies from pyproject.toml
RUN uv sync --no-dev

# Copy application files
COPY app app
COPY migrations migrations
COPY moviestore.py start.sh ./

RUN chmod +x start.sh

ENV FLASK_APP moviestore.py

EXPOSE 5000

ENTRYPOINT ["./start.sh"]