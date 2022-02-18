#!/usr/bin/env bash

if ! [ -x "$(which pytest)" ]; then
    python3 -m pip install --upgrade pip
    python3 -m pip install pytest pytest-cov
fi

pytest --cov=binarypp .