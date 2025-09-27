# 1. Builder stage: Install dependencies with uv
FROM python:3.11-slim as builder

RUN pip install uv
WORKDIR /app
COPY pyproject.toml .
RUN uv pip install --system -r pyproject.toml

# 2. Final stage: Create the production image
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH /app

# Copy the installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application source code, the shared library, and the ML model
COPY ./app /app/app
COPY ../shared /app/shared_lib

EXPOSE 8000

# Run the application with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]