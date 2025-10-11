#!/bin/sh
pip install --upgrade pip pip-tools
echo "Python version: $(python --version)"
echo "pip version: $(pip --version)"
echo "pip-compile version: $(pip-compile --version)"
pip-compile requirements.in
