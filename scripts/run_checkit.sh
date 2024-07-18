#!/bin/bash

# check path by running "poetry env info --path" under source directory
POETRY_ENV_PATH=$(find $HOME/Library/Caches/pypoetry/virtualenvs -name 'checkit-*' -type d | head -n 1)

if [ -z "$POETRY_ENV_PATH" ]; then
    echo "Error: Could not find Poetry virtual environment for checkit" >&2
    exit 1
fi

source "$POETRY_ENV_PATH/bin/activate"

if [ $? -ne 0 ]; then
    echo "Error: Failed to activate Poetry virtual environment" >&2
    exit 1
fi

checkit "$@"
EXIT_CODE=$?
deactivate
exit $EXIT_CODE