#!/bin/bash
# Start Ollama in background
ollama serve &

# Wait for Ollama to be ready
sleep 10

# Pull the models
ollama pull qwen2.5:3b
ollama pull llava:7b

# Start the application
python -m app.main1