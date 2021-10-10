#!/bin/bash

set -x
set -e

python -m pip install -U pipreqs setuptools twine
pipreqs .
python setup.py check && python setup.py sdist bdist_wheel
twine upload dist/*
