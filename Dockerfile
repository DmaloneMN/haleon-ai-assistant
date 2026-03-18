FROM python:3.10-slim

# Create a non-root user for security
RUN useradd --create-home appuser
WORKDIR /home/appuser/app

# Copy project files and install dependencies
COPY pyproject.toml ./
COPY src/ ./src/

RUN pip install --no-cache-dir -e .

USER appuser

EXPOSE 8000

# TODO: adjust workers and timeout for production
CMD ["uvicorn", "haleon_assistant.main:app", "--host", "0.0.0.0", "--port", "8000"]
