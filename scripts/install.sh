#!/usr/bin/env bash

if ! [ -x "$(which flit)" ]; then
    python3 -m pip install flit
fi

# python3 setup.py install
# python3 -m pip install -e .
flit install --deps develop --symlink --extras test
