#!/bin/sh
set -e

OUTPUT_FILE=${1:-requirements.txt}

pip install --upgrade pip pip-tools
echo "Python version: $(python --version)"
echo "pip version: $(pip --version)"
echo "pip-compile version: $(pip-compile --version)"

pip-compile requirements.in -o "$OUTPUT_FILE"
