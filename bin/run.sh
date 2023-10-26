#!/bin/sh

# Define path to python executable (in virtual environment).
  PYTHON3="../.venv/bin/python3"

# Execute main python entrypoint.
  cd ../src && $PYTHON3 ./main.py
