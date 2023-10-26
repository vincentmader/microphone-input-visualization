#!/bin/sh

# Create virtual environment for Python, if not already existing.
  [ -d ../.venv ] || python3 -m virtualenv ../.venv

# Install Python dependencies.
  ../.venv/bin/pip install -r ../requirements.txt

# Download Matplotlib styles/themes.
  [ -d ../lib ] || mkdir ../lib
  if [ ! -d ../lib/mpl-styles ]; then
    cd ../lib && git clone https://github.com/vincentmader/mpl-styles
  else
    cd ../lib/mpl-styles && git pull
  fi
