#!/bin/sh

# Upgrade all installed python packages.
# https://stackoverflow.com/questions/2720014/how-to-upgrade-all-python-packages-with-pip

pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
