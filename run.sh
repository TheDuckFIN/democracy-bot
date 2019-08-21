#!/usr/bin/env bash

source .venv/bin/activate

# Load environment variabled from .env file. Allexport will make all variables
# from the file to be automatically exported.
if test -f ".env"; then
    set -o allexport
    source .env
    set +o allexport
fi

python app.py
