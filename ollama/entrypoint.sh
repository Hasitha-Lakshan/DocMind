#!/bin/sh
# Start Ollama in the background
ollama serve &

# Wait for Ollama to be ready
sleep 10

# Pull necessary models
ollama pull llama3.2:1b
ollama pull nomic-embed-text

# Bring Ollama to the foreground to keep the container running
fg %1
