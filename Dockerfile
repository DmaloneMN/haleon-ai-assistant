FROM python:3.11-slim

WORKDIR /app

# Install dependencies first for layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY src/ ./src/
COPY pyproject.toml ./

# Install the package in editable mode
RUN pip install --no-cache-dir -e .

EXPOSE 8000

ENV HOST=0.0.0.0
ENV PORT=8000
ENV RELOAD=false

CMD ["uvicorn", "haleon_assistant.main:app", "--host", "0.0.0.0", "--port", "8000"]
