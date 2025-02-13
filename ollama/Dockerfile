# Use the official Ollama base image
FROM ollama/ollama:0.5.7

# Set the working directory
WORKDIR /app

# Copy the entrypoint script into the container
COPY entrypoint.sh /app/entrypoint.sh

# Make the script executable
RUN chmod +x /app/entrypoint.sh

# Use the script as the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
