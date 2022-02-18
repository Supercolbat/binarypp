#!/usr/bin/env bash
# https://github.com/tiangolo/fastapi/blob/master/scripts/format.sh

set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place binarypp tests --exclude=__init__.py
black binarypp tests
isort binarypp tests