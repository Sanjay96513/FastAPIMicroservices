# 1. Builder stage: Install dependencies with uv
FROM python:3.11-slim as builder

RUN pip install uv
WORKDIR /app
COPY pyproject.toml .
# In a real monorepo, you might install shared dependencies here
# from a shared pyproject.toml to improve layer caching.
RUN uv pip install --system -r pyproject.toml

# 2. Final stage: Create the production image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Set the PYTHONPATH to include the root /app directory, allowing imports
# from both 'app' and 'shared_lib'
ENV PYTHONPATH /app

# Copy the installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application source code and the shared library
# The build context is the service directory (e.g., auth-service/)
COPY ./app /app/app
COPY ../shared /app/shared_lib

# Expose the port the app runs on
EXPOSE 8000

# Run the application with uvicorn, pointing to the correct app module
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]