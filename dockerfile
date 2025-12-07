# Dockerfile
FROM python:3.12-slim

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Clone or update your bot repo
# (We'll handle pull in entrypoint so it's always fresh)
RUN git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git . || echo "Will pull later"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest (fallback if clone failed)
COPY . .

# Make sure the files folder exists
RUN mkdir -p prograde_files

# Entrypoint that ALWAYS updates from git on container start
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "bot.py"]
