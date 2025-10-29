FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire source code into the container
COPY src/ ./src/
COPY configs/ ./configs/
COPY scripts/ ./scripts/
COPY notebooks/ ./notebooks/
COPY data/ ./data/
COPY docs/ ./docs/
COPY tests/ ./tests/
COPY pyproject.toml .
COPY README.md .
COPY LICENSE .

# Command to run the application
CMD ["python", "src/main.py"]