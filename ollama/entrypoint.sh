#!/bin/sh
# Start Ollama in the background
ollama serve &

# Wait for Ollama to be ready
sleep 5

# Pull necessary models
ollama pull llama3
ollama pull nomic-embed-text

# Bring Ollama to the foreground to keep the container running
fg %1
