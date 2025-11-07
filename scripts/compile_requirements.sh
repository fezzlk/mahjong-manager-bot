#!/bin/sh
set -e

# デフォルトは requirements.txt
OUTPUT_FILE=${1:-requirements.txt}

pip install --no-cache-dir "pip==24.3.1" "pip-tools==7.5.0"
echo "Python version: $(python --version)"
echo "pip version: $(pip --version)"
echo "pip-compile version: $(pip-compile --version)"

# 引数で出力ファイルを指定
pip-compile --upgrade requirements.in -o "$OUTPUT_FILE"
