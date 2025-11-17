# Use official lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install only what we need
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code and files folder
COPY bot.py .
COPY prograde_files ./prograde_files

# Non-root user (security best practice)
RUN adduser --disabled-password --gecos '' botuser
USER botuser

# Run the bot
CMD ["python", "bot.py"]
