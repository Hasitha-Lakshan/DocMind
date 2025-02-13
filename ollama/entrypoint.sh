#!/bin/sh
# Start Ollama in the background
ollama serve &

# Wait for Ollama to be ready
sleep 10

# Pull necessary models
ollama pull llama3.2:1b
ollama pull nomic-embed-text

# Keep the container running
wait
