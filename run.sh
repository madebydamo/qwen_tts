#!/bin/bash
if [ $# -lt 2 ]; then
	echo "Usage: ./run.sh <ref_audio> 'Your sentence here' [optional ref_text]"
	exit 1
fi
python generate.py "$1" "$2" "$3"
