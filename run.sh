#!/bin/bash
if [ $# -lt 1 ]; then
	echo "Usage: ./run.sh 'Your sentence here' [optional ref_text]"
	exit 1
fi
python generate.py "$1" "$2"
