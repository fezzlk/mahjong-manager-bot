#!/bin/sh
set -e

# デフォルトは requirements.txt
OUTPUT_FILE=${1:-requirements.txt}

pip install --upgrade pip pip-tools
echo "Python version: $(python --version)"
echo "pip version: $(pip --version)"
echo "pip-compile version: $(pip-compile --version)"

# 引数で出力ファイルを指定
pip-compile --upgrade requirements.in -o "$OUTPUT_FILE"
