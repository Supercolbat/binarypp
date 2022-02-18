#!/usr/bin/env bash
# https://github.com/tiangolo/fastapi/blob/master/scripts/lint.sh

set -e
set -x

mypy binarypp --no-strict-optional
flake8 binarypp tests
black binarypp tests --check
isort binarypp tests --check-only