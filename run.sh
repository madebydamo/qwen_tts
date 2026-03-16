#!/bin/bash
set -e

if [ $# -lt 2 ]; then
	echo "Usage: ./run.sh <ref_audio> 'Your sentence here' [optional ref_text]"
	exit 1
fi

# Detect if running inside Docker container
if [ -f /.dockerenv ]; then
	# Inside container: execute the generation
	python generate.py "$1" "$2" "${3:-}"
else
	# On host: build if necessary and run in Docker
	echo "Running via Docker container..."

	# Build image if it doesn't exist
	if ! docker image inspect damotts-qwen-tts >/dev/null 2>&1; then
		echo "Docker image not found. Building (this may take a minute)..."
		docker compose build
	fi

	docker compose run --remove-orphans qwen-tts ./run.sh "$1" "$2" "${3:-}"
fi
