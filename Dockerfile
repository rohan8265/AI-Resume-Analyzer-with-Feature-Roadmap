FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Set working directory and change ownership to user
WORKDIR /app
RUN chown -R user:user /app

# Copy requirements
COPY backend/requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Copy backend code and ensure user owns it
COPY --chown=user:user backend/ .

# Switch to the non-root user
USER user

# Expose port 7860 which is required by Hugging Face Spaces
EXPOSE 7860

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
