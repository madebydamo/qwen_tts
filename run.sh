#!/bin/bash
set -e

if [ $# -lt 1 ]; then
	echo "Usage: ./run.sh --text 'Your sentence here' [--ref-audio REF] [--ref-text TEXT] [--language LANG] [--name NAME]"
	exit 1
fi

# Detect if running inside Docker container
if [ -f /.dockerenv ]; then
	# Inside container: execute the generation
	python generate.py "$@"
else
	echo "Running via Docker container..."
	if ! docker image inspect qwen3-tts >/dev/null 2>&1; then
		echo "Docker image not found. Building (this may take a minute)..."
		docker compose build
	fi

	docker compose run --remove-orphans -e UID -e GID qwen-tts ./run.sh "$@"

fi
