#!/bin/bash

if ! hash python; then
    echo "python is not installed"
    exit 1
fi

ver=$(python -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
if [ "$ver" -lt "27" ]; then
    echo "This script requires python 2.7 or greater"
    exit 1
else
    echo "Installing gzRenamerPro..."
    sleep 1.5
    python src/installers/install.py
fi
