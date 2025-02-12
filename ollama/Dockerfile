# Use the official Ollama base image
FROM ollama/ollama:0.5.7

# Set the working directory
WORKDIR /app

# Ensure necessary models are pulled before starting the service
RUN ollama pull nomic-embed-text && ollama pull llama3:1b

# Start Ollama server
CMD ["ollama", "serve"]
